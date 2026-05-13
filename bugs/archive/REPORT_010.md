# Bug Report 010: Gemini CLI Hook Timeout

**Date:** 2026-05-11
**Scenario:** Environment Setup / Hook Execution
**Status:** Closed (Verified)

---

## 1. Hook Timeout Failure

### Description
The `context-pipe` hook (`AfterTool` event) fails intermittently in the Gemini CLI with the error `Hook(s) [context-pipe] failed for event AfterTool`.

### Verification (2026-05-11)
Successfully verified that `onboarding.py` now explicitly injects `"timeout": 10000` into the Gemini CLI hook configuration, preventing premature termination during cold starts.

### Root Cause
The `pipe_onboard` tool generates the hook configuration for Gemini CLI but omits the `timeout` parameter. The Gemini CLI appears to have a relatively short default timeout for command hooks. Because the hook invokes a Python interpreter (`context_pipe.orchestrator wrap`), which in turn invokes another binary (`semantic-sift-cli`), the total cold-start latency (approx 300-600ms on Windows) frequently exceeds the default threshold, causing the CLI to terminate the hook prematurely.

### Evidence
Manual execution of the hook command completes successfully with an exit code of 0 and valid JSON. Adding `"timeout": 10000` to the hook configuration in `.gemini/settings.json` resolves the issue.

---

## 2. Impact on Lab
Transparent context sifting is flaky or completely broken depending on system load and disk speed.

### Workaround Applied
Manually injected `"timeout": 10000` into the hook definitions within `.gemini/settings.json`.

### Recommended Fix
In `context_pipe/onboarding.py`, update `merge_hook_json` to explicitly include a reasonable timeout (e.g., `10000` ms) when generating the `command` hook objects for the Gemini CLI.