# Evidence: Scenario 18 — Autonomous Dynamic Sifting

**Date:** 2026-05-31 | **Status:** ✅ PASS | **Baseline:** `context-pipe v0.5.7`

## Fix Applied
**Windows drift:** Original command used `grep` (not on Windows PATH). Updated to `rg` (ripgrep).
**Log drift:** `needle_in_haystack.log` regenerated — needle is `FATAL_ERROR_CODE_9942`, not the string "needle".

## Test — JIT dynamic graph: rg filter → semantic sift
```bash
cd scenarios/18-autonomous-dynamic-sifting
python generate_haystack.py  # regenerate 150,000-line haystack
mcp-pipe run-dynamic '[{"cmd":"rg","args":["FATAL_ERROR"]},{"cmd":"semantic-sift-cli","args":["semantic"]}]' --input_file needle_in_haystack.log --allow_shell
```
**stdout:**
```
--- [Semantic-Sift Audit] ---
📊 Reduction: -48.7% (0.1KB -> 0.2KB)
🛡️ Guard: Trace-Verified (No Echo)
⚡ Latency: 15.7ms
-----------------------------
[2026-05-13 14:22] CRITICAL: FATAL_ERROR_CODE_9942 - Database connection completely dropped by peer at pool_id=14.
```
✅ JIT graph assembled and executed. 1 needle extracted from 150,000 lines without modifying `pipes.json`.

## Phase 11 Parity via run-dynamic (previously verified 2026-05-30)
`type:"validator"`, `condition`, `id`+`next` all work in `run-dynamic` — node schemas pass through unmodified to `run_pipe`.
