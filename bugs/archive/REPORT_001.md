# Bug Report 001: Orchestration & Telemetry Failures

**Date:** 2026-05-11
**Scenario:** 03 - Research Synthesizer
**Status:** Closed (Verified)

---

## 1. Audit Header Crash (CRITICAL)

### Description
The `context-pipe` orchestrator crashes when a node fails if the audit header is generated.

### Verification (2026-05-11)
Successfully verified that `telemetry.py` now uses `.get("input_size", 0)` to safely handle failed node traces. The CLI passes the `server_registry` correctly, and `orchestrator.py` safely handles string commands.

### Root Cause
In `context_pipe/telemetry.py` -> `generate_audit_header()`, the code assumes every trace entry contains an `"input_size"` key. However, when an MCP node or binary node fails, the orchestrator appends a trace entry that only contains an `"error"` and `"node"` key.

### Error Traceback
```python
KeyError: 'input_size'
  File "context_pipe/telemetry.py", line 111, in generate_audit_header
    start_size = trace[0]["input_size"]
```

### Reproduction (Scenario 04)
Triggered when a binary node command (e.g. `jq`) is missing from the system.
`Get-Content data.json | mcp-pipe run json-optimizer -v`
The orchestrator fails to resolve `jq`, appends an error trace without `input_size`, and `generate_audit_header` crashes.

---

## 2. Terminal CLI Server Registry Leak (MAJOR)

### Description
MCP nodes defined in `pipes.json` cannot be executed via the `mcp-pipe run` or `run-dynamic` terminal commands.

### Root Cause
In `context_pipe/cli.py`, the `_cmd_run` and `_cmd_run_dynamic` handlers load the configuration correctly but fail to pass the `server_registry` dictionary to the `asyncio.run(run_pipe(...))` call. The orchestrator receives an empty registry and fails to resolve any MCP servers.

---

## 3. MCP Command Validation Sensitivity (MINOR)

### Description
The orchestrator fails if an MCP server's `"command"` is a string instead of a list.

### Root Cause
In `context_pipe/orchestrator.py` -> `_run_mcp_node()`, the code accesses `server_cfg["command"]` and attempts to slice it (`cmd[0]`, `cmd[1:]`). If the user provides a string, Python treats the string as a list of characters, leading to invalid command execution (e.g. `'n'` with args `'o','d','e'`).

---

## 4. Impact on Lab
Scenario 03 is blocked from completion. Manual intervention (patching) is required in the source codebase to proceed with multi-node MCP testing.
