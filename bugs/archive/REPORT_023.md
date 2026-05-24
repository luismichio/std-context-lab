# Bug Report 023: Missing SessionStart Hook in Onboarding

**Date:** 2026-05-24
**Scenario:** Environment Setup / Hook Injection
**Status:** Closed (Verified)

---

## 1. Missing Hook Event

### Description
The `pipe_onboard` tool (and the specialized `_inject_gemini` helper) fails to register the `SessionStart` hook, even though it is supported by the Gemini CLI (v0.41.0+).

### Evidence
- `onboarding.py` loop: `for hook_key in ["BeforeTool", "AfterTool", "PreCompress"]:`
- Gemini CLI documentation: Supports `SessionStart` for initial context injection.
- `.gemini/settings.json`: No `SessionStart` entry after onboarding.

### Root Cause
The `onboarding.py` logic in `context-pipe` has not been updated to include the `SessionStart` event in its automated injection loop. While `BeforeTool`, `AfterTool`, and `PreCompress` handle tool-level sifting, `SessionStart` is required for platform-level initialization and providing the agent with early context regarding the sifting environment.

---

## 2. Impact on Lab
Agents may lack critical "Day 0" instructions regarding the presence of Context-Pipe until the first tool is invoked. This can lead to a slightly degraded initial experience where the agent might attempt non-sifted native calls before the mandates are fully reinforced by a `BeforeTool` or `AfterTool` interception.

### Recommended Fix
Update the hook injection loop in `context_pipe/onboarding.py` to include `SessionStart`.
```python
for hook_key in ["SessionStart", "BeforeTool", "AfterTool", "PreCompress"]:
    # ... injection logic ...
```
