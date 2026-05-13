# Bug Report 009: Python RuntimeWarning Corrupting Hook Output

**Date:** 2026-05-11
**Scenario:** Environment Setup / Hook Execution
**Status:** Closed (Verified)

---

## 1. Hook Output Corruption

### Description
The newly refactored `context-pipe` hook (`AfterTool` and `PreCompress` events) crashes the Gemini CLI hook runner. The IDE reports: `Hook(s) [context-pipe] failed for event AfterTool`.

### Verification (2026-05-11)
Successfully verified that `onboarding.py` -> `build_runtime_hook_command()` now injects the `-W ignore` flag into the Python command, suppressing the warning and restoring a clean JSON stream.

### Root Cause
In a recent update, the onboarding tool (`onboarding.py`) was changed to register the hook command as:
`python -m context_pipe.orchestrator wrap`

Because `orchestrator.py` is inside the `context_pipe` package, running it as `__main__` via `-m` causes Python to emit a `RuntimeWarning` to `stderr`:
`<frozen runpy>:128: RuntimeWarning: 'context_pipe.orchestrator' found in sys.modules after import of package 'context_pipe', but prior to execution of 'context_pipe.orchestrator'; this may result in unpredictable behaviour`

The Gemini CLI hook system captures this warning (either by merging `stderr` with `stdout`, or by failing if `stderr` is non-empty) and fails to parse the subsequent JSON payload.

### Evidence
Manual testing in the shell reveals the `RuntimeWarning` prefixing the JSON output. Adding the `-W ignore` flag to the Python invocation completely suppresses the warning and restores a pure JSON stream.

---

## 2. Impact on Lab
Transparent context sifting remains broken due to stream corruption.

### Workaround Applied
Manually updated `.gemini/settings.json` to include the `-W ignore` flag in the hook commands.

### Recommended Fix
Update `context_pipe/onboarding.py` -> `build_runtime_hook_command()` to inject `-W ignore` into the Python command array when registering hooks, or revert to executing `pipe_hook.py` directly.