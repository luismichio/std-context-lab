# Bug Report 012: Schema Violation on Hook Exception

**Date:** 2026-05-12
**Scenario:** Environment Setup / Hook Execution
**Status:** Open

---

## 1. Safety Fallback Schema Violation

### Description
The `context-pipe` hook (`AfterTool` event) crashes the Gemini CLI hook runner whenever an internal Python exception occurs. The IDE reports: `Hook(s) [context-pipe] failed for event AfterTool`.

### Root Cause
In `pipe_hook.py`, there is a global `except Exception:` block designed for "Absolute Safety." If any error occurs (e.g., `ImportError` when loading the wrapper, configuration file reading failure, etc.), the block executes:
`sys.stdout.write(raw_input)`

As identified in Bug #011, the **Gemini CLI** strictly requires a **Decision Object** response schema. Returning the original raw JSON payload on an error path violates this schema, causing the CLI to reject the entire hook execution.

### Evidence
Manual testing confirms that if the `PYTHONPATH` is missing or the `import context_pipe` fails, the script outputs the raw input JSON. When this happens during a Gemini CLI session, the "Hook failed" message appears because the CLI cannot find the mandatory `decision` key.

---

## 2. Impact on Lab
The "Absolute Safety" fallback is actually "Absolute Failure" for the Gemini platform. Any minor environment discrepancy results in an IDE warning rather than a silent bypass.

### Recommended Fix
The `except Exception:` block in `pipe_hook.py` must be platform-aware. For "Gemini CLI", it should return:
```json
{
  "decision": "allow",
  "reason": "Context-Pipe encountered an internal error and bypassed sifting."
}
```
instead of the raw input.
