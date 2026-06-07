# Backlog

This document tracks upcoming tasks, feature scenarios, and tests for the `std-context-lab`. 

*Note: While there is no single strict standard for backlogs, this file uses a simple, prioritized list grouped by epic/scenario. Tasks should move from 'Later' -> 'Up Next' -> 'Done'.*

## 🎯 Dual-Channel Mandate
All technical claims MUST be verified via two channels to ensure platform parity:
1. **Shell Channel**: Using the `mcp-pipe` terminal tool (Pure Standard I/O).
2. **Agent Channel**: Using the AI assistant's MCP tools (IDE/Client Integration).

## 🎯 Up Next (Phase 3: New Feature Validation — v0.5.0)

### Scenario 22: Pipe Transparency Layer (Phase 9)
- [x] Verify `logging` block in `pipes.json` emits `[PIPE]` lines to `stderr`.
- [x] Verify `compact` vs `verbose` log levels.
- [x] Verify custom prefix override.
- [x] Verify env var fallback (`PIPE_LOG_LEVEL`, `PIPE_LOG_PREFIX`).
- [x] Verify per-pipe wins over env var.
- [x] Verify Rust parity (`cpipe`).

### Scenario 23: Conditional Branching — `condition` Predicates (Phase 11A)
- [x] Verify `size:>N` and `size:<N` skip/execute logic.
- [x] Verify `artifact:missing` and `artifact:exists` predicates.
- [x] Verify `contains:<string>` predicate.
- [x] Verify unknown predicate fails-open (warn + run).
- [x] Verify Rust parity.

### Scenario 24: DAG Validator Nodes + Loop Guard (Phase 11B/C)
- [x] Verify `type: "validator"` routes by exit code to `branches`.
- [x] Verify `id` + `next` explicit DAG jumps (node skip).
- [x] Verify 100-step loop guard triggers with `--- [Context-Pipe: Loop Guard] ---`.
- [x] Verify `artifact-fork-pipe`: true two-route fork via validator (file exists → sift, file missing → create). Mutual exclusion confirmed.

### Scenario 25: Runtime Variable Injection (Phase 12A)
- [x] Verify `--var KEY=VALUE` substitution in `cmd` and `args`.
- [x] Verify pipe `vars` defaults block.
- [x] Verify caller `--var` overrides pipe default.
- [x] Verify missing variable fail-fast error.
- [x] Verify empty-default fail-fast works (positive path of REPORT_038 cap).
- [x] Verify `--manifest` + `--var` combined.
- [x] Verify `os.environ` fallback for undeclared vars.
- [ ] Verify agent channel via `pipe_run` vars param. (pending pi reload)

### Scenario 26: Run Manifests (Phase 12B)
- [x] Verify `--manifest <path>` creates JSON artifact with correct schema.
- [x] Verify manifest records `status: "fail"` for broken pipe.
- [x] Verify `"manifest": "auto"` generates `.pipe_cache/<name>-<iso>.json`.
- [x] Verify no manifest created by default.

### Scenario 27: MCP Banner Tolerance (Phase 13)
- [x] ALL TESTS UNBLOCKED → **REPORT_041** ✅ Closed in v0.5.5.`_run_mcp_node` no longer hangs. MCP SDK logs JSON parse warnings for banner lines but pipe completes successfully.

## 📅 Later (Future Explorations)

### IDE Integration Parity
- [ ] Test scenario execution within Cursor.
- [ ] Test scenario execution within OpenCode.
- [~] Test scenario execution within VSCode. (`.vscode/mcp.json` configured 2026-06-02 — test pass pending)

## ✅ Done

- [x] **REPORT_044 fix 2026-06-07**: `parity_v3.py` harness hardened — subprocess decode (`utf-8`+`replace`), stale Scenario 02 command updated, `[HARNESS_ERROR]` vs `[ENGINE_REGRESSION]` labels split.

- [x] **Gap tests 2026-05-30**: 
  - S13: Timeout via env var on required node; optional+condition interaction; discovered false pass in original timeout test (forever_sleep.py never sleeps); **filed REPORT_039** (node.timeout ignored by orchestrator)
  - S18: Verified run-dynamic supports Phase 11 features (validator, condition, id+next all work)
  - S24: Validator cycle loop guard (universal); nested validator in branch_sequences; two-route artifact fork
  - S25: Empty-default fail-fast (positive path of REPORT_038); manifest+var combined

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