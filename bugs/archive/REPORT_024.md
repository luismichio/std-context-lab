# Bug Report 024: Hook Duplication & Idempotency Failure

**Date:** 2026-05-24
**Scenario:** Environment Setup / Hook Injection
**Status:** Closed (Verified)

### Verification (2026-05-24)
Successfully verified that `pipe_onboard` in v0.4.5 is now fully idempotent. Re-running the tool on an existing `settings.json` results in zero duplicates, confirming the fingerprint-based fingerprinting is working correctly.


---

## 1. Redundant Hook Injection (MAJOR)

### Description
The `pipe_onboard` tool (specifically `merge_hook_json`) fails to identify and replace existing Context-Pipe hooks if their internal command structure has changed. This results in duplicate hook entries in `settings.json`, leading to double-sifting, increased latency, and confusing telemetry.

### Evidence
In the current `.gemini/settings.json`, the `AfterTool` and `PreCompress` lists contain two entries for "context-pipe":
1.  **Previous Interpreted-style Hook**: Uses `$env:PYTHONPATH=...; python -m context_pipe.orchestrator wrap`.
2.  **Modern Nested Hook**: Uses `python -c "import sys; sys.path.insert(0, ...); from context_pipe.orchestrator import main; main()"` within a `matcher` block.

**Naming Inconsistency**: 
Investigation of `onboarding.py` reveals that while Gemini and Antigravity hooks are explicitly assigned the name `"context-pipe"`, hooks for Cursor and VS Code/GitHub are injected as **anonymous objects** (omitting the `name` field entirely). This lack of a unified identifier forces the deduplication logic to rely on fragile command-string matching.

### Root Cause
In `context_pipe/onboarding.py`, the specialized injection helpers are inconsistent:
- `_inject_gemini`: Includes `{"name": "context-pipe", ...}`.
- `_inject_cursor` & `_inject_vscode_github`: Include only `{"command": ...}`.
- `merge_hook_json`: Only normalizes the `command` string for deduplication and does not utilize the `name` field as a primary key.

---

## 2. Proposed Improvements

### A. Fingerprint-based Deduplication
Instead of searching for substrings in the `command`, the logic should:
1.  Check the `name` field. If `name == "context-pipe"`, treat it as a candidate for replacement.
2.  Use a more flexible regex to identify the orchestrator entry point (e.g., `(context_pipe\.orchestrator|from context_pipe\.orchestrator)`).

### B. Interactive Conflict Resolution
When `pipe_onboard` detects a hook that *looks* like Context-Pipe but has a different command string than the one being injected, it should:
1.  Display a diff of the old vs. new command.
2.  Ask the user: *"Detected a previous/modified 'context-pipe' hook. Replace it with the modern version? [Y/n]"*
3.  Provide an option to "Keep Both" only if explicitly requested.

---

### Follow-up (2026-05-24)
While the `is_context_pipe_hook` logic is now robust, the `merge_hook_json` implementation has a logic error:
```python
if new_hook in hooks_list:
    return False  # Exactly present, nothing to do
```
Because this check happens **before** the list is filtered, the tool will never clean up legacy hooks if the modern hook has already been injected in a previous run. The check should either happen after filtering or include a check for other context-pipe hooks.
