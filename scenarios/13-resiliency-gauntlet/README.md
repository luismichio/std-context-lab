# Scenario 13: The Resiliency Gauntlet

## Objective
To prove the "Resiliency" claim: that the context supply chain can survive node failures (binary not found, syntax error, or timeout) and continue processing via optional nodes.

## Setup
- **Pipeline**: `gauntlet-pipe` (4 nodes)
    - Node 1: `missing-tool-99` (Design to trigger FileNotFoundError, marked `optional: true`)
    - Node 2: `bad_syntax.py` (Design to trigger Non-zero Exit, marked `optional: true`)
    - Node 3: `forever_sleep.py` (Design to trigger Timeout, marked `optional: true`)
    - Node 4: `semantic-sift-cli logs` (Success node)

## Execution
Run the following command:
```bash
echo "[10:00] ERROR: survive the gauntlet" | mcp-pipe run gauntlet-pipe -v
```

## Findings
- **Failure Bypass**: ✅ **SUCCESS**. The orchestrator successfully survived a 'Not Found', an 'Exit Error', and a 'Timeout' in a single execution.
- **Optional Nodes**: ✅ **PROVEN**. Verified that the new `optional: true` schema flag allows the mental supply chain to continue using the previous node's output when a link breaks.
- **Telemetry Integrity**: ✅ **SUCCESS**. The audit trace (visible with `-v`) correctly recorded all 3 failures while still delivering the final context.
- **Latency**: ⚠️ Verified that timeouts correctly add to the total pipe latency (~30s in this test) but do not block the final result.

## Resolved Bug
**Verified & Closed Bug #015**: The orchestrator is no longer strictly 'Fail-Fast' and can bypass optional node failures.
