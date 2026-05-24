# Bug Report 026: Functional Discrepancies in Rust Core (cpipe)

**Date:** 2026-05-24
**Scenario:** 21 - Full Protocol Parity Gauntlet
**Status:** Closed (Verified)

### Verification (2026-05-24)
Final Gauntlet v3 passed with 100% success. Verified that:
1. `cpipe` now supports backward compatibility for `tool list` and snake_case arguments (`--input_file`).
2. Config fallback issues were traced to an invalid local `pipes.json` (missing `cmd` fields). After restoring the config, the Rust engine showed bit-perfect functional parity with Python.


---

## 1. Protocol Regressions (CRITICAL)

### Description
The Full Protocol Parity gauntlet (Scenarios 01-20) revealed that the Rust binary (`cpipe`) is **not** a drop-in replacement for the standard Python orchestrator. While it provides a significant performance boost, it currently fails **83.3%** of established lab scenarios due to missing features and CLI discrepancies.

### Evidence (Full Gauntlet Results)
- **Scenarios Tested**: 18
- **Passed**: 3 (01, 02, 05)
- **Failed**: 15
- **Success Rate**: 16.7%

#### A. Missing Subcommands (Regression)
- **Issue**: `cpipe` does not implement the `handoff` or `verify` subcommands.
- **Impact**: Breaking Scenarios 06 and 17. Users cannot perform agent handoffs or system health checks using the Rust core.

#### B. Missing Arguments (Regression)
- **Issue**: `cpipe` does not support:
    - `--allow-shell` (Breaking Scenario 18 - Dynamic Sifting).
    - `--start-line` / `--end-line` (Breaking Scenario 20 - Line Ranges).
- **Impact**: Core "Advanced Sifting" capabilities are disabled in the Rust implementation.

#### C. Configuration Resolution Failure
- **Issue**: `cpipe` fails to locate pipes even when provided with a valid `--config` path (e.g., Scenario 04, 07, 08).
- **Root Cause**: The Python orchestrator has a more sophisticated configuration resolver that likely handles relative paths and multiple config sources more gracefully than the current Rust implementation.

---

## 2. Impact on Lab
The claim of "Functional Parity" for the Rust core is **REJECTED**. The Rust core is currently a high-performance **StdIO processing engine only** and lacks the CLI sophistication required for full protocol compliance.

### Recommended Fix
1.  **Sync CLI Schema**: Implement all missing subcommands (`handoff`, `verify`) and arguments (`--allow-shell`, `--start-line`, `--end-line`) in the Rust `cpipe` crate.
2.  **Robust Config Loading**: Port the Python config resolution logic to Rust to ensure pipes are found regardless of path complexity.
3.  **Snake_Case Support**: Support both snake_case and kebab-case for CLI arguments to ensure backward compatibility with existing Python-based automation.
