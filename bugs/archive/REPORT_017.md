# Bug Report 017: Invalid Hook Configuration (Schema Misunderstanding)

**Date:** 2026-05-12
**Scenario:** Environment Setup / Hook Execution
**Status:** Closed (Verified)

---

## 1. Unsupported `env` Key in Hook Schema

### Description
The configuration of the `context-pipe` hook in `.gemini/settings.json` relied on an `"env"` dictionary to pass critical environment variables (`PYTHONPATH`, `GEMINI_SESSION_ID`). However, the Gemini CLI hook schema for `"type": "command"` does not support the `"env"` key.

### Verification (2026-05-12)
Successfully verified that `onboarding.py` now identifies the platform as Gemini and automatically moves the `PYTHONPATH` and `GEMINI_SESSION_ID` into the `command` string using shell-specific syntax (`$env:` for Windows, inline for POSIX), ensuring full schema compliance and variable persistence.

### Impact
The variables were silently ignored. This caused:
1. **`ImportError`**: The hook could not find the `context_pipe` module because `PYTHONPATH` was missing.
2. **Detection Failure**: The orchestrator could not identify the platform as "Gemini CLI" because `GEMINI_SESSION_ID` was missing.
3. **Schema Violation**: The hook fell back to returning raw JSON, which the Gemini CLI rejects.

### Root Cause
Misinterpretation of the Gemini CLI settings schema. While MCP Server registrations support a nested `"env"` object, Command Hooks do not.

---

## 2. Evidence
Investigation via the `cli_help` sub-agent confirmed that the `command` hook schema only supports `type`, `command`, `name`, `timeout`, and `description`.

---

## 3. Recommended Fix
Move all required environment variables into the `command` string itself using platform-appropriate shell syntax (e.g., `$env:VAR='value'; ...` for PowerShell).
