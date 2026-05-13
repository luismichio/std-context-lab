# Bug Report 006: Gemini Hook Payload Incompatibility

**Date:** 2026-05-11
**Scenario:** Environment Setup / Onboarding
**Status:** Closed (Verified)

---

## 1. Incorrect Hook Response Schema

### Description
The `context-pipe` orchestrator (specifically the `wrapper.py` logic) returns the original JSON payload with the `llmContent` modified. However, the Gemini CLI hook system requires a specific "Decision" schema to override or modify tool output.

### Verification (2026-05-11)
Successfully verified that `context_pipe/platforms.py` -> `inject_content()` now correctly returns the `{ "decision": "deny", "reason": content }` schema when the platform is identified as "Gemini CLI".

### Root Cause
In `context_pipe/platforms.py` -> `inject_content()`, the code attempts to modify the `llmContent` inside the `tool_response` object. 

Gemini CLI expects the hook to return:
```json
{
  "decision": "deny",
  "reason": "<THE_SIFTED_CONTENT>"
}
```
`context-pipe` currently returns:
```json
{
  "tool_name": "...",
  "tool_response": { "llmContent": "<THE_SIFTED_CONTENT>" }
}
```
Because the return object does not contain a `decision` key, the Gemini CLI likely treats the hook as "Failed" or ignores its output, resulting in the error message: `Hook(s) [context-pipe] failed for event AfterTool`.

---

## 2. Impact on Lab
Transparent context sifting is completely broken on the Gemini platform. The "Subconscious Interceptor" claim is unverified for this environment.
