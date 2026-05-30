# Report 034: `_inject_pi()` Template — `execute` Returns Raw String Instead of `{ content }` Object

**Date:** 2026-05-30
**Scenario:** Multi-Platform Parity / pi.dev Integration
**Status:** ✅ Resolved — context-pipe v0.5.2 (verified 2026-05-30)

---

## Description

After fixing REPORT_033 (`"auto"` pipe name), calling any registered tool (`pipe_read_file`, `pipe_run`, etc.) in a pi.dev session produces a hard crash:

```
Error: Cannot read properties of undefined (reading 'some')
```

This crash locks the pi session and forces the user to revert the conversation. It is not catchable within the extension.

---

## Root Cause

All six `execute` handlers in the generated `.pi/extensions/context-pipe.ts` return the raw `string` output of `callCli()` (via Node.js `execSync` with `encoding: "utf-8"`):

```typescript
async execute(_toolCallId, params) {
  const text = readFileSync(params.path, "utf-8");
  return callCli(["run", params.pipe_name || "standard-distill"], text);  // ← returns string
}
```

The pi `ExtensionAPI` requires `execute` to return a **structured result object**:

```typescript
return {
  content: [{ type: "text", text: "..." }],
};
```

This is documented in `extensions.md` (Quick Start example and `registerTool` reference):

> ```typescript
> async execute(toolCallId, params, signal, onUpdate, ctx) {
>   return {
>     content: [{ type: "text", text: "Done" }],
>   };
> }
> ```

### Why `.some()` crashes

Pi's internal tool result processing receives the raw string, then attempts to inspect the `content` array to determine result type (e.g. checking if any item `type === "text"`). The call looks like:

```javascript
result.content.some(item => ...)
```

Because `result` is a plain `string` (not an object), `result.content` is `undefined`. Calling `.some()` on `undefined` throws:

```
TypeError: Cannot read properties of undefined (reading 'some')
```

This is an unrecoverable crash — it propagates out of pi's tool dispatch loop and locks the session.

---

## Affected Tools (all six)

| Tool | Line in `.pi/extensions/context-pipe.ts` | Returns |
|---|---|---|
| `pipe_read_file` | 42 | `callCli(...)` → raw `string` |
| `pipe_run` | 55 | `callCli(...)` → raw `string` |
| `get_pipe_stats` | 65 | `callCli(...)` → raw `string` |
| `list_pipes` | 75 | `callCli(...)` → raw `string` |
| `pipe_analyze_file` | 89 | `callCli(...)` → raw `string` |
| `pipe_run_dynamic` | 101 | `callCli(...)` → raw `string` |

---

## Evidence / Reproduction

### 1. Live crash (2026-05-30)

```
pipe_read_file(path="LAB_STATUS.md")
→ Error: Cannot read properties of undefined (reading 'some')
→ Session locked — user forced to revert conversation
```

### 2. Current extension `execute` return pattern

```bash
$ grep -A3 "async execute" .pi/extensions/context-pipe.ts
    async execute(_toolCallId, params) {
      const text = readFileSync(params.path, "utf-8");
      return callCli(["run", params.pipe_name || "standard-distill"], text);  # ← raw string
    }
```

### 3. Required return shape per `extensions.md`

```typescript
// REQUIRED:
return {
  content: [{ type: "text", text: someString }],
};

// What the template returns (WRONG):
return "raw string output from CLI";
```

---

## Impact

| Dimension | Impact |
|---|---|
| **Severity** | 🔴 Critical — session-locking crash, not a silent failure |
| **All tools broken** | Every registered tool crashes pi identically |
| **User experience** | Forces conversation revert to recover; worst possible failure class |
| **Context safety** | Completely non-functional — no reads, no pipes, no stats |
| **Scope** | All projects onboarded with the `_inject_pi()` template (v0.4.x through v0.5.1) |

---

## Fix (for maintainers, not this agent)

In `target_repos/context-pipe/context_pipe/onboarding.py`, `_inject_pi()` template — wrap every `callCli(...)` return value:

```typescript
// Before (all six execute handlers):
return callCli(["run", params.pipe_name || "standard-distill"], text);

// After:
return { content: [{ type: "text", text: callCli(["run", params.pipe_name || "standard-distill"], text) }] };
```

Apply to all six tools: `pipe_read_file`, `pipe_run`, `get_pipe_stats`, `list_pipes`, `pipe_analyze_file`, `pipe_run_dynamic`.

Also apply to the `tool_result` auto-sift handler's `return` (line ~126) — though that one already returns the correct patch shape `{ content: [...] }`, so it is not affected by this specific bug.

---

## Related

- **REPORT_033** (archived) — Previous failure: `"auto"` not a valid pipe name; fix exposed this crash
- **REPORT_031** (archived) — Original 5-defect report on the template
- `extensions.md` — Documents required `execute` return shape: `{ content: [{ type, text }] }`
- Offending source: `target_repos/context-pipe/context_pipe/onboarding.py` `_inject_pi()` template, all six `execute` handlers
- Deployed file: `.pi/extensions/context-pipe.ts` lines 42, 55, 65, 75, 89, 101
