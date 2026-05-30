# Report 033: `_inject_pi()` Template Uses `"auto"` as Pipe Name — Not a Valid CLI Pipe

**Date:** 2026-05-30
**Scenario:** Multi-Platform Parity / pi.dev Integration
**Status:** ✅ Resolved — context-pipe v0.5.1 (verified 2026-05-30)

---

## Description

After REPORT_032 was fixed (onboarding now regenerates `.pi/extensions/context-pipe.ts`), calling `pipe_read_file` in a pi.dev session produces a new hard failure:

```
Command failed: ".../.venv/Scripts/python.exe" -m context_pipe.cli run auto
mcp-pipe: error: Pipe 'auto' not found.
  Available: standard-distill, semantic-refinery, research-pipe, ...
```

The v0.5.0 `_inject_pi()` template uses `"auto"` as a pipe name fallback in two places. `"auto"` is **not a registered pipe** and the CLI `_cmd_run` handler performs a direct name lookup with no special-case handling for it — it simply throws `Pipe 'auto' not found`.

---

## Root Cause

Two occurrences in the TypeScript template string inside `_inject_pi()` (`context_pipe/onboarding.py`):

### Occurrence 1 — `pipe_read_file` default (line ~1249 of `onboarding.py`)

```typescript
async execute(_toolCallId, params) {
  const text = readFileSync(params.path, "utf-8");
  return callCli(["run", params.pipe_name || "auto"], text);  // ← "auto" invalid
}
```

When called without an explicit `pipe_name`, this produces `mcp-pipe run auto` — rejected immediately.

### Occurrence 2 — `tool_result` auto-sift handler (line ~1293 of `onboarding.py`)

```typescript
pi.on("tool_result", async (event, ctx) => {
  const text = event.content?.[0]?.text;
  if (typeof text === "string" && text.length > 5000) {
    ...
    const sifted = callCli(["run", "auto"], text);  // ← "auto" invalid
    return { content: [{ type: "text", text: sifted }] };
  }
});
```

Every large tool result triggers this handler, which also fails with the same error.

### Why `"auto"` doesn't exist

The CLI `_cmd_run` in `context_pipe/cli.py` resolves pipe names by direct lookup only:

```python
pipe = next((p for p in config.get("pipes", []) if p["name"] == args.pipe_name), None)
if pipe is None:
    _die(f"Pipe '{args.pipe_name}' not found. ...")
```

There is no `"auto"` built-in — the `resolve_pipe_from_context()` function in `orchestrator.py` handles auto-routing via `mappings`, but it is only invoked internally by the MCP server layer, not exposed as a named pipe in the CLI.

### Correct default

The MCP `server.py` `pipe_read_file` tool uses `"standard-distill"` as its default (`pipe_name: str = "standard-distill"`, line 155). The project `pipes.json` also maps all inputs to `"standard-distill"` via the `default` trigger in `mappings`. The correct fallback for both template occurrences is `"standard-distill"`.

---

## Evidence / Reproduction

### 1. Live test failure (2026-05-30)

```
pipe_read_file(path="LAB_STATUS.md")
→ Command failed: python -m context_pipe.cli run auto
→ mcp-pipe: error: Pipe 'auto' not found.
   Available: standard-distill, semantic-refinery, ...
```

### 2. Offending lines in the regenerated extension

```bash
$ grep -n "auto" .pi/extensions/context-pipe.ts
42:      return callCli(["run", params.pipe_name || "auto"], text);
126:        const sifted = callCli(["run", "auto"], text);
```

### 3. CLI confirms no "auto" pipe

```bash
$ python -m context_pipe.cli run auto <<< "test"
mcp-pipe: error: Pipe 'auto' not found.
  Available: standard-distill, semantic-refinery, research-pipe, ...
```

### 4. Server default confirms `"standard-distill"` is correct

```bash
$ grep "pipe_name.*standard" target_repos/context-pipe/context_pipe/server.py
    pipe_name: str = "standard-distill",
```

---

## Impact

| Dimension | Impact |
|---|---|
| **`pipe_read_file`** | Always fails when called without explicit `pipe_name` (the standard usage) |
| **Auto-sift interceptor** | Every large tool result triggers a failed CLI call — `tool_result` handler throws on all large outputs |
| **Context safety** | Both the primary read tool and the auto-sift fallback are non-functional — context flooding is unguarded |
| **Scope** | Affects every project onboarded with v0.5.0 `_inject_pi()` template |

---

## Fix (for maintainers, not this agent)

In `target_repos/context-pipe/context_pipe/onboarding.py`, `_inject_pi()` template:

**Occurrence 1:**
```typescript
// Before:
return callCli(["run", params.pipe_name || "auto"], text);
// After:
return callCli(["run", params.pipe_name || "standard-distill"], text);
```

**Occurrence 2:**
```typescript
// Before:
const sifted = callCli(["run", "auto"], text);
// After:
const sifted = callCli(["run", "standard-distill"], text);
```

---

## Related

- **REPORT_032** (archived) — Previous `pipe_read_file` failure (stale extension not regenerated); fix exposed this new defect
- **REPORT_031** (archived) — Original 5-defect report on the broken template
- Offending source: `target_repos/context-pipe/context_pipe/onboarding.py` `_inject_pi()` template, two occurrences of `"auto"`
- Deployed file: `.pi/extensions/context-pipe.ts` lines 42 and 126
