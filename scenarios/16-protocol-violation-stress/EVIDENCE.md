# Evidence: Scenario 16 (Protocol Violation Stress)

**Verified On:** 2026-05-24
**Baseline:** `context-pipe v0.4.3` | `semantic-sift v0.3.2`

## Verification Command
```powershell
python bad_actor.py | mcp-pipe run standard-distill --config ../01-protocol-basics/pipes.json
```

## Captured Evidence (Raw)
*   **Log File**: [run_protocol_violation_stress.log](run_protocol_violation_stress.log)
*   **Claim Proven**: Proved system resilience against malicious/corrupt binary streams by successfully sanitizing non-UTF8 bytes.
