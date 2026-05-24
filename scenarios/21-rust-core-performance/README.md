# Scenario 21: Rust Core Stress & Concurrency (cpipe)

## Objective
To measure the performance gains of the Rust-based `cpipe` binary and verify its resilience under high concurrency and protocol violations.

## Setup
- **Tool**: `cpipe` (Rust binary) vs `mcp-pipe` (Python).
- **Pipeline**: `stress-test` (A 3-node chain of `findstr`).
- **Test Harness**: `benchmark.py` (Sequential and parallel execution).

## Execution
Run the benchmarking suite from the scenario directory:
```bash
python benchmark.py
```

## Findings
- **Startup Tax Elimination**: ✅ Rust orchestrator achieved a **21.4x speedup** over Python by eliminating interpreter cold-start.
- **Concurrency Stability**: ✅ Successfully processed 20 parallel instances in 0.14s with near-zero OS overhead.
- **Stream Integrity**: ✅ Strictly enforced UTF-8 encoding, correctly identifying and rejecting binary protocol violations.
