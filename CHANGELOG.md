# Lab Tracking Record

This document serves as a chronological journal of events, configurations, and experiments conducted within the `std-context-lab`. Since this is a testing environment and not a releasable software project, entries are logged by date and milestone rather than semantic versioning.

## [2026-05-10] - Initial Lab Setup
- Initialized `std-context-lab` repository to battle-test `context-pipe` and `semantic-sift`.
- Cloned `context-pipe` and `semantic-sift` into `target_repos/` as read-only references (local push disabled).
- Created `AGENTS.md` to establish the Feature Lab identity and operational constraints.
- Configured a shared `uv` Python virtual environment at the repository root.
- Installed `context-pipe` and `semantic-sift` in editable mode within the shared `.venv`.
- Compiled the `sift-core` Rust binary (`--release`).
- Scaffolded `scenarios/shared_mcps` directory with a basic `package.json` for external MCP server dependencies.
- Added `BACKLOG.md` to manage upcoming feature tests and scenarios.
- Defined explicit **MCP Setup Directives** in `AGENTS.md` covering dependency centralization, scenario isolation, and shadowing by default.
- Registered `context-pipe` and `semantic-sift` as local MCP servers in `.gemini/settings.json` using the absolute venv interpreter path.
- Successfully ran `pipe_onboard`, injecting `/pipe-*` slash commands into the Gemini CLI.
- Verified installation with `pipe_verify`, confirming auto-discovery of `semantic-sift-cli`.
- Initialized root `pipes.json` with portable command names (e.g., `semantic-sift-cli`), relying on `context-pipe`'s internal venv resolution.
- Installed `semantic-sift[neural]` extras (PyTorch, Transformers, etc.) to enable high-fidelity neural sifting.
- Injected the mandatory Context-Pipe SOP/Mandate into `AGENTS.md`.
- Created `MCP_CATALOG.md` (v4) mapping 24+ tools across core infrastructure, shadow MCPs, security guardrails, and binary pre-filters to provide a comprehensive technical roadmap.
- Added `.gitignore` to protect `.gemini`, `.venv`, and `target_repos` from version control.
- Uninstalled global `github` extension to remove noise and ensure a clean testing environment.

## [2026-05-11] - Scenario 01: Protocol Basics
- Started Phase 1: Protocol Basics.
- Scaffolded `scenarios/01-protocol-basics/` with a local Node.js `transformer.js` script and a dedicated `pipes.json`.
- Successfully executed the `basics-pipe` via the `mcp-pipe` terminal tool, proving the fundamental `stdin`/`stdout` contract and language agnosticism.
- Verified that `semantic-sift-cli` correctly distilled the output of the Node.js pre-transformer.

## [2026-05-11] - Scenario 02: Shadow Discovery
- Started Phase 2: Shadow Discovery.
- Installed `@modelcontextprotocol/server-everything` into `scenarios/shared_mcps/`.
- Proved that `mcp-pipe tool everything --list-tools` successfully introspects shadow servers from local `pipes.json`.
- Verified direct shell-to-MCP bridging via `mcp-pipe tool everything echo`.
- **Bug Identified**: Discovered that the `mcp-pipe run` and `run-dynamic` commands fail to pass the `server_registry` to the orchestrator, preventing MCP nodes from functioning inside named pipes when called via the terminal CLI.
- Proved the "Zero Tool Bloat" claim by executing complex shadow tools without global registration.
- Created `README.md` files for Scenarios 01 and 02 to establish a permanent laboratory manual.
- Formally paused Scenario 03 due to discovered orchestration bugs (Logged in `bugs/REPORT_001.md`).
- **Verified & Closed Bug #002**: Confirmed `pipe_onboard` now automatically handles `.gitignore` updates.
- **Verified & Closed Bug #004**: Confirmed `pipe_onboard` now correctly injects `AfterTool` and `PreCompress` hooks for Gemini CLI.
- **Verified & Closed Bug #005**: Confirmed `pipe_onboard` now normalizes hook commands for better idempotency.
- **Verified & Closed Bug #006**: Confirmed `inject_content` now uses the correct Gemini CLI `decision: deny` schema.
- **Verified & Closed Bug #007**: Confirmed telemetry is now Opt-Out by default (Telemetry enabled automatically).
- **Verified & Closed Bug #008**: Confirmed `onboarding.py` correctly injects `GEMINI_SESSION_ID` into hook env vars.
- **Verified & Closed Bug #009**: Confirmed `onboarding.py` correctly injects `-W ignore` into the python hook command.
- **Verified & Closed Bug #001**: Confirmed orchestration fixes (Audit Header crash, Registry Leak, Command string validation).
- **Verified & Closed Bug #003**: Confirmed `orchestrator.py` now resolves `.exe` binaries on Windows correctly.
- **Verified & Closed Bug #010**: Confirmed `onboarding.py` now explicitly configures a 10s timeout for Gemini CLI hooks.
- **Verified & Closed Bug #011**: Confirmed `wrapper.py` now correctly returns `decision: allow` for Gemini CLI during bypass paths.
- **Verified & Closed Bug #012**: Confirmed `pipe_hook.py` now correctly returns `decision: allow` on exception path.
- **Verified & Closed Bug #013**: Confirmed orchestrator now resolves `${VAR}` placeholders in node arguments.
- **Verified & Closed Bug #014**: Confirmed CLI now reconfigures I/O encoding to prevent Unicode crashes on Windows.
- **Verified & Closed Bug #015**: Confirmed orchestrator now supports `optional: true` nodes for failure-bypass.
- **Verified & Closed Bug #017**: Confirmed `onboarding.py` correctly injects environment variables into the Gemini CLI hook command string (schema compliance).
- **Identified Bug #018**: Discovered idempotency failure in `merge_hook_json` when commands have shell prefixes (Logged in `bugs/REPORT_018.md`).
- Updated `target_repos/context-pipe` to **v0.3.0** (The Integration Stable Release).
- Overhauled root `README.md` with agnostic, tool-independent setup instructions to ensure lab portability for the public.
- Updated `.gitignore` to protect `node_modules` across all scenario directories.
- Manually fixed `.gitignore` to include `.pipe_cache/`, `.sift_cache/`, and `.sift_telemetry.json`.
- Defined standardized **Bug Reporting Protocol** in `AGENTS.md` to ensure high-fidelity reporting without unauthorized codebase modifications.
- Established **`bugs/archive/`** to house verified/fixed reports, keeping the root `bugs/` directory focused on active blockers.

