# Report 036: Native `read` Tool Blocking — Platform Enforcement Gap (Corrected)

**Date:** 2026-05-30
**Scenario:** Multi-Platform Parity — Universal
**Status:** ✅ Resolved (pi.dev gap) — context-pipe v0.5.2 (verified 2026-05-30)

> **Correction notice:** The original version of this report incorrectly stated that Gemini CLI, Antigravity, Windsurf, and Cline did not enforce pre-tool blocking. This was wrong. All four have working pre-tool inhibitors. The report has been fully rewritten based on empirical source analysis.

---

## Corrected Platform-by-Platform Status

| Platform | Pre-tool mechanism | Blocks native read? | Notes |
|---|---|---|---|
| **Gemini CLI** | `BeforeTool` hook → `wrapper.py` | ✅ Yes — `read_file`/`view_file` > 50KB → `{"decision": "deny"}` | Configured in `.gemini/settings.json`; all 4 hooks wired |
| **Antigravity** | `BeforeTool` hook → `wrapper.py` | ✅ Yes — same logic as Gemini CLI | `.agents/settings.json`; same 4-hook pattern |
| **Cline** | `PreToolUse` hook (PS1 + bash) | ✅ Yes — `read_file`/`view_file` > 1KB → `{"cancel": true}` | Platform-native scripts in `.clinerules/hooks/` |
| **Windsurf** | `pre_mcp_tool_use` + security gateway | ✅ Yes — `read_file`/`view_file` > 1KB → `exit 2` + stderr | Matcher: `mcp__.*__(read_file\|view_file)` |
| **pi.dev** | `pi.on("tool_call", ...)` → `{ block: true }` | ❌ No — notifies only, returns `undefined` | Has the API; wrong implementation — **REPORT_035 Defect D** |
| **Cursor** | `postToolUse` only | ❌ No — fires after execution | No `beforeToolUse` hook available in Cursor hook system |
| **Claude Code** | `PostToolUse` only | ❌ No — fires after execution | No pre-tool hook available |
| **Qwen CLI** | `PostToolUse` only | ❌ No — fires after execution | Same pattern as Claude Code |
| **Codex CLI** | `PostToolUse` only | ❌ No — fires after execution | Same pattern as Claude Code |
| **OpenCode** | `tool.execute.before` (not triggered) | ❌ No — known bug #25918 | Hook API exists but not wired by OpenCode runtime |
| **VSCode/GitHub** | Mandate only | ❌ No — no hook system | LLM-compliance only |
| **Kilocode** | Mandate only | ❌ No — no hook system | LLM-compliance only |

---

## Summary

**4 platforms already have working pre-tool blocking** (Gemini CLI, Antigravity, Cline, Windsurf).  
**1 platform has the API capability but uses it incorrectly** (pi.dev — fixable via REPORT_035 Defect D).  
**5 platforms structurally cannot block** (Cursor, Claude Code, Qwen, Codex, OpenCode) — either post-tool-only hooks or no hooks at all.  
**2 platforms rely solely on LLM compliance** (VSCode/GitHub, Kilocode).

---

## Remaining Gap: pi.dev

The only actionable item in this report is the pi.dev implementation gap.

**Current code** (wrong — notifies only):
```typescript
pi.on("tool_call", async (event, ctx) => {
  if (isToolCallEventType("read", event)) {
    ctx.ui.notify("Large file detected. Redirecting to pipe_read_file.", "info");
    // ← returns undefined — native read still executes
  }
});
```

**Required code** (per REPORT_035 Defect D fix):
```typescript
pi.on("tool_call", async (event, ctx) => {
  if (isToolCallEventType("read", event)) {
    try {
      const { statSync } = require("fs");
      const stats = statSync(event.input.path);
      if (stats.size > 1024) {
        return {
          block: true,
          reason: `File is ${(stats.size / 1024).toFixed(1)}KB. Use pipe_read_file("${event.input.path}") instead.`
        };
      }
    } catch (e) {}
  }
});
```

Once fixed, pi.dev joins Gemini CLI, Antigravity, Cline, and Windsurf as platforms with active pre-tool enforcement.

---

## Platforms with Structural Gap (No Pre-Tool Hook Available)

For Cursor, Claude Code, Qwen, Codex, and OpenCode — enforcement is not possible today via hooks. These platforms depend entirely on:
1. The AGENTS.md mandate being present and clear.
2. The model reliably following it.

**Potential mitigation for post-tool-only platforms:** inject a visible `[MANDATE VIOLATION DETECTED]` warning into the `AfterTool`/`PostToolUse` output when a raw file read passes through without a context-pipe audit header — alerting the model it bypassed the mandate in the previous turn.

---

## Related

- **REPORT_035 Defect D** — pi.dev `tool_call` implementation (the only actionable fix)
- `context_pipe/wrapper.py` lines 83–113 — `BeforeTool` handler with `{"decision": "deny"}`
- `context_pipe/onboarding.py` — `_inject_gemini()` line 949, `_inject_windsurf()` line 1037, `_inject_cline()` line 1050, `_inject_antigravity()` line 1419
- OpenCode issue #25918 — `tool.execute.after` not triggered by runtime
