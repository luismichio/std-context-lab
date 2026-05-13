# Context-Pipe Scenarios: The Mental Supply Chain Lab

This document consolidates the details, objectives, and findings for all 17 test scenarios executed in the `std-context-lab`. It serves as the definitive reference for the technical claims verified during Phase 1 (Protocol Basics & Feature Validation) and Phase 2 (Operational Hardening).

---

## Phase 1: Feature Validation

### Scenario 01: Protocol Basics
*   **Last Verified In**: `v0.3.1`
*   **Objective**: Prove the fundamental `stdin`/`stdout` contract and language agnosticism of the Context-Pipe Protocol (CPP).
*   **Setup**: A simple `basics-pipe` executing a Node.js script (`transformer.js`) followed by the `semantic-sift-cli` (Rust/Python hybrid).
*   **Status**: ✅ **Verified**. Proved multi-language orchestration by passing text cleanly between Node.js and Rust environments via standard I/O.

### Scenario 02: Shadow Discovery
*   **Last Verified In**: `v0.3.1`
*   **Objective**: Prove the "Zero Tool Bloat" claim. The orchestrator must execute MCP nodes dynamically without registering them in the global IDE.
*   **Setup**: Configured `@modelcontextprotocol/server-everything` in a local `pipes.json`.
*   **Status**: ✅ **Verified**. The `mcp-pipe tool` command correctly executed shadow server functionalities without global registration.

### Scenario 03: Research Synthesizer
*   **Last Verified In**: `v0.3.1`
*   **Objective**: Prove the "Mental Supply Chain" claim by chaining multiple tools to reduce massive web bloat into high-signal context.
*   **Setup**: A 3-node pipe (`mcp-server-fetch` -> `markitdown` -> `semantic-sift`).
*   **Status**: ✅ **Verified**. Successfully fetched, converted, and distilled HTML content into dense Markdown signal in a single pass.

### Scenario 04: Core Pre-Filters
*   **Last Verified In**: `v0.3.1`
*   **Objective**: Prove massive context reduction using deterministic OS-native binaries before passing to the neural refinery.
*   **Setup**: Utilized `findstr` / `rg` / `jq` as early pipeline nodes to quickly filter raw log data.
*   **Status**: ✅ **Verified**. Massive deterministic reduction achieved, effectively lowering the computational load on the LLM.

### Scenario 05: Pipe-Tee Inspection
*   **Last Verified In**: `v0.3.1`
*   **Objective**: Prove non-breaking stream auditing using the T-Pipe (`tee`) stream splitter.
*   **Setup**: A pipeline that captures snapshots to a `.tee/` folder *before* semantic sifting occurs.
*   **Status**: ✅ **Verified**. Snapshots were successfully written to disk without interrupting or corrupting the standard output stream delivered to the LLM.

### Scenario 06: Agent-to-Agent (A2A) Testing
*   **Last Verified In**: `v0.3.1`
*   **Objective**: Prove "Refined Handoff ROI" during multi-agent workflows.
*   **Setup**: Tested a live handoff between a 'Researcher' and 'Reviewer' sub-agent using `pipe_agent_handoff`.
*   **Status**: ✅ **Verified**. Captured real-world ROI telemetry indicating over 1,200 characters of noise incinerated during the handshake while maintaining perfect reasoning fidelity.

### Scenario 07: The Mental Supply Chain (E2E Flagship)
*   **Last Verified In**: `v0.3.1`
*   **Objective**: Deliver a full orchestration flow showcasing the power of Context-Pipe across disparate tools.
*   **Setup**: A 5-node E2E pipe: `fetch` -> `prettier` -> `semantic-sift` (with tee) -> `auditor_script.js` -> `ship_it_mock.js`.
*   **Status**: ✅ **Verified**. Safely streamed data across MCP servers, Node.js scripts, Python CLIs, and Rust engines in one execution.

### Scenario 08: Multi-Modal Distillation
*   **Last Verified In**: `v0.3.1`
*   **Objective**: Prove format agnosticism (HTML, PDF, DOCX, etc.) using `markitdown` as a universal pre-refinery node.
*   **Setup**: Chained `markitdown` with `semantic-sift`.
*   **Status**: ✅ **Verified**. Distilled complex formatted documents into clean Markdown, fulfilling the Dual-Channel Mandate for both Shell and Agent channels.

