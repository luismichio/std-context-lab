# Scenario 07: The Mental Supply Chain (E2E)

## Objective
To prove the full Context-Pipe Vision by delivering a multi-node pipeline that orchestrates fetching, formatting, distillation (with a tee snapshot), logic injection, and shipping in a single execution.

## Setup
- **Pipeline**: `e2e-supply-chain`
    - Node 1: `mcp:fetch` (Web content ingestion)
    - Node 2: `prettier` (Normalization via Node.js script)
    - Node 3: `semantic-sift-cli semantic` (Distillation + Tee snapshot)
    - Node 4: `auditor_script.js` (Logic/Context injection)
    - Node 5: `ship_it_mock.js` (Output sink)

## Execution
Run the following script to execute the pipe with input `https://example.com`:
```bash
python run_pipe_manual.py
```

## Findings
- **End-to-End Orchestration**: ✅ Successfully chained 5 nodes across different execution environments (MCP Server, Node.js scripts, Python CLI, Rust engine).
- **Data Flow Reliability**: ✅ The data flowed cleanly from the fetcher, through the formatter and sifter, to the auditor script, and finally saved to a mock issue tracker file.
- **Tee Integration**: ✅ A snapshot was successfully captured before the sifting node to `.tee/snapshot_before_sift.md`.
- **Fault Tolerance (Heuristic Fallback)**: ✅ If the neural model is not pre-warmed or if memory is constrained, `semantic-sift-cli` automatically falls back to its high-speed Rust heuristic mode. This proves the system prioritizes supply chain continuity over failure.
