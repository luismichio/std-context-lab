# Bug Report 020: Protocol Violation Crash (Non-UTF8 Stream)

**Date:** 2026-05-13
**Scenario:** 16 - Protocol Violation Stress
**Status:** Open

---

## 1. Stream Integrity Failure

### Description
The `context-pipe` orchestrator crashes when a node outputs invalid UTF-8 byte sequences or binary garbage. It does not sanitize the stream, leading to a fatal Python `UnicodeDecodeError` within the subprocess reading thread, followed by a `TypeError` in the orchestrator.

### Root Cause
In `context_pipe/orchestrator.py` -> `run_pipe()`, the subprocess execution uses `subprocess.communicate()` which likely assumes text decoding with strict error handling, or the thread reading the output crashes on invalid UTF-8 bytes. 

When the `UnicodeDecodeError` happens in the `_readerthread`, `process.communicate()` returns `None` for stdout, leading to a subsequent crash:
```python
end_size = len(stdout)  # TypeError: object of type 'NoneType' has no len()
```

### Evidence
Running a pipe with a node that outputs `b"garbage: \xff\xfe\xfd\n"` results in:
```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 52: invalid start byte
...
TypeError: object of type 'NoneType' has no len()
```

---

## 2. Impact on Lab
The "Stream Integrity" and "Platform Safety" claims are **UNVERIFIED / FAILED**. A "bad actor" node or a node that accidentally outputs binary data (like `cat image.png`) will completely crash the orchestrator and the agent session.

### Recommended Fix
1. Execute subprocesses with `errors="replace"` or `errors="ignore"` to safely handle non-UTF8 bytes without crashing the reading thread.
2. Add a `None` check for `stdout` in `run_pipe()` to handle cases where `communicate()` fails to return a string.