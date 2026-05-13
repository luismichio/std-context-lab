# Bug Report 018: Hook Deduplication Failure with Shell Prefixes

**Date:** 2026-05-13
**Scenario:** Environment Setup / Hook Injection
**Status:** Closed (Verified)

---

## 1. Idempotency Regression

### Description
During the verification of the `v0.3.0` update (which added shell-prefixed environment variables to Gemini CLI hooks to fix Bug #017), a new regression was discovered. The `pipe_onboard` tool failed to recognize its own previously injected hooks if they contained shell variables (like `$env:PYTHONPATH=...`).

### Evidence
When running `pipe_onboard` on an existing `settings.json`, instead of updating the existing `context-pipe` hook, it would either fail to overwrite the old invalid `"env": {}` schema, or inject duplicate hooks.

### Root Cause
In `context_pipe/onboarding.py`, the `merge_hook_json()` function relied on a strict string match (looking for exactly `context_pipe.orchestrator wrap`) to identify and deduplicate hooks. The logic was brittle and failed to account for complex shell prefix strings, breaking the tool's idempotency.

---

## 2. Impact on Lab
Users attempting to upgrade from `v0.2.2` to `v0.3.0` using `pipe_onboard` were left with corrupt or duplicate `.gemini/settings.json` configurations, requiring manual deletion of the `hooks` section to recover.

---

## 3. Resolution
**Verified in:** `v0.3.1`
The `merge_hook_json` logic was updated upstream to correctly parse and deduplicate hooks regardless of the platform-specific shell prefixes attached to the python command. Re-running `pipe_onboard` now safely replaces old hooks without duplication.
