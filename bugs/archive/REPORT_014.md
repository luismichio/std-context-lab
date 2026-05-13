# Bug Report 014: Unicode Encoding Crash on Windows Shell

**Date:** 2026-05-12
**Scenario:** 12 - Giant File Heart-Attack
**Status:** Open

---

## 1. CLI Audit Header Crash

### Description
On Windows systems using standard PowerShell or CMD, the `mcp-pipe` terminal tool crashes with a `UnicodeEncodeError` when the `-v` (verbose) flag is used.

### Evidence
```python
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4ca' in position 43: character maps to <undefined>
  File "context_pipe/cli.py", line 79, in _print_audit
    sys.stdout.write(header)
```
The character `\U0001f4ca` (📊) in the audit header header is incompatible with the default `cp1252` encoding of the Windows shell.

### Root Cause
The `_print_audit` function in `cli.py` uses `sys.stdout.write()` with strings containing rich Unicode emojis. If the host shell is not configured for UTF-8 (the default for most Windows installations), Python's `stdout` fails to encode the characters.

---

## 2. Impact on Lab
Audit traces are unusable on Windows without manual environment intervention (`$env:PYTHONUTF8=1`).

### Recommended Fix
The CLI should either:
1. Detect encoding capabilities and use ASCII fallbacks (e.g. `[SIGNAL]` instead of `📊`).
2. Force `sys.stdout.reconfigure(encoding='utf-8')` if the platform is Windows and the output is a TTY.
