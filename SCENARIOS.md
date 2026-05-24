# Context-Pipe Scenarios: The Mental Supply Chain Lab

This document consolidates the details, objectives, and findings for all 21 test scenarios executed in the `std-context-lab`. 

**The Verifiable Proof Standard**: As of `v0.4.3`, all scenarios have been audited to meet the **Verifiable Proof** standard. Every scenario directory now contains a raw terminal `.log` file and a structured `EVIDENCE.md` file, providing immutable proof of the technical claims.

---

## Phase 1: Feature Validation

### Scenario 01: Protocol Basics
*   **Last Verified In**: `v0.4.3`
*   **Objective**: Prove the fundamental `stdin`/`stdout` contract and language agnosticism of the Context-Pipe Protocol (CPP).
*   **Setup**: A simple `basics-pipe` executing a Node.js script (`transformer.js`) followed by the `semantic-sift-cli` (Rust/Python hybrid).
*   **Status**: ✅ **Verified**. Proved multi-language orchestration by passing text cleanly between Node.js and Rust environments via standard I/O.
*   **Proof**: [run_basics.log](scenarios/01-protocol-basics/run_basics.log)

### Scenario 02: Shadow Discovery
*   **Last Verified In**: `v0.4.3`
*   **Objective**: Prove the "Zero Tool Bloat" claim. The orchestrator must execute MCP nodes dynamically without registering them in the global IDE.
*   **Setup**: Configured `@modelcontextprotocol/server-everything` in a local `pipes.json`.
*   **Status**: ✅ **Verified**. The `mcp-pipe tool` command correctly executed shadow server functionalities without global registration.
*   **Proof**: [run_shadow_discovery.log](scenarios/02-shadow-discovery/run_shadow_discovery.log)

### Scenario 03: Research Synthesizer
*   **Last Verified In**: `v0.4.3`
*   **Objective**: Prove the "Mental Supply Chain" claim by chaining multiple tools to reduce massive web bloat into high-signal context.
*   **Setup**: A 3-node pipe (`mcp-server-fetch` -> `markitdown` -> `semantic-sift`).
*   **Status**: ✅ **Verified**. Successfully fetched, converted, and distilled HTML content into dense Markdown signal in a single pass.
*   **Proof**: [run_research_synthesizer.log](scenarios/03-research-synthesizer/run_research_synthesizer.log)

### Scenario 04: Core Pre-Filters
*   **Last Verified In**: `v0.4.3`
*   **Objective**: Prove massive context reduction using deterministic OS-native binaries before passing to the neural refinery.
*   **Setup**: Utilized `findstr` / `rg` / `jq` as early pipeline nodes to quickly filter raw log data.
*   **Status**: ✅ **Verified**. Massive deterministic reduction achieved, effectively lowering the computational load on the LLM.
*   **Proof**: [run_core_prefilters.log](scenarios/04-core-prefilters/run_core_prefilters.log)

### Scenario 05: Pipe-Tee Inspection
*   **Last Verified In**: `v0.4.3`
*   **Objective**: Prove non-breaking stream auditing using the T-Pipe (`tee`) stream splitter.
*   **Setup**: A pipeline that captures snapshots to a `.tee/` folder *before* semantic sifting occurs.
*   **Status**: ✅ **Verified**. Snapshots were successfully written to disk without interrupting or corrupting the standard output stream delivered to the LLM.
*   **Proof**: [run_tee.log](scenarios/05-pipe-tee-inspection/run_tee.log)

### Scenario 06: Agent-to-Agent (A2A) Testing
*   **Last Verified In**: `v0.4.3`
*   **Objective**: Prove "Refined Handoff ROI" during multi-agent workflows.
*   **Setup**: Tested a live handoff between a 'Researcher' and 'Reviewer' sub-agent using `pipe_agent_handoff`.
*   **Status**: ✅ **Verified**. Captured real-world ROI telemetry indicating noise incineration during the handshake.
*   **Proof**: [run_a2a_handoff.log](scenarios/06-a2a-handoff/run_a2a_handoff.log)

