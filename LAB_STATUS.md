# Lab Status Dashboard

This document tracks technical scenario validation across all target environments. It uses explicit version numbers to prevent "regression drift" and ensure absolute transparency about what code was tested when.

**Baseline**: `context-pipe v0.5.7` | `semantic-sift v0.3.5`

## 🏁 Cross-Platform Parity Matrix
Verified success across primary agent channels. Evidence for every cell is stored in the `scenarios/` directory.

| Scenario ID | Feature / Claim | Shell (CLI) | Gemini CLI | pi.dev | Proof Artifact |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **01** | Protocol Basics (StdIO) | ✅ | ✅ | ✅ | `run_basics.log` |
| **02** | Shadow Discovery (Zero-Bloat) | ✅ | ✅ | ✅ | `run_shadow_discovery.log` |
| **03** | Research Synthesizer | ✅ | ✅ | ✅ | `run_research_synthesizer.log` |
| **04** | Core Pre-Filters (rg/jq) | ✅ | ✅ | ✅ | `run_core_prefilters.log` |
| **05** | Pipe-Tee Inspection | ✅ | ✅ | ✅ | `run_tee.log` |
| **06** | A2A Handoff ROI | ✅ | ✅ | ✅ | `run_a2a_handoff.log` |
| **07** | Mental Supply Chain (E2E) | ✅ | ✅ | ✅ | `run_mental_supply_chain.log` |
| **08** | Multi-Modal (HTML/PDF) | ✅ | ✅ | ✅ | `run_multi_modal_distillation.log` |
| **09** | Adaptive Pressure ($VAR) | ✅ | ✅ | ✅ | `run_adaptive_pressure.log` |
| **10** | Structured Data Exemption | ✅ | ✅ | ✅ | `run_structured_data_auditor.log` |
| **11** | Observability (Mermaid) | ✅ | ✅ | ✅ | `run_observability_viz.log` |
| **12** | Giant File Heart-Attack | ✅ | ✅ | ✅ | `run_giant_file_heart_attack.log` |
| **13** | Resiliency Gauntlet | ✅ | ✅ | ✅ | `run_resiliency_gauntlet.log` |
| **14** | Security Black Hole (PII) | ✅ | ✅ | ✅ | `run_security_black_hole.log` |
| **15** | Recursive Supply Chains | ✅ | ✅ | ✅ | `run_recursive_supply_chains.log` |
| **16** | Protocol Violation Stress | ✅ | ✅ | ✅ | `run_protocol_violation_stress.log` |
| **17** | Version Awareness | ✅ | ✅ | ✅ | `run_version_awareness.log` |
| **18** | Autonomous Dynamic Sifting | ✅ | ✅ | ✅ | `run_autonomous_dynamic_sifting.log` |
| **19** | Proactive Gating (BeforeTool) | ✅ | ✅ | ✅ | `run_gating_battle_test.log` |
| **20** | Line Range Precision | ✅ | ✅ | ✅ | `run_ranges_battle_test.log` |
| **21** | Rust Core Performance | ✅ | ✅ | ✅ | `run_parity_v2.log` |
| **22** | Pipe Transparency Layer (Phase 9) | ✅ | ⏳ | ✅ | `run_pipe_transparency.log` |
| **23** | Conditional Branching — `condition` predicates (Phase 11A) | ✅ | ⏳ | ✅ | `run_conditional_branching.log` |
| **24** | DAG Validator Nodes + Loop Guard (Phase 11B/C) | ✅ | ⏳ | ✅ | `run_dag_validator.log` |
| **25** | Runtime Variable Injection — `--var` (Phase 12A) | ✅ | ⏳ | ✅ | `run_runtime_variables.log` |
| **26** | Run Manifests — `--manifest` / `auto` (Phase 12B) | ✅ | ⏳ | ✅ | `run_manifests.log` |
| **27** | MCP Banner Tolerance (Phase 13) | ✅ | ⏳ | ✅ | `run_mcp_banner_tolerance.log` |

**Legend:** ✅ Verified │ ⚠️ Partial (infra drift, not engine regression) │ ❌ Hard fail │ ⏳ Pending

> **Shell (CLI)** and **pi.dev** results for scenarios 01–21 are from the 2026-05-30 regression run (v0.5.2); scenarios 22–27 re-verified on 2026-05-31 (v0.5.5). Gemini CLI results for 01–21 are from the original v0.4.x run; 22–27 are pending a dedicated Gemini CLI pass.

