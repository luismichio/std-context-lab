# Lab Status Dashboard

This document tracks technical scenario validation across all target environments. It uses explicit version numbers to prevent "regression drift" and ensure absolute transparency about what code was tested when.

**Baseline**: `context-pipe v0.4.5` | `semantic-sift v0.3.2`

## 🏁 Cross-Platform Parity Matrix
Verified success across primary agent channels. Evidence for every cell is stored in the `scenarios/` directory.

| Scenario ID | Feature / Claim | Shell (CLI) | Gemini CLI | Proof Artifact |
| :--- | :--- | :---: | :---: | :--- |
| **01** | Protocol Basics (StdIO) | ✅ | ✅ | `run_basics.log` |
| **02** | Shadow Discovery (Zero-Bloat) | ✅ | ✅ | `run_shadow_discovery.log` |
| **03** | Research Synthesizer | ✅ | ✅ | `run_research_synthesizer.log` |
| **04** | Core Pre-Filters (rg/jq) | ✅ | ✅ | `run_core_prefilters.log` |
| **05** | Pipe-Tee Inspection | ✅ | ✅ | `run_tee.log` |
| **06** | A2A Handoff ROI | ✅ | ✅ | `run_a2a_handoff.log` |
| **07** | Mental Supply Chain (E2E) | ✅ | ✅ | `run_mental_supply_chain.log` |
| **08** | Multi-Modal (HTML/PDF) | ✅ | ✅ | `run_multi_modal_distillation.log` |
| **09** | Adaptive Pressure ($VAR) | ✅ | ✅ | `run_adaptive_pressure.log` |
| **10** | Structured Data Exemption | ✅ | ✅ | `run_structured_data_auditor.log` |
| **11** | Observability (Mermaid) | ✅ | ✅ | `run_observability_viz.log` |
| **12** | Giant File Heart-Attack | ✅ | ✅ | `run_giant_file_heart_attack.log` |
| **13** | Resiliency Gauntlet | ✅ | ✅ | `run_resiliency_gauntlet.log` |
| **14** | Security Black Hole (PII) | ✅ | ✅ | `run_security_black_hole.log` |
| **15** | Recursive Supply Chains | ✅ | ✅ | `run_recursive_supply_chains.log` |
| **16** | Protocol Violation Stress | ✅ | ✅ | `run_protocol_violation_stress.log` |
| **17** | Version Awareness | ✅ | ✅ | `run_version_awareness.log` |
| **18** | Autonomous Dynamic Sifting | ✅ | ✅ | `run_autonomous_dynamic_sifting.log` |
| **19** | Proactive Gating (BeforeTool) | ✅ | ✅ | `run_gating_battle_test.log` |
| **20** | Line Range Precision | ✅ | ✅ | `run_ranges_battle_test.log` |
| **21** | Rust Core Performance | ✅ | ✅ | `run_parity_v2.log` |

---

## 📦 Component Versioning (Latest Verified)
| Component | Version | Date | Note |
| :--- | :--- | :--- | :--- |
| **`context-pipe`** | `v0.4.5` | 2026-05-24 | PowerShell fix verified (v0.4.5). Parity at 85.7%. |
| **`semantic-sift`** | `v0.3.2` | 2026-05-24 | Refinery kernel updated from source. |
| **Telemetry (ROI)** | `v0.4.5` | 2026-05-24 | Updated with context-pipe. |

---

## 🐞 Active Bug Tracker (Open Only)
Refer to the `bugs/` directory for full details on failures.

| Bug ID | Platform | Impact | Status |
| :--- | :--- | :--- | :--- |
| **#024** | Universal | Hook Duplication & Idempotency failure. | 🔴 Open (Follow-up) |
| **#026** | Rust | Parity regression (Config Fallback logic). | 🔴 Open (Partial Fix) |
