# Scenario 15: Recursive Supply Chains

## Objective
To prove the "Encapsulation" claim: complex supply chains can be built by nesting existing pipes within each other using the standard CLI runner as a node.

## Setup
- **Inner Pipe**: `inner-distiller` (Wraps `semantic-sift-cli logs`)
- **Recursive Pipe**: `recursive-pipe`
    - Node 1: `mcp-pipe run inner-distiller` (Executes the inner pipe via CLI)

## Verification (Dual-Channel)

### 1. Shell Channel
Run: `echo "[2026-05-12 10:00:00] ERROR: recursive" | mcp-pipe run recursive-pipe -v`
- **Result**: ✅ **SUCCESS**. The outer orchestrator successfully spawned the inner CLI, which processed the data and returned it through the chain.

### 2. Agent Channel
Run: `pipe_run(pipe_name="recursive-pipe")`
- **Result**: ✅ **SUCCESS**. Full parity with the Shell Channel.

## Findings
- **Modular Design**: ✅ **PROVEN**. Verified that Context-Pipes can be used as building blocks for higher-level orchestration without modifying the core logic of the inner pipes.
- **Protocol Integrity**: ✅ Verified that `stdin`/`stdout` flow correctly through nested layers of the orchestrator.
- **Echo Guard Synergy**: ✅ Confirmed that the `CPP_SIGNATURE` is correctly respected by nested pipes, preventing redundant processing loops.
