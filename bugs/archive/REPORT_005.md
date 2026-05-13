# Bug Report 005: Hook Idempotency Failure

**Date:** 2026-05-11
**Scenario:** Environment Setup / Onboarding
**Status:** Closed (Verified)

---

## 1. Duplicate Hook Registration

### Description
The `pipe_onboard` tool (specifically `merge_hook_json`) fails to prevent duplicate hook registrations if the calling Python interpreter path changes between executions.

### Verification (2026-05-11)
Successfully verified that `merge_hook_json()` now includes a `get_core_target()` normalization step that identifies the `context_pipe.orchestrator wrap` module regardless of the absolute Python path, preventing redundant injections.

### Evidence
In `.gemini/settings.json`, two identical `context-pipe` hooks were registered for the same event (`AfterTool`), but one used the absolute path to the local `.venv` and the other used the global Python path.

### Root Cause
The idempotency logic in `context_pipe/onboarding.py` -> `merge_hook_json()` relies on string matching of the `command` field. Since `build_runtime_hook_command()` uses `sys.executable`, running the onboard tool from different environments generates different command strings, bypassing the duplicate detection.

---

## 2. Impact on Lab
Double-sifting. The same context might be processed twice by two different instances of the orchestrator, leading to unnecessary latency, potential data corruption, and redundant telemetry entries.
