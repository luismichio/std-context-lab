# Evidence: Scenario 01 (Protocol Basics)

**Verified On:** 2026-05-24
**Baseline:** `context-pipe v0.4.3` | `semantic-sift v0.3.2`

## Verification Command
```powershell
cd scenarios/01-protocol-basics
Get-Content sample.log | mcp-pipe run basics-pipe
```

## Captured Evidence (Raw)
*   **Log File**: [run_basics.log](run_basics.log)
*   **Transcript Snippet**:
```log
[LAB-TEST-TRANSFORMED] [] INFO: Connection established to remote node.
[LAB-TEST-TRANSFORMED] [] WARN: Latency spike detected on backbone interface.
[LAB-TEST-TRANSFORMED] [] DEBUG: Heartbeat successful.
```

## Observation
The pipeline successfully orchestrated a handoff between a **Node.js runtime** (`transformer.js`) and a **Python/Rust runtime** (`semantic-sift-cli`). 
1. `transformer.js` successfully injected the `[LAB-TEST-TRANSFORMED]` prefix.
2. `semantic-sift-cli` successfully sified the resulting stream, proving the fundamental `stdin`/`stdout` contract of the Context-Pipe Protocol (CPP).
