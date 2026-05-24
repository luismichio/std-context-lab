# Evidence: Scenario 12 (Giant File Heart-Attack)

**Verified On:** 2026-05-24
**Baseline:** `context-pipe v0.4.3` | `semantic-sift v0.3.2`

## Verification Command
```powershell
mcp-pipe run giant-sift --config pipes.json --input_file giant_heart_attack.log
```

## Captured Evidence (Raw)
*   **Log File**: [run_giant_file_heart_attack.log](run_giant_file_heart_attack.log)
*   **Claim Proven**: Handled a 50MB log file through the heuristic refinery without memory exhaustion or stream corruption.
