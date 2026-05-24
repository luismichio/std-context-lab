# Evidence: Scenario 04 (Core Pre-Filters)

**Verified On:** 2026-05-24
**Baseline:** `context-pipe v0.4.3` | `semantic-sift v0.3.2`

## Verification Command
```powershell
mcp-pipe run noisy-filter --config pipes.json --input_file noisy_app.log
```

## Captured Evidence (Raw)
*   **Log File**: [run_core_prefilters.log](run_core_prefilters.log)
*   **Claim Proven**: Proved massive deterministic context reduction using OS-native pre-filters before the neural refinery.