### Scenario 07: The Mental Supply Chain (E2E Flagship)
*   **Last Verified In**: `v0.4.3`
*   **Objective**: Deliver a full orchestration flow showcasing the power of Context-Pipe across disparate tools.
*   **Setup**: A 5-node E2E pipe: `fetch` -> `prettier` -> `semantic-sift` (with tee) -> `auditor_script.js` -> `ship_it_mock.js`.
*   **Status**: ✅ **Verified**. Safely streamed data across MCP servers, Node.js scripts, Python CLIs, and Rust engines in one execution.
*   **Proof**: [run_mental_supply_chain.log](scenarios/07-mental-supply-chain/run_mental_supply_chain.log)

### Scenario 08: Multi-Modal Distillation
*   **Last Verified In**: `v0.4.3`
*   **Objective**: Prove format agnosticism (HTML, PDF, DOCX, etc.) using `markitdown` as a universal pre-refinery node.
*   **Setup**: Chained `markitdown` with `semantic-sift`.
*   **Status**: ✅ **Verified**. Distilled complex formatted documents into clean Markdown.
*   **Proof**: [run_multi_modal_distillation.log](scenarios/08-multi-modal-distillation/run_multi_modal_distillation.log)

### Scenario 09: Adaptive Pressure Simulation
*   **Last Verified In**: `v0.4.3`
*   **Objective**: Prove "Adaptive Signaling" by injecting contextual pressure metrics into pipeline arguments dynamically.
*   **Setup**: Utilized `$env:SIFT_RATE` to dynamically set the neural compression rate based on the agent's context window.
*   **Status**: ✅ **Verified**. Node arguments successfully resolved dynamic shell placeholders.
*   **Proof**: [run_adaptive_pressure.log](scenarios/09-adaptive-pressure/run_adaptive_pressure.log)

### Scenario 10: The Structured Data Auditor
*   **Last Verified In**: `v0.4.3`
*   **Objective**: Prove the "Structured Data Exemption" — intentional bypass of valid JSON payloads to prevent structural corruption.
*   **Setup**: Queried a mock SQLite DB with 1,000 bloated telemetry rows.
*   **Status**: ✅ **Verified**. Sift engine safely detected valid JSON arrays and bypassed mutation to protect data structure.
*   **Proof**: [run_structured_data_auditor.log](scenarios/10-structured-data-auditor/run_structured_data_auditor.log)

### Scenario 11: Supply Chain Visualization
*   **Last Verified In**: `v0.4.3`
*   **Objective**: Prove the "System over Patch" (Observability) claim.
*   **Setup**: Built `pipes_to_mermaid.py` and a `viz-pipe` meta-pipeline.
*   **Status**: ✅ **Verified**. Successfully generated Mermaid flowcharts directly from the local `pipes.json`.
*   **Proof**: [run_observability_viz.log](scenarios/11-observability-viz/run_observability_viz.log)

---

## Phase 2: Operational Hardening

### Scenario 12: The "Giant File" Heart-Attack
*   **Last Verified In**: `v0.4.3`
*   **Objective**: Stress-test stream stability and Rust-sidecar memory management.
*   **Setup**: Processed a 50.6 MB raw log file through the heuristic refinery.
*   **Status**: ✅ **Verified**. Processed 50MB in ~6 seconds without memory exhaustion.
*   **Proof**: [run_giant_file_heart_attack.log](scenarios/12-giant-file-heart-attack/run_giant_file_heart_attack.log)

### Scenario 13: The Resiliency Gauntlet
*   **Last Verified In**: `v0.4.3`
*   **Objective**: Test error handling and failure bypasses under cascading node failures.
*   **Setup**: A 5-node pipe with intentional failures, utilizing the `optional: true` schema.
*   **Status**: ✅ **Verified**. The orchestrator successfully bypassed failures via optional nodes.
*   **Proof**: [run_resiliency_gauntlet.log](scenarios/13-resiliency-gauntlet/run_resiliency_gauntlet.log)

### Scenario 14: The Security "Black Hole"
*   **Last Verified In**: `v0.4.3`
*   **Objective**: Prove the "Zero-Trust Context" claim via massive PII scrubbing.
*   **Setup**: Ingested a log stream with 1,500 fake secrets.
*   **Status**: ✅ **Verified**. Successfully redacted 100% of the secrets before LLM ingestion.
*   **Proof**: [run_security_black_hole.log](scenarios/14-security-black-hole/run_security_black_hole.log)

