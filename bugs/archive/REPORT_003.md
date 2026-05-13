# Bug Report 003: Windows PATH Resolution Failure

**Date:** 2026-05-11
**Scenario:** 04 - Core Pre-Filters
**Status:** Closed (Verified)

---

## 1. Binary Discovery Failure

### Description
On Windows systems, the `context-pipe` orchestrator fails to resolve binaries located in the virtual environment's `Scripts/` folder when using bare command names (e.g. `"cmd": "yq"`), even if the venv is active and the binary exists.

### Verification (2026-05-11)
Successfully verified that `orchestrator.py` -> `resolve_node_cmd()` now includes logic to append `.exe` and manually search user-level bin directories on Windows.

### Evidence
- `ls .venv/Scripts/yq.exe` ✅ (Exists)
- `mcp-pipe run json-optimizer` ❌ (Error: "Command 'yq' not found in system PATH.")
- `pipes.json` with absolute path `C:/.../yq.exe` ✅ (Works)

### Root Cause
In `context_pipe/orchestrator.py` -> `resolve_node_cmd()`, the code uses `shutil.which(cmd)`. On Windows, `shutil.which` may not consistently find executables without the `.exe` suffix depending on the environment state or if the `PATHEXT` variable isn't correctly respected during the subprocess discovery phase. 

Furthermore, although the orchestrator attempts to inject the venv path, the resolution logic appears to bypass this injected path for the initial binary check.

---

## 2. Impact on Lab
Pipes are not portable across machines/OSs because absolute paths are required on Windows to ensure binary discovery.
