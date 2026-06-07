# REPORT_044 — Rust parity harness false failures on Windows due to subprocess decoding and stale test commands

**Date**: 2026-06-02
**Scenario**: 21 - Rust Core Performance
**Status**: ✅ Closed (2026-06-07)
**Target Repo**: std-context-lab
**Priority**: Medium - regression signal quality compromised

---

## Description

The parity harness used in Scenario 21 can still report failures that are not actual engine regressions because parts of the hardcoded command matrix are stale relative to current scenario configs.

The original decode instability on Windows has been fixed, but stale scenario commands still produce misleading failure signals.

---

## Root Cause

1. Fixed issue: subprocess decoding is hardened with `encoding="utf-8", errors="replace"`.
2. Fixed issue: stale hardcoded tests were replaced with a matrix-driven harness sourced from `parity_matrix.json`.

---

## Evidence/Reproduction

### Run command
```powershell
cd scenarios/21-rust-core-performance
..\..\.venv\Scripts\python.exe parity_v3.py
```

### Observed output excerpts (post-fix)
```text
Native Parity Test: 04: Core Pre-Filters
Command: Get-Content noisy_app.log -Raw | mcp-pipe run log-optimizer --config pipes.json
Exit Code: 0
[PASS]: Native parity maintained.
```

### Relevant source
- Matrix-driven command source in [scenarios/21-rust-core-performance/parity_matrix.json](scenarios/21-rust-core-performance/parity_matrix.json)
- Refactored harness in [scenarios/21-rust-core-performance/parity_v3.py](scenarios/21-rust-core-performance/parity_v3.py)

---

## Impact

- Scenario 21 can be marked partial/fail for harness reasons rather than engine behavior.
- Parity trend data becomes less trustworthy.
- Investigation time increases because failures need manual triage.

---

## Proposed Fix

1. Refresh Scenario 21 command matrix from per-scenario README/pipes config rather than hardcoded stale commands.
2. Keep explicit failure labels:
- `HARNESS_ERROR` for harness/decode/config script issues
- `ENGINE_REGRESSION` only when the same test fails with a clean harness path.

---

## Acceptance Criteria

- Scenario 21 run has no decode exceptions on Windows. ✅
- Shadow Discovery subtest uses a current valid command. ✅
- Core Pre-Filters subtest uses current scenario command (`log-optimizer`) instead of stale `noisy-filter`. ✅
- Harness output distinguishes harness failures from engine failures. ✅

---

## Verification Update (2026-06-07)

Re-ran the original harness command:

```powershell
cd scenarios/21-rust-core-performance
..\..\.venv\Scripts\python.exe parity_v3.py
```

Observed behavior after the fix set:

- ✅ No `UnicodeDecodeError` during harness execution (decode hardening works).
- ✅ Scenario 02 command has been updated (`mcp-pipe tool everything --list-tools`).
- ✅ Scenario 04 command now uses `log-optimizer` and passes.
- ✅ Harness emits explicit labels: `PASS`, `KNOWN_GAP`, `ENGINE_REGRESSION`, `HARNESS_ERROR`.

Conclusion: report issue is resolved. Remaining non-zero test(s), if present, are now correctly attributed as engine parity behavior rather than harness drift.
