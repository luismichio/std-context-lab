# Evidence: Scenario 13 (Resiliency Gauntlet)

**Verified On:** 2026-05-24
**Baseline:** `context-pipe v0.4.3` | `semantic-sift v0.3.2`

## Verification Command
```powershell
mcp-pipe run resilience-pipe --config pipes.json --input_file ../01-protocol-basics/sample.log
```

## Captured Evidence (Raw)
*   **Log File**: [run_resiliency_gauntlet.log](run_resiliency_gauntlet.log)
*   **Claim Proven**: Proved that the system gracefully handles and bypasses node failures via the `optional: true` schema.