### Scenario 09: Adaptive Pressure Simulation
*   **Last Verified In**: `v0.3.1`
*   **Objective**: Prove "Adaptive Signaling" by injecting contextual pressure metrics into pipeline arguments dynamically.
*   **Setup**: Utilized `$env:SIFT_RATE` to dynamically set the neural compression rate based on the agent's context window.
*   **Status**: ✅ **Verified**. After an upstream orchestrator fix (Bug #013), node arguments successfully resolved dynamic shell placeholders.

### Scenario 10: The Structured Data Auditor
*   **Last Verified In**: `v0.3.1`
*   **Objective**: Prove the "Structured Data Exemption" — intentional bypass of valid JSON payloads to prevent structural corruption.
*   **Setup**: Queried a mock SQLite DB with 1,000 bloated telemetry rows.
*   **Status**: ✅ **Verified**. Sift engine safely detected valid JSON arrays and bypassed mutation to protect data structure.

### Scenario 11: Supply Chain Visualization
*   **Last Verified In**: `v0.3.1`
*   **Objective**: Prove the "System over Patch" (Observability) claim.
*   **Setup**: Built `pipes_to_mermaid.py` and a `viz-pipe` meta-pipeline.
*   **Status**: ✅ **Verified**. Successfully generated Mermaid flowcharts directly from the local `pipes.json`, proving architectural transparency.

---

## Phase 2: Operational Hardening

### Scenario 12: The "Giant File" Heart-Attack
*   **Last Verified In**: `v0.3.1`
*   **Objective**: Stress-test stream stability and Rust-sidecar memory management.
*   **Setup**: Processed a 50.6 MB raw log file through the heuristic refinery.
*   **Status**: ✅ **Verified**. Processed 50MB in ~6 seconds. The orchestrator's "Truncation Guard" safely triggered, preventing memory exhaustion.

### Scenario 13: The Resiliency Gauntlet
*   **Last Verified In**: `v0.3.1`
*   **Objective**: Test error handling and failure bypasses under cascading node failures.
*   **Setup**: A 5-node pipe with intentional failures (missing binary, syntax error, timeout), utilizing the `optional: true` schema.
*   **Status**: ✅ **Verified**. The orchestrator successfully surfaced error strings as `[Context-Pipe: Dependency Error]` and bypassed failures via optional nodes to deliver the final context.

### Scenario 14: The Security "Black Hole"
*   **Last Verified In**: `v0.3.1`
*   **Objective**: Prove the "Zero-Trust Context" claim via massive PII scrubbing.
*   **Setup**: Ingested a log stream with 1,500 fake AWS keys, emails, and credit cards.
*   **Status**: ✅ **Verified**. Processed via a custom high-performance Python Regex node, successfully redacting 100% of the secrets in milliseconds before LLM ingestion.

### Scenario 15: Recursive Supply Chains
*   **Last Verified In**: `v0.3.1`
*   **Objective**: Prove "Pipeline Encapsulation" by calling a pipe inside another pipe.
*   **Setup**: `recursive-pipe` invoking `mcp-pipe run inner-distiller`.
*   **Status**: ✅ **Verified**. `stdin` and `stdout` maintained integrity across nested processes. The Echo Guard (`CPP_SIGNATURE`) successfully prevented infinite looping.

### Scenario 16: Protocol Violation Stress
*   **Last Verified In**: `v0.3.1`
*   **Objective**: Stress-test the system against malicious or corrupt binary data streams.
*   **Setup**: An intentional "Bad Actor" node outputting invalid UTF-8 byte sequences (`\xff\xfe\xfd`).
*   **Status**: ✅ **Verified**. The orchestrator successfully replaces non-UTF8 bytes with `` placeholders and executes cleanly without crashing the Python stream.

### Scenario 17: Version Awareness & Self-Update
*   **Last Verified In**: `v0.3.1`
*   **Objective**: Determine if the system can detect an outdated state and provide actionable "Self-Heal" CLI commands.
*   **Setup**: Mocked a downgraded local version (v0.2.0) against the remote v0.3.1.
*   **Status**: ✅ **Verified**. `pipe_verify` successfully queries GitHub, detects the version discrepancy, and outputs a self-healing upgrade command to the user.

---

## Conclusion
The `std-context-lab` successfully processed 17 comprehensive architectural and operational tests. All 17 claims are fully proven, and all identified bugs have been resolved upstream.