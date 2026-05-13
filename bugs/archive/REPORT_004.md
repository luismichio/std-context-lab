# Bug Report 004: Missing Hook Injection for Gemini CLI

**Date:** 2026-05-11
**Scenario:** Environment Setup / Onboarding
**Status:** Closed (Verified)

---

## 1. Missing `hooks` in `settings.json`

### Description
When running `pipe_onboard(environment="Gemini")`, the tool successfully injects slash commands into `.gemini/commands/*.toml` but fails to register the required `AfterTool` hooks in `.gemini/settings.json`.

### Verification (2026-05-11)
Successfully verified that `pipe_onboard` now includes logic for Gemini CLI to call `merge_hook_json()`, correctly injecting the `AfterTool` and `PreCompress` event hooks using the absolute path to the orchestrator.

### Impact
The "Subconscious Interceptor" (transparent context sifting) does not work in the Gemini CLI. The agent must call `/pipe-run` manually, or the user must manually trigger pipes. The core claim of "transparent context shielding" is unfulfilled for this platform.

### Evidence
- `pipe_onboard` returns success. ✅
- `.gemini/commands/` populated. ✅
- `.gemini/settings.json` remains unchanged (contains only `mcpServers`). ❌

### Root Cause
Analysis of `context_pipe/onboarding.py` shows that the `Gemini` block (lines 699-730) only creates `.toml` command files. It lacks the logic to modify `settings.json` to add the `hooks` registry, unlike the `Cursor` or `VSCode` blocks which use `merge_hook_json()`.

---

## 2. Recommended Fix
Implement `merge_hook_json()` for the `.gemini/settings.json` path using the `AfterTool` event schema supported by the Gemini CLI.