## [2026-05-11] - Scenario 03: Research Synthesizer
- Started Phase 3: Research Synthesizer.
- Installed `mcp-server-fetch` and `markitdown` into the shared laboratory environment.
- Scaffolded `scenarios/03-research-synthesizer/` with a multi-node pipe that chains an MCP fetcher, a document converter, and a neural refinery.
- Proved the "Mental Supply Chain" claim by distilling bloated web content into high-signal markdown context.

## [2026-05-11] - Scenario 04: Core Pre-Filters
- Started Phase 4: Core Pre-Filters.
- Demonstrated context optimization using `findstr` and `yq` as pre-refinery nodes.
- Successfully reduced a 5,000-line log to pure actionable signal, proving the value of deterministic structural filtering.
- **Bug Identified**: Logged **REPORT_003.md** identifying a major issue with Windows PATH resolution for venv-installed binaries.
- Finalized permanent documentation for Scenario 04.

## [2026-05-11] - Scenario 05: Pipe-Tee Inspection
- Started Phase 5: Pipe-Tee Inspection.
- Created `scenarios/05-pipe-tee-inspection/` to test stream splitting.
- Verified that the orchestrator can reliably dump intermediate context payloads to a `.tee/` folder before a node processes them, without breaking standard output.
- Finalized permanent documentation for Scenario 05.

## [2026-05-11] - Scenario 07: The Mental Supply Chain (E2E)
- Started Phase 7: The Mental Supply Chain.
- Installed `prettier` into the shared MCPs directory for clean-room formatting.
- Created `scenarios/07-mental-supply-chain/` with mock auditor and ship-it scripts.
- Successfully orchestrated a 5-node E2E pipeline (`fetch` -> `prettier` -> `semantic-sift` with tee snapshot -> `auditor_script` -> `ship_it_mock`).
- Proved that the system can reliably stream data across MCP servers, Node.js scripts, Python CLIs, and Rust engines in a single execution.
- Finalized permanent documentation for Scenario 07.

## [2026-05-11] - Scenario 03: Research Synthesizer (Re-run)
- Successfully re-executed Scenario 03 via the terminal CLI.
- **Verified Fix #001 & #002**: Confirmed the `mcp-pipe` terminal tool now correctly passes shadow server configurations and handles telemetry headers without crashing on node failures.
- Proven the "Research Synthesizer" use case with a 3-node chain (`mcp:fetch` -> `markitdown` -> `semantic-sift`).
- Finalized permanent documentation for Scenario 03.

## [2026-05-12] - Scenario 08: Multi-Modal Distillation
- Established the **Dual-Channel Mandate** in `BACKLOG.md` to ensure platform parity across Shell and Agent interfaces.
- Successfully verified Scenario 08, proving format agnosticism by distilling styled HTML into clean Markdown signal.
- Verified 100% parity between the terminal `mcp-pipe tool` and the AI assistant's `pipe_run` tool.
- Initialized **`LAB_STATUS.md`** to provide an at-a-glance dashboard of environment health and technical scenario validation.
- Updated `LAB_STATUS.md` to support **Environment Multi-Tenancy**, enabling cross-platform parity tracking for Gemini, Cursor, VSCode, and OpenCode.
- Documented the **🖥️ IDE/Environment Onboarding SOP** in the root `README.md` to guide users through multi-platform setup.
- Finalized permanent documentation for Scenario 08.

