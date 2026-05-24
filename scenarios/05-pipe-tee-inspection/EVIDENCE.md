# Evidence: Scenario 05 (Pipe-Tee Inspection)

**Verified On:** 2026-05-24
**Baseline:** `context-pipe v0.4.3` | `semantic-sift v0.3.2`

## Verification Command
```powershell
Get-Content scenarios/05-pipe-tee-inspection/raw_audit.log | mcp-pipe run tee-pipe --config scenarios/05-pipe-tee-inspection/pipes.json
```

## Captured Evidence (Raw)
*   **Log File**: [run_tee.log](run_tee.log)
*   **Transcript Snippet**:
```log
[] ERROR: Connection to primary database failed! Timeout 3000ms.
[] ERROR: Authentication rejected for user 'admin_svc'.
[] ERROR: Critical segment fault at 0x00000000. Core dumped.
```

## Observation
The `tee` node successfully intercepted the stream *before* it was delivered to the final output, providing a non-breaking audit trail on the local file system. This confirms the "Non-breaking Audit" claim. The raw output in [run_tee.log](run_tee.log) shows the sifted content after the tee capture.
