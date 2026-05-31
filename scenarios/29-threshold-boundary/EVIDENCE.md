# Scenario 29 — Evidence: Threshold Boundary

**Date:** 2026-05-31 | **Status:** ✅ PASS | **Baseline:** `context-pipe v0.5.7`

## Test A — 50,000 bytes (under threshold)
`read` on `under_threshold.txt` (50,000 B) → passes through natively ✅

## Test B — 51,200 bytes (at threshold, `size > 51200` is false)
`read` on `at_threshold.txt` (51,200 B) → passes through natively ✅
The condition is strictly `>`, so exactly 51200 bytes is NOT blocked.

## Test C — 51,201 bytes (over threshold)
`read` on `over_threshold.txt` (51,201 B):
```
File is 50.0KB. Use pipe_read_file("...over_threshold.txt") instead.
```
✅ Blocked. Message directs to `pipe_read_file`.

## Key Finding
Threshold is exclusive (`stats.size > 51200`). Files up to and including 51200 bytes pass natively. 51201+ bytes are blocked. The boundary is well-defined and consistent with Python's `wrapper.py` (also `> 51200`).