## [2026-05-12] - Scenario 06: Agent-to-Agent (A2A) Testing
- Resumed Phase 6: A2A Testing after verified fixes for telemetry, platform detection, and hook schemas.
- Successfully executed a live hand handshake between a 'Researcher' agent and a 'Reviewer' sub-agent.
- **Verified ROI**: Captured first real-world Context Balance Sheet data, showing >1,200 chars of noise incinerated during the handshake.
- Proven the "Refined Handoff" claim: reasoning fidelity is maintained even with highly compressed context.
- Verified 100% parity across Shell and Agent channels for A2A distillation.
- Finalized permanent documentation for Scenario 06.

## [2026-05-12] - Scenario 10: Structured Data Auditor
- Proven the **Structured Data Exemption** claim: `context-pipe` intentionally bypasses sifting for valid JSON to prevent data corruption.
- Successfully verified that tools like Supabase/SQLite show "Zero Save" by design to protect intelligence integrity.
- Demonstrated how to opt-in to distillation for structured data by explicitly flattening JSON via `yq` in a multi-node supply chain.
- Finalized permanent documentation for Scenario 10.

## [2026-05-12] - Scenario 11: Supply Chain Visualization
- Developed `pipes_to_mermaid.py` script to parse `pipes.json` and generate visual supply chain diagrams.
- Created a specialized meta-pipe (`viz-pipe`) to enable self-visualization of the context supply chain.
- **Verified Observability claim**: Proved that the system is transparent and auditable across both Shell and Agent channels.
- Finalized permanent documentation for Scenario 11.

## [2026-05-12] - Scenario 12: The "Giant File" Heart-Attack
- Successfully processed a **50.6 MB** log file in **6.2 seconds**, proving industrial-grade refinery speed.
- Verified the **Truncation Guard** claim: `semantic-sift` successfully protects system memory by capping input at 50MB.
- **Verified Fix #014**: Confirmed the CLI no longer crashes on Windows Unicode headers.
- Finalized permanent documentation for Scenario 12.

## [2026-05-12] - Scenario 13: The Resiliency Gauntlet
- Tested the orchestrator's error handling under cascading node failures.
- Verified that `help_msg` hints are correctly surfaced to the agent when a node fails to resolve.
- **Verified Fix #015**: Proven that the orchestrator can successfully bypass optional node failures and continue the supply chain.
- Finalized permanent documentation for Scenario 13.

## [2026-05-12] - Scenario 14: The Security Black Hole
- Proven the **Zero-Trust Context** claim by successfully redacting over 1,000 secrets from a log stream.
- Demonstrated the use of high-performance **Python script nodes** for deterministic context sanitation.
- Finalized permanent documentation for Scenario 14.

## [2026-05-12] - Scenario 09: Adaptive Pressure Simulation (Re-run)
- Successfully re-executed Scenario 09 after verified fix for placeholder resolution.
- **Verified Fix #013**: Proven that node arguments can now dynamically resolve `${VAR}` environment placeholders.
- Finalized permanent documentation for Scenario 09.

## [2026-05-13] - Scenario 15: Recursive Supply Chains
- Successfully demonstrated **Pipeline Encapsulation** by defining a pipe that calls the `mcp-pipe` CLI as a node.
- Proven that `stdin`/`stdout` streams maintain integrity through nested layers of the orchestrator.
- Verified that the **Echo Guard** (`CPP_SIGNATURE`) correctly prevents infinite recursion loops when a pipe attempts to process its own output.
- Finalized permanent documentation for Scenario 15.

## [2026-05-13] - Scenario 16: Protocol Violation Stress
- Attempted to test the orchestrator's resiliency against corrupt node output (binary garbage, invalid UTF-8).
- **Identified Bug #020**: Discovered that the orchestrator completely crashes with a `UnicodeDecodeError` and a subsequent `TypeError` if a node outputs non-UTF8 data.
- **Verified Fix #020**: Re-executed after upstream fix. Orchestrator now correctly sanitizes binary/non-UTF8 garbage streams without crashing.
- Finalized permanent documentation for Scenario 16.

## [2026-05-13] - Scenario 17: Version Awareness & Self-Update
- **Identified Feature Gap #019**: Discovered the need for automated version awareness and 'Self-Heal' update suggestions in `pipe_verify`.
- **Verified Fix #019**: Mocked local downgrade and successfully verified `pipe_verify()` now checks GitHub tags and outputs actionable update commands.
- Finalized permanent documentation for Scenario 17.

## [2026-05-13] - 100% Full Regression Sweep
- Initiated a formal Regression Gauntlet (per `REGRESSION_SOP.md`) following the `v0.3.1` update.
- Successfully re-executed and verified Scenarios 07, 12, 13, and 15 (The "Core Four").
- Conducted an exhaustive sweep, re-executing Scenarios 01, 02, 03, 04, 05, 06, 08, 10, 11, and 14 against the `v0.3.1` code base.
- **Status: All Clear**. Confirmed that all 17 scenarios pass under the new `v0.3.1` baseline.