### Scenario 15: Recursive Supply Chains
*   **Last Verified In**: `v0.4.3`
*   **Objective**: Prove "Pipeline Encapsulation" by calling a pipe inside another pipe.
*   **Setup**: `recursive-pipe` invoking `mcp-pipe run inner-distiller`.
*   **Status**: ✅ **Verified**. The Echo Guard (`CPP_SIGNATURE`) successfully prevented infinite looping.
*   **Proof**: [run_recursive_supply_chains.log](scenarios/15-recursive-supply-chains/run_recursive_supply_chains.log)

### Scenario 16: Protocol Violation Stress
*   **Last Verified In**: `v0.4.3`
*   **Objective**: Stress-test the system against malicious or corrupt binary data streams.
*   **Setup**: An intentional "Bad Actor" node outputting invalid UTF-8 byte sequences.
*   **Status**: ✅ **Verified**. The orchestrator successfully sanitized non-UTF8 bytes without crashing.
*   **Proof**: [run_protocol_violation_stress.log](scenarios/16-protocol-violation-stress/run_protocol_violation_stress.log)

### Scenario 17: Version Awareness & Self-Update
*   **Last Verified In**: `v0.4.3`
*   **Objective**: Determine if the system can detect an outdated state and provide actionable "Self-Heal" CLI commands.
*   **Setup**: Mocked a downgraded local version (v0.2.0) against the remote v0.4.3.
*   **Status**: ✅ **Verified**. Successfully detected discrepancy and output self-healing command.
*   **Proof**: [run_version_awareness.log](scenarios/17-version-awareness/run_version_awareness.log)

### Scenario 18: Autonomous Dynamic Sifting
*   **Last Verified In**: `v0.4.3`
*   **Objective**: Prove the "Dynamic Sifting" capability, allowing agents to assemble JIT processing graphs on-the-fly.
*   **Setup**: Run a dynamic graph (`grep` -> `semantic-sift-cli`) against a custom log file.
*   **Status**: ✅ **Verified**. Proved JIT graph assembly and execution.
*   **Proof**: [run_autonomous_dynamic_sifting.log](scenarios/18-autonomous-dynamic-sifting/run_autonomous_dynamic_sifting.log)

---

## Phase 3: Battle Testing & Rust Core

### Scenario 19: Proactive Gating Resilience (`BeforeTool`)
*   **Last Verified In**: `v0.4.3`
*   **Objective**: Test the `BeforeTool` hook against boundary conditions and massive files to ensure robust proactive context protection.
*   **Status**: ✅ **Verified**. Successfully denied native reads on a 50MB file while allowing small config reads and failing-safe on unknown tools.
*   **Proof**: [run_gating_battle_test.log](scenarios/19-beforetool-gating/run_gating_battle_test.log)

### Scenario 20: Line Range Precision & Fallbacks (`pipe_read_file`)
*   **Last Verified In**: `v0.4.3`
*   **Objective**: Stress test the slicing logic of `pipe_read_file` against valid, invalid, and inverted ranges.
*   **Status**: ✅ **Verified**. Proved bit-perfect extraction for valid ranges and graceful safety fallbacks for OOB/Inverted bounds.
*   **Proof**: [run_ranges_battle_test.log](scenarios/20-orchestrated-line-ranges/run_ranges_battle_test.log)

### Scenario 21: Rust Core Stress, Concurrency & Parity
*   **Last Verified In**: `v0.4.5`
*   **Objective**: Measure performance gains of the Rust orchestrator and verify functional parity with the Python core across all scenarios.
*   **Status**: ✅ **Verified**. Rust achieved a **21.4x speedup** and reached **100%** functional parity across all 21 scenarios.
*   **Proof**: [run_parity_v3.log](scenarios/21-rust-core-performance/run_parity_v3.log)

---

## Conclusion
The `std-context-lab` successfully processed 21 comprehensive architectural and operational tests. All 21 claims are fully proven, and all identified bugs have been documented and/or resolved upstream. Every scenario now meets the **Verifiable Proof** standard with raw logs and structured evidence.
