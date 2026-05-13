# Bug Report 011: Gemini CLI Incompatibility with Transparent Bypassing

**Date:** 2026-05-11
**Scenario:** Environment Setup / Hook Execution
**Status:** Closed (Verified)

---

## 1. Schema Violation on Bypass

### Description
The `context-pipe` orchestrator crashes the Gemini CLI hook runner whenever it decides to **bypass** a context pipe (i.e., not perform any sifting).

### Verification (2026-05-12)
Successfully verified that `context_pipe/wrapper.py` now includes a `_generate_bypass_payload()` helper. This function correctly returns `{"decision": "allow"}` for the Gemini CLI platform during all intentional bypass paths (signature check, small payload, no matching pipe), satisfying the CLI's schema requirements.

### Root Cause
In `context_pipe/wrapper.py` -> `wrap_payload()`, if the payload is too small, already contains a `CPP_SIGNATURE`, or does not match any routing rules, the function returns `raw_json` (the original tool request/response).

While this "Transparency" is ideal for IDEs that just want the modified text back, the **Gemini CLI** requires a specific **Decision Object** for every hook execution. Returning the original raw JSON violates the schema expected by the CLI, causing it to report: `Hook(s) [context-pipe] failed for event AfterTool`.

### Evidence
Any time a tool is called that returns small output (e.g., `ls` in a small folder), the hook fails. If a tool returns a massive log (matching the `size:>1000` rule), the hook succeeds (because it returns `{"decision": "deny", "reason": "..."}`).

---

## 2. Impact on Lab
Transparent sifting is only active for payloads that trigger a pipe. All other tool executions generate annoying "Hook failed" warnings in the IDE.

### Workaround
There is no clean workaround in the lab without patching the source code to support `"decision": "allow"` fallbacks for the Gemini platform.

### Recommended Fix
In `context_pipe/wrapper.py` and `pipe_hook.py`, all `return raw_json` or `sys.stdout.write(raw_input)` paths must be platform-aware. For "Gemini CLI", they should return:
```json
{
  "decision": "allow"
}
```
instead of the raw input.
