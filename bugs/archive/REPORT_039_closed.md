# REPORT_039: Node-Level `timeout` Field Ignored by Orchestrator

**Date:** 2026-05-30
**Scenario:** 13 — Resiliency Gauntlet
**Status:** 🔴 Confirmed

## Description

The `timeout` field on individual nodes in `pipes.json` is read **nowhere** in the orchestrator. Both the MCP tool path (`_run_mcp_node`) and the binary/validator subprocess path (`_execute_node_chain`) only consult the `PIPE_NODE_TIMEOUT_MS` environment variable (default 30 000 ms). The per-node `"timeout": 2` declaration in pipes.json is silently ignored, meaning every node gets the default 30-second timeout regardless of what the pipe author specified.

## Root Cause

In `context_pipe/orchestrator.py`:

1. **`_run_mcp_node`** (≈ line 282):  
   ```python
   raw_timeout = os.environ.get("PIPE_NODE_TIMEOUT_MS", "30000")
   timeout_s = int(raw_timeout) / 1000.0
   ```
   Never reads `node.get("timeout")`.

2. **`_execute_node_chain`** (≈ line 585):  
   ```python
   raw_timeout = os.environ.get("PIPE_NODE_TIMEOUT_MS", "30000")
   node_timeout = int(raw_timeout) / 1000.0
   ```
   Same — only the env var is used. The variable `node_timeout` is computed **once** before the loop and applied uniformly to every node.

The `"timeout"` key is never extracted from the node dict anywhere in the file:

```bash
grep -n 'node.*timeout\|\.get.*timeout\|node_timeout' context_pipe/orchestrator.py
#  586:    node_timeout = int(raw_timeout) / 1000.0
#  754:                        timeout=node_timeout
#  782:            error_text = f"--- [Context-Pipe: Timeout] ---\nNode {node['cmd']} exceeded {node_timeout}s."
```

No `node.get("timeout")` appears.

## Evidence / Reproduction

**Broken test — node-level timeout is ignored:**

1. Create a pipe with a node that sleeps 10s and `"timeout": 2`:
```json
{
  "name": "required-timeout-pipe",
  "nodes": [
    {
      "cmd": "C:/.../python.exe",
      "args": ["-c", "import sys,time; sys.stdin.read(1); time.sleep(30)"],
      "timeout": 2
    },
    { "cmd": "semantic-sift-cli", "args": ["logs"] }
  ]
}
```

2. Run it:
```bash
echo "test" | mcp-pipe run required-timeout-pipe --config pipes.json
```

3. **Expected:** Hangs for only 2 seconds, then returns `--- [Context-Pipe: Timeout] ---`
4. **Actual:** Hangs for the full 30s default timeout (then returns the same error, but far longer than intended)

**Workaround — env var IS respected:**
```bash
PIPE_NODE_TIMEOUT_MS=2000 echo "test" | mcp-pipe run required-timeout-pipe --config pipes.json
```
→ Returns in ≈2s with the timeout error. ✅

**False pass in S13:** The `forever_sleep.py` script reads **1 character** and exits immediately — it never sleeps at all. The gauntlet-pipe test never exercised the timeout; the `[TIMEOUT]` claim in S13's evidence is incorrect.

## Fix

In `_execute_node_chain`, inside the per-node loop, use `node.get("timeout")` as the per-node timeout before falling back to the env var / global default:

```python
node_timeout_override = node.get("timeout")
node_timeout = int(node_timeout_override) if node_timeout_override is not None else int(os.environ.get("PIPE_NODE_TIMEOUT_MS", "30000")) / 1000.0
```

Apply the same logic in `_run_mcp_node` (or accept the timeout as a parameter from the caller).

## Impact

- **All scenarios** using `"timeout"` in pipes.json are incorrectly using the default 30s timeout instead of the author-intended value.
- **S13** evidence for the timeout test is unreliable — the script used (`forever_sleep.py`) never actually triggered a timeout.
- **S27** MCP banner tolerance may complete slower than intended if verbose MCP servers generate large amounts of banner output.
- User-facing timeout configurations in production pipes are silently ignored.
