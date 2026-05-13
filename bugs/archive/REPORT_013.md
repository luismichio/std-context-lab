# Bug Report 013: Missing Placeholder Resolution in Node Arguments

**Date:** 2026-05-12
**Scenario:** 09 - Adaptive Pressure Simulation
**Status:** Open

---

## 1. Static Arguments in `pipes.json`

### Description
The `context-pipe` orchestrator fails to resolve `${VAR}` environment placeholders when they are used inside the `args` array of a node definition. 

### Evidence
- `pipes.json` defined with: `"args": ["semantic", "--rate", "${SIFT_RATE}"]`
- Shell environment set: `$env:SIFT_RATE="0.1"`
- Execution Result: `semantic-sift-cli: error: argument --rate: invalid float value: '${SIFT_RATE}'`

### Root Cause
Analysis of `context_pipe/config_loader.py` reveals that `_resolve_env_placeholders()` is only called on the `env` dictionary of server definitions. There is no equivalent resolution logic for the `args` list in the `orchestrator.py` node execution loop.

---

## 2. Impact on Lab
The **Adaptive Window Pressure** claim is currently unverified. Pipes cannot dynamically adjust their behavior (like compression depth) based on environment signals without patching the orchestrator.

### Recommended Fix
In `context_pipe/orchestrator.py`, before spawning a subprocess node, the `args` list should be passed through a resolver that replaces `${VAR}` tokens with values from `os.environ`.
