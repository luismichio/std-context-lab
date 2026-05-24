# Evidence: Scenario 15 (Recursive Supply Chains)

**Verified On:** 2026-05-24
**Baseline:** `context-pipe v0.4.3` | `semantic-sift v0.3.2`

## Verification Command
```powershell
mcp-pipe run recursive-distill --config ../01-protocol-basics/pipes.json --input_file ../01-protocol-basics/sample.log
```

## Captured Evidence (Raw)
*   **Log File**: [run_recursive_supply_chains.log](run_recursive_supply_chains.log)
*   **Claim Proven**: Proved "Pipeline Encapsulation" by calling a pipe inside another pipe without infinite loops, thanks to the Echo Guard.
