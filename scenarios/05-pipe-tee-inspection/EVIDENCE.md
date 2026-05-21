# Evidence: Scenario 05 (Pipe-Tee Inspection)

**Verified On:** 2026-05-18
**Baseline:** `context-pipe v0.4.0` | `semantic-sift v0.3.2`

## Verification Command
```powershell
Get-Content scenarios/05-pipe-tee-inspection/raw_audit.log | mcp-pipe run tee-pipe --config scenarios/05-pipe-tee-inspection/pipes.json
```

## Captured Evidence (Tee Snapshot)
The following content was automatically captured by the `tee` hook in `pipes.json` and persisted to `.tee/snapshot_cli_run_2026-05-11.log`.

```log
[2026-05-11 12:00:02] ERROR: Connection to primary database failed! Timeout 3000ms.
[2026-05-11 12:00:04] ERROR: Authentication rejected for user 'admin_svc'.
[2026-05-11 12:00:06] ERROR: Critical segment fault at 0x00000000. Core dumped.

--- [Context-Pipe: Tee @ semantic-sift-cli | 2026-05-11T20:39:22.481454+00:00] ---
```

## Observation
The `tee` node successfully intercepted the stream *before* it was delivered to the final output, providing a non-breaking audit trail on the local file system. This confirms the "Non-breaking Audit" claim.
