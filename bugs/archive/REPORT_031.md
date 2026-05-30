# Report 031: `_inject_pi()` Generates Broken pi.dev Extension — 5 Defects in Template

**Date:** 2026-05-27
**Scenario:** Multi-Platform Parity
**Status:** ✅ Resolved — context-pipe v0.5.0 (verified 2026-05-30)

---

## Description

The `_inject_pi()` function in `target_repos/context-pipe/context_pipe/onboarding.py` (added per REPORT_030) generates a pi.dev TypeScript extension at `.pi/extensions/context-pipe.ts` that contains **5 distinct defects** making it non-functional:

1. **Tool execute signatures use wrong parameter position** — all three registered tools (`pipe_read_file`, `pipe_run`, `get_pipe_stats`) fail to receive their parameters.
2. **Fast path CLI command `cpipe` not in PATH** — the Rust `cpipe.exe` fast path always fails, forcing costly Python fallback.
3. **`tool_result` interceptor reads `event.result` (undefined)** — field name is wrong, so auto-sift never triggers.
4. **`tool_result` mutates event directly instead of returning a patch** — mutation has no effect on the tool result.
5. **`pipe-stats` command uses `execute()` instead of `handler()`** — command is never registered because pi ignores unrecognized properties.

Additionally, **3 tools referenced in the companion skill/AGENTS.md mandate are not registered**:
- `list_pipes`
- `pipe_analyze_file`
- `pipe_run_dynamic`

This means the pi.dev extension looks plausible at a glance but is functionally dead — none of the interceptors fire, none of the tools return valid parameters, and the command doesn't register.

## Root Cause

All defects originate in the `_inject_pi()` function's TypeScript template string at **lines 1206–1352** of `target_repos/context-pipe/context_pipe/onboarding.py`. The template was written without testing against pi's actual `ExtensionAPI` signatures.

### Defect 1: Tool execute signatures (line ~1252–1274)

**Template code:**
```typescript
async execute(input) {
  const args = ["run", input.pipe_name || "auto", "--file", input.path];
  return callCli(args);
}
```

**pi ExtensionAPI signature** (from pi docs `extensions.md`):
```typescript
async execute(toolCallId: string, params: T, signal: AbortSignal, onUpdate: OnUpdateCallback, ctx: ExtensionContext)
```

The first parameter is `toolCallId` (a string like `"call_abc123"`), not the user-supplied parameters. Parameters arrive in the **second** argument. So `input.pipe_name` reads `undefined` from string prototype — no error, just silent failure.

**Affected tools:** `pipe_read_file`, `pipe_run`, `get_pipe_stats`

### Defect 2: Bare `cpipe` command (line ~1214)

**Template code:**
```typescript
const cmd = `cpipe ${args.join(" ")}`;
return execSync(cmd, { input, encoding: "utf-8" });
```

On Windows (and likely other platforms where `cpipe` is not on `PATH`), `execSync("cpipe ...")` throws with `ENOENT`. The catch block silently falls through to the Python fallback, adding ~1000ms cold-start overhead per invocation. The project already has a resolved absolute path to `cpipe.exe` — the Python onboarding script itself resolves it earlier during `resolve_pipes_config()`, but that resolved path is not passed into the template.

**Evidence:**
```bash
$ which cpipe
which: no cpipe in (PATH...)

$ cpipe stats 2>&1
bash: cpipe: command not found

$ .venv/Scripts/cpipe.exe stats 2>&1  # works
## Context-Pipe Balance Sheet
...
```

### Defect 3–4: `tool_result` handler (line ~1300)

**Template code:**
```typescript
pi.on("tool_result", async (event, ctx) => {
  if (typeof event.result === "string" && event.result.length > 5000) {
    // ...
    event.result = sifted;
  }
});
```

**Two bugs in one block:**

1. **Wrong field name:** The `ToolResultEvent` interface exposes `event.content` (an array of `{ type: string, text: string }`), not `event.result`. The string `event.result` is always `undefined`, so the size check `undefined.length > 5000` throws a silent `TypeError` caught by the outer try/catch.

2. **Wrong mutation pattern:** pi's event API expects handlers to **return** a partial patch object to modify results:
   ```typescript
   return { content: [{ type: "text", text: sifted }] };
   ```
   Mutating `event.result` has no effect on the actual tool result delivered to the LLM.

### Defect 5: Command handler (line ~1345)

