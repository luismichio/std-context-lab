# Regression Run — Scenarios 01–21
**Date:** 2026-05-30 | **Baseline:** context-pipe v0.5.2 | semantic-sift v0.3.5 | pi.dev (Shell channel)

---

## Results Matrix

| # | Scenario | v0.5.2 Shell | Notes |
|---|---|---|---|
| **01** | Protocol Basics | ✅ PASS | Must run from scenario dir (relative `transformer.js`) |
| **02** | Shadow Discovery | ✅ PASS | `list` discovers configured pipes + PATH tools |
| **03** | Research Synthesizer | ❌ FAIL | **Two blockers:** (1) `mcp-server-fetch.exe` not installed; (2) REPORT_037 (all MCP nodes broken) |
| **04** | Core Pre-Filters | ✅ PASS | 18.2% reduction on noisy log |
| **05** | Pipe-Tee Inspection | ✅ PASS | Tee file created in `.tee/`, sift ran on matched lines |
| **06** | A2A Handoff | ✅ PASS | `mcp-pipe handoff` works; telemetry write warning (pre-existing sift issue) |
| **07** | Mental Supply Chain | ❌ FAIL | **REPORT_037** — e2e-supply-chain contains `type:"mcp"` node |
| **08** | Multi-Modal Distillation | ✅ PASS | HTML → markitdown → sift pipeline works |
| **09** | Adaptive Pressure | ⚠️ PARTIAL | `adaptive-sift` pipe no longer in S01 pipes.json; core `${VAR}` substitution still works (confirmed via S25) |
| **10** | Structured Data Auditor | ⚠️ PARTIAL | `json-auditor` pipe no longer in S01 pipes.json; JSON bypass logic verified via root pipes.json |
| **11** | Observability Viz | ⚠️ PARTIAL | `pipes_to_mermaid.py` script-based; not re-run; no pipe changes that would affect it |
| **12** | Giant File Heart-Attack | ✅ PASS | 51MB processed in 6.9s, 100% reduction |
| **13** | Resiliency Gauntlet | ✅ PASS | `optional:true` bypass working |
| **14** | Security Black Hole | ✅ PASS | Must run from scenario dir (relative `pii_scrubber.py`) |
| **15** | Recursive Supply Chains | ⚠️ PARTIAL | `recursive-distill` pipe no longer in referenced pipes.json; basic recursion via chained sift still works |
| **16** | Protocol Violation Stress | ✅ PASS | `bad_actor.py` binary garbage handled without crash |
| **17** | Version Awareness | ✅ PASS | `mcp-pipe verify` reports correct versions |
| **18** | Autonomous Dynamic Sifting | ⚠️ PARTIAL | `grep` not on Windows PATH; **re-run with `rg` passes** (10MB, 2.9s) — scenario pipes.json needs updating |
| **19** | BeforeTool Gating | ✅ PASS | `wrap_payload()` (renamed from `wrap()`) returns `{"decision":"deny"}` for 51MB file |
| **20** | Line Range Precision | ✅ PASS | `--start-line`/`--end-line` slicing working |
| **21** | Rust Core Performance | ✅ PASS | `cpipe` processes input correctly |

---

## Regression Summary

| Category | Count |
|---|---|
| ✅ Full Pass | 13 |
| ⚠️ Partial (infra drift, not feature regression) | 5 |
| ❌ Hard Fail | 2 |

### Hard Failures (bugs)
- **S03, S07**: Blocked by **REPORT_037** (`_StdoutToleranceWrapper` missing async ctx mgr protocol — all MCP nodes broken)

### Infrastructure Drift (not regressions in the sifting engine)
- **S01, S14**: Require running from scenario directory (relative file paths in node `args`)
- **S09, S10, S15**: Referenced pipes (`adaptive-sift`, `json-auditor`, `recursive-distill`) no longer exist in the cross-referenced pipes.json — scenarios need their own pipes.json
- **S18**: `grep` not on Windows PATH — scenario hardcodes `grep`; should use `rg` on Windows

### API Change (not a regression failure)
- **S19**: `context_pipe.wrapper.wrap()` renamed to `wrap_payload()` in v0.5.x — test script updated in-place during run, now passes

---

## Action Items
1. **Fix REPORT_037** — restores S03 and S07
2. **Update S18 pipes / EVIDENCE** to use `rg` on Windows
3. **Add standalone pipes.json** to S09, S10, S15 — currently borrow from S01 which has changed
4. **Update S01, S14 pipes.json** to use absolute paths for node scripts (portability)
