# Backlog

This document tracks upcoming tasks, feature scenarios, and tests for the `std-context-lab`. 

*Note: While there is no single strict standard for backlogs, this file uses a simple, prioritized list grouped by epic/scenario. Tasks should move from 'Later' -> 'Up Next' -> 'Done'.*

## 🎯 Dual-Channel Mandate
All technical claims MUST be verified via two channels to ensure platform parity:
1. **Shell Channel**: Using the `mcp-pipe` terminal tool (Pure Standard I/O).
2. **Agent Channel**: Using the AI assistant's MCP tools (IDE/Client Integration).

## 🎯 Up Next (Phase 2: Operational Hardening)
## 📅 Later (Future Explorations)

### IDE Integration Parity
- [ ] Test scenario execution within Cursor.
- [ ] Test scenario execution within OpenCode.
- [ ] Test scenario execution within VSCode.

## ✅ Done

- [x] Scenario 16: Protocol Violation Stress
    - [x] Built a "Bad Actor" node that outputs binary garbage.
    - [x] Identified **Bug #020**: Protocol Violation Crash (Non-UTF8 Stream).
    - [x] Marked "Stream Integrity" claim as UNVERIFIED.
- [x] Scenario 15: Recursive Supply Chains
    - [x] Defined nested pipe architecture.
    - [x] Proven the "Encapsulation" claim.
    - [x] Verified Shell/Agent parity for recursive flows.
- [x] Scenario 13: The Resiliency Gauntlet
    - [x] Proven failure bypass via `optional: true` flag.
    - [x] Verified fix for **Bug #015** (Fail-Fast).
- [x] Scenario 09: Adaptive Pressure Simulation
    - [x] Proven dynamic argument resolution.
    - [x] Verified fix for **Bug #013** (Placeholder resolution).
- [x] Scenario 12: The "Giant File" Heart-Attack
    - [x] Successfully processed 50MB via Rust sidecar in 6.2s.
    - [x] Verified fix for **Bug #014** (Unicode crash).
- [x] Scenario 14: The Security "Black Hole"
    - [x] Proven Zero-Trust context redaction.
- [x] Scenario 11: Supply Chain Visualization
    - [x] Proven the "System over Patch" (Observability) claim.
- [x] Scenario 10: The Structured Data Auditor
    - [x] Proven the "Structured Data Exemption" (Automatic JSON bypass).
- [x] Scenario 06: Agent-to-Agent (A2A) Testing
    - [x] Proven Refined Handoff ROI via sub-agent handshake.
    - [x] Verified fix for **Bug #007** (Silent Telemetry).
- [x] Scenario 08: Multi-Modal Distillation
    - [x] Proved format agnosticism using `markitdown` pre-refinery node.
- [x] Scenario 03: Research Synthesizer
    - [x] Successfully re-executed and verified CLI registry fix.
- [x] Scenario 07: The Mental Supply Chain (E2E)
    - [x] Prove the full Context-Pipe Vision by delivering an orchestrated multi-node flow.
- [x] Scenario 05: Pipe-Tee Inspection
    - [x] Proved T-Pipe stream splitting works.
- [x] Scenario 04: Core Pre-Filters (`jq` / `rg` / `findstr`)
    - [x] Proved massive context reduction using deterministic binaries.
- [x] Scenario 02: Shadow Discovery (`@modelcontextprotocol/server-everything`)
    - [x] Discovered shadow tools using `mcp-pipe tool --list-tools`.
- [x] Scenario 01: Protocol Basics (`lab-mock-transformer` + `semantic-sift`)
    - [x] Proved multi-language orchestration (Node.js -> Python/Rust).
- [x] Establish root project identity and `AGENTS.md`.
- [x] Define explicit MCP Setup Directives in `AGENTS.md`.
- [x] Configure local MCP server registration in `.gemini/settings.json`.
- [x] Run `pipe_onboard` and verify installation with `pipe_verify`.
- [x] Initialize root `pipes.json` with portable command names.
- [x] Configure shared `uv` environment with `neural` extras.
- [x] Compile Rust sidecar (`sift-core`).
- [x] Scaffold shared MCP directory.
- [x] Create `MCP_CATALOG.md` (v4).