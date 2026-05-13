# Lab Status Dashboard

This document tracks technical scenario validation across all target environments. It uses explicit version numbers to prevent "regression drift" and ensure absolute transparency about what code was tested where.

---

## 🏗️ Environment Health (Foundation)

| Component | Status | Verified On | Note |
| :--- | :---: | :--- | :--- |
| **Python Venv** | ✅ | 2026-05-13 | Master venv shared by all environments. |
| **Rust sidecar** | ✅ | 2026-05-13 | Compiled for high-performance heuristic sifting. |
| **`context-pipe`** | `v0.3.1` | 2026-05-13 | Orchestrator installed and active. |
| **`semantic-sift`** | `v0.3.1` | 2026-05-13 | Refinery kernel installed and active. |
| **Telemetry (ROI)** | `v0.3.1` | 2026-05-13 | Accounting active (Verified fix #007). |

---

## 🧪 Cross-Platform Parity Matrix

**Rule of Honesty:** A cell MUST contain the exact upstream version string (e.g., `v0.3.1`) that was empirically executed and verified in that specific environment. Do NOT use generic checkmarks. If a scenario is untested in a specific environment/version combination, it remains blank or shows the older verified version.

| Scenario | Claim Proved | Shell | Gemini | Cursor | VSCode | OpenCode |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **01: Basics** | Protocol Fidelity | `v0.3.1` | `v0.3.1` | `-` | `-` | `-` |
| **02: Shadow** | Zero Tool Bloat | `v0.3.1` | `v0.3.1` | `-` | `-` | `-` |
| **03: Synthesizer**| Multi-node Supply | `v0.3.1` | `v0.3.1` | `-` | `-` | `-` |
| **04: Pre-Filters** | Binary Pre-Sifting | `v0.3.1` | `v0.3.1` | `-` | `-` | `-` |
| **05: Pipe-Tee** | Non-breaking Audit | `v0.3.1` | `v0.3.1` | `-` | `-` | `-` |
| **06: A2A** | Handoff ROI | `v0.3.1` | `v0.3.1` | `-` | `-` | `-` |
| **07: Flagship** | Full Supply Chain | `v0.3.1` | `v0.3.1` | `-` | `-` | `-` |
| **08: Multi-Modal**| Format Agnosticism | `v0.3.1` | `v0.3.1` | `-` | `-` | `-` |
| **09: Pressure** | Adaptive Signaling | `v0.3.1` | `v0.3.1` | `-` | `-` | `-` |
| **10: Auditor** | Structured Data | `v0.3.1` | `v0.3.1` | `-` | `-` | `-` |
| **11: Visualizer** | Observability | `v0.3.1` | `v0.3.1` | `-` | `-` | `-` |
| **12: Big File** | Stream Stability | `v0.3.1` | `v0.3.1` | `-` | `-` | `-` |
| **13: Fallback** | Resilience Gauntlet| `v0.3.1` | `v0.3.1` | `-` | `-` | `-` |
| **14: Scrubber** | PII/Secret Redaction| `v0.3.1` | `v0.3.1` | `-` | `-` | `-` |
| **15: Recursive** | Chained Supply Chain| `v0.3.1` | `v0.3.1` | `-` | `-` | `-` |
| **16: Corruption** | Stream Integrity | `v0.3.1` | `v0.3.1` | `-` | `-` | `-` |
| **17: Awareness** | Self-Heal Updates | `v0.3.1` | `v0.3.1` | `-` | `-` | `-` |

**Legend:**
- `vX.Y.Z` **Verified**: The scenario was explicitly executed and passed under this version.
- `❌ (vX.Y.Z)` **Failed**: The scenario was executed and failed under this version (see `/bugs`).
- `-` **Not Tested**: No execution data exists for this environment.

---

## 🐞 Active Platform Blockers
Check the `bugs/` directory for full details on failures.

| Bug ID | Platform | Impact | Status |
| :--- | :--- | :--- | :--- |
| **None** | - | All 16 lab bugs and 1 feature request verified as resolved upstream for `v0.3.1` in Shell and Gemini. | 🟢 Clear |
