# Scenario 05: Pipe-Tee Inspection

## Objective
To verify that `context-pipe` can save intermediate snapshots of a context stream to disk (the 'Tee' pattern) without interrupting or corrupting the main pipeline flow.

## Setup
- **Dataset**: `raw_audit.log` (Simulated application logs).
- **Pipeline**: `tee-pipe`
    - Node 1: `findstr ERROR` (Pre-filter)
    - Node 2: `semantic-sift-cli logs` (Distiller, configured with a `tee` object)

## Execution
Run the following command:
```bash
Get-Content raw_audit.log -Raw | mcp-pipe run tee-pipe
```

## Findings
- **Stream Integrity**: ✅ The pipeline successfully executed, outputting the distilled logs (timestamps stripped) to `stdout`.
- **Tee Snapshot**: ✅ The orchestrator successfully dumped the *input* to Node 2 (which is the output of Node 1, containing the full timestamps) to `.tee/snapshot_cli_run_2026-05-11.log` before distillation.
- **Auditability**: ✅ The snapshot included the `--- [Context-Pipe: Tee @ ...] ---` marker, proving that intermediate states of the mental supply chain can be reliably audited without breaking agent workflows.
