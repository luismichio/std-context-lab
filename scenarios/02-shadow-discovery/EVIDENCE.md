# Evidence: Scenario 02 (Shadow Discovery)

**Verified On:** 2026-05-24
**Baseline:** `context-pipe v0.4.3` | `semantic-sift v0.3.2`

## Verification Command
```powershell
mcp-pipe tool list --config pipes.json
```

## Captured Evidence (Raw)
*   **Log File**: [run_shadow_discovery.log](run_shadow_discovery.log)
*   **Claim Proven**: The orchestrator correctly identified and listed shadow MCP nodes without requiring global registration.
