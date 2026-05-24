# Evidence: Scenario 09 (Adaptive Pressure)

**Verified On:** 2026-05-24
**Baseline:** `context-pipe v0.4.3` | `semantic-sift v0.3.2`

## Verification Command
```powershell
$env:SIFT_RATE="0.1"; mcp-pipe run adaptive-sift --config ../01-protocol-basics/pipes.json --input_file ../01-protocol-basics/sample.log
```

## Captured Evidence (Raw)
*   **Log File**: [run_adaptive_pressure.log](run_adaptive_pressure.log)
*   **Claim Proven**: Verified that node arguments successfully resolve environment variables to dynamically adjust behavior.