---

## 🖥️ Environment Run History

Tracks the exact component versions active when each environment channel executed its test pass.

| Environment | Scenarios | `context-pipe` | `semantic-sift` | Date | Notes |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **Shell (CLI)** | 01–21 | `v0.5.2` | `v0.3.5` | 2026-05-30 | Regression run inside pi.dev session |
| **Shell (CLI)** | 22–27 | `v0.5.2` | `v0.3.5` | 2026-05-30 | First run, same session |
| **pi.dev** | 01–27 | `v0.5.2` | `v0.3.5` | 2026-05-30 | Same session as Shell — `bash` tool runs inside pi.dev |
| **Shell (CLI)** | 27 (re-verify) | `v0.5.5` | `v0.3.5` | 2026-05-31 | REPORT_041 fixed — S27 no longer hangs |
| **Gemini CLI** | 01–21 | `v0.4.3`–`v0.4.5` | `v0.3.2` | 2026-05-24 | Original validation pass |
| **Gemini CLI** | 22–27 | — | — | ⏳ Pending | Not yet run on Gemini CLI |

---

## 📦 Component Versioning (Latest Verified)
| Component | Version | Date | Note |
| :--- | :--- | :--- | :--- |
| **`context-pipe`** | `v0.5.7` | 2026-05-31 | Updated via lab_update.py — commit `ef0ea93` fixes REPORT_042 in `onboarding.py` template (all thresholds → 51200). |
| **`semantic-sift`** | `v0.3.5` | 2026-05-30 | Updated via lab_update.py. |
| **Telemetry (ROI)** | `v0.5.0` | 2026-05-30 | Updated with context-pipe. |

---

## 🐞 Active Bug Tracker (Open Only)
Refer to the `bugs/` directory for full details on failures.

| Bug ID | Platform | Impact | Status |
| :--- | :--- | :--- | :--- |
| **#024** | Universal | Hook Duplication & Idempotency failure. | ✅ Closed in v0.4.5 |
| **#026** | Rust | Parity regression (Config Fallback logic). | ✅ Closed in v0.4.5 |
| **#030** | Universal | Missing pi.dev integration. | ✅ Closed in v0.5.0 |
| **#033** | Universal / pi.dev | `_inject_pi()` template uses `"auto"` as pipe name — not a valid CLI pipe; `pipe_read_file` and auto-sift broken. | ✅ Closed in v0.5.1 |
| **#034** | Universal / pi.dev | `_inject_pi()` template `execute` handlers return raw string — pi expects `{ content: [...] }`; all tools crash with `Cannot read properties of undefined (reading 'some')`. | ✅ Closed in v0.5.2 |
| **#035** | Universal / pi.dev | `_inject_pi()` template — 5 remaining defects: `pipe_run_dynamic` shell injection, `pipe_analyze_file` reads full file, `execSync` 1MB maxBuffer, `tool_call` doesn’t block, missing `setStatus`. | ✅ Closed in v0.5.2 |
| **#037** | Universal | `_StdoutToleranceWrapper` missing `__aenter__`/`__aexit__` — ALL MCP node pipes broken since v0.5.0 (Phase 13 regression). | ✅ Closed in v0.5.3 |
| **#038** | Universal | Missing `${VAR}` not detected before node spawn — literal string passed to subprocess instead of fail-fast error. | ✅ Closed in v0.5.3 |

| **#039** | Universal | `node.get("timeout")` ignored by orchestrator — per-node `"timeout"` field in pipes.json silently ignored; only `PIPE_NODE_TIMEOUT_MS` env var respected. S13 timeout test was a false pass (`forever_sleep.py` never sleeps). | ✅ Closed in v0.5.3 |

| **#040** | Windows MCP | `StdioServerParameters` missing `encoding`/`encoding_error_handler` params on Windows — `UnicodeDecodeError` on non-UTF8 banner lines from MCP servers. Blocks S27 banner tolerance. | ✅ Closed in v0.5.4 |

| **#041** | Universal | `_run_mcp_node` hangs when called from module context; identical logic works as standalone function. Blocks all MCP node pipes in full pipe execution. | ✅ Closed in v0.5.5 |
| **#042** | pi.dev | `read` threshold in pi.dev extension is 1KB; Python hook uses 50KB. v0.5.6 changelog claims fix but `onboarding.py` template unchanged — false fix. | ✅ Closed in v0.5.7 |