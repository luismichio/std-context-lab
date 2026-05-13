# Bug Report 008: Gemini CLI Environment Detection Failure in Hooks

**Date:** 2026-05-11
**Scenario:** Environment Setup / Hook Execution
**Status:** Closed (Verified)

---

## 1. Hook Platform Detection Failure

### Description
The `context-pipe` hook (`AfterTool` event) fails to identify the execution environment as "Gemini CLI" on Windows. Consequently, it falls back to a generic MCP response schema instead of the specific `{ decision: deny }` schema required by Gemini, causing the hook to crash with "Hook(s) [context-pipe] failed for event AfterTool."

### Verification (2026-05-11)
Successfully verified that `onboarding.py` now automatically injects `{"GEMINI_SESSION_ID": "true"}` into the hook configuration.

### Root Cause
In `context_pipe/platforms.py`, the `detect_client_id()` function relies on two heuristics:
1. Presence of environment variables (like `GEMINI_SESSION_ID`).
2. Parent process names containing `"gemini"`.

When the Gemini CLI spawns a hook process on Windows, it runs via `powershell.exe` -> `node.exe`, and the `GEMINI_SESSION_ID` environment variable is **not** automatically passed to the hook's shell environment. Because neither heuristic matches, `detect_client_id()` falls through.

### Evidence
Running a manual environment inspection within a child process spawned by the CLI reveals:
- `GEMINI_SESSION_ID`: `None`
- Parent process names: `['python.exe', 'powershell.exe', 'node.exe', 'node.exe', 'pwsh.exe', 'WindowsTerminal.exe']`

---

## 2. Impact on Lab
Transparent context sifting is broken.

### Workaround Applied
Manually injected `"GEMINI_SESSION_ID": "lab-test"` into the `"env"` dict of the hook definitions within `.gemini/settings.json`.

### Recommended Fix
In `context_pipe/onboarding.py`, the `merge_hook_json` payload for Gemini should automatically include `"env": { "GEMINI_SESSION_ID": "true" }` to guarantee platform detection regardless of the OS process tree.
