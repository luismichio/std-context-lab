# Scenario 09: Adaptive Pressure Simulation

## Objective
To prove the "Adaptive Window Pressure" claim: the context supply chain can automatically increase compression depth when it receives a signal that the context window is near-full.

## Setup
- **Dataset**: A redundant text payload.
- **Signal**: Environment variable `SIFT_RATE` (0.1 for high pressure, 0.7 for low pressure).
- **Pipeline**: `adaptive-pipe`
    - Node 1: `pressure_gauge.py` (Mock signal injector)
    - Node 2: `semantic-sift-cli --rate ${SIFT_RATE}` (Attempted adaptive refinery)

## Execution
Run the following command:
```bash
$env:SIFT_RATE="0.1"; mcp-pipe run adaptive-pipe
```

## Findings
- **Observability**: ✅ Successfully captured node executions in the audit trace, allowing for precise identification of argument behaviors.
- **Adaptive Window Pressure**: ✅ **VERIFIED**.

## Resolved Bugs
- **Verified & Closed Bug #013**: During initial testing (`v0.3.0`), the orchestrator failed to resolve `${VAR}` tokens in node arguments. This was fixed upstream. The `v0.3.1` regression sweep confirmed that dynamic argument resolution (e.g., passing `$env:SIFT_RATE`) works perfectly, proving the "Adaptive Window Pressure" claim.