**Template code:**
```typescript
pi.registerCommand("pipe-stats", {
  description: "View Context-Pipe Balance Sheet",
  async execute() {
    const stats = callCli(["stats"]);
    console.log(stats);
  }
});
```

**pi API** (from pi docs `extensions.md`):
```typescript
pi.registerCommand("name", {
  description: "...",
  handler: async (args, ctx) => { ... }
});
```

The property must be `handler`, not `execute`. pi silently ignores unknown properties, so the command never registers.

### Defect 6: Missing tools

The companion skill (`context-pipe.md`) and the mandate (`AGENTS.md`) instruct the LLM to use `list_pipes()`, `pipe_analyze_file(path)`, and `pipe_run_dynamic(nodes_json, input_text)`, but none of these are registered as pi tools. The LLM will attempt to call non-existent tools, producing tool-not-found errors.

## Evidence / Reproduction

### Repro 1: Generated extension is identical to buggy template

```bash
# Run onboarding
$ mcp-pipe onboard Gemini
# Check generated file
$ grep -n "async execute(" .pi/extensions/context-pipe.ts
6:    async execute(input) {       # <-- should be (toolCallId, params, ...)
14:    async execute(input) {       # <-- same
21:    async execute() {            # <-- same (though no params needed here)

$ grep -n "event.result" .pi/extensions/context-pipe.ts
29:    if (typeof event.result === "string"  # <-- should be event.content
30:    event.result = sifted;                 # <-- should return patch

$ grep -n "execute" .pi/extensions/context-pipe.ts
43:    async execute() {                      # <-- should be handler
```

### Repro 2: Tool calls silently accept undefined params

After `/reload` in pi.dev, calling the registered `pipe_read_file` tool with valid params:

```
LLM calls: pipe_read_file({ path: "README.md" })
```

- `toolCallId` = `"call_abc"` (a string)
- `input` (which is actually `toolCallId`) = `"call_abc"`
- `input.pipe_name` = `undefined` → defaults to `"auto"`
- `input.path` = `undefined` → CLI receives `--file undefined`
- Result: CLI errors confusingly about path resolution

### Repro 3: Auto-sift never fires

After generating a large (>5KB) tool result:

```
LLM calls: bash("cat huge-file.log")
// result is 50KB string
// tool_result handler fires
// event.result === undefined
// TypeError: Cannot read properties of undefined (reading 'length')
// caught by empty catch block, silent no-op
```

## Impact

| Dimension | Impact |
|---|---|
| **Functionality** | All 3 registered tools return junk params; both interceptors are no-ops; command doesn't register |
| **User experience** | Extension loads without errors, appears to work, silently does nothing — hardest class of bug to diagnose |
| **Context safety** | Auto-sift interceptor never fires, so large tool results flood the context window unchecked |
| **Mandate alignment** | Mandate instructs LLM to use `pipe_read_file`, `list_pipes`, etc., but only `pipe_read_file` exists and it's broken |
| **Perf** | Fast path to Rust `cpipe` binary always fails — every invocation pays ~1000ms Python cold-start tax |

## Fix (for maintainers, not this agent)

In `target_repos/context-pipe/context_pipe/onboarding.py`, `_inject_pi()` function:

1. **Tool executors:** Change all three `execute(input)` → `execute(_toolCallId, params, ...)` and use `params.pipe_name`, `params.path`, etc.

2. **Fast path:** Replace bare `cpipe` with the resolved absolute path (available earlier in the onboarding flow via `resolve_pipes_config()`). Pass it into the template or read it from the resolved config.

3. **`tool_result` handler:**
   - Change `event.result` → `event.content?.[0]?.text`
   - Change `event.result = sifted` → `return { content: [{ type: "text", text: sifted }] }`

4. **Command:** Change `execute()` → `handler: async (_args, _ctx) => { ... }`

5. **Add missing tools:** Register `list_pipes`, `pipe_analyze_file`, `pipe_run_dynamic` to match the mandate.

## Related

- REPORT_030 (original feature request for pi.dev integration)
- [pi Extension API docs](https://pi.dev/docs/extensions) — `execute(toolCallId, params, signal, onUpdate, ctx)` signature
- Generated file: `target_repos/context-pipe/context_pipe/onboarding.py` lines 1206–1352
- Generated output: `.pi/extensions/context-pipe.ts` (any project running `mcp-pipe onboard` with pi detection)
