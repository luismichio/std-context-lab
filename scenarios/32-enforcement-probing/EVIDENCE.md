# Scenario 32 — Evidence: Enforcement Probing

**Date:** 2026-05-31 | **Status:** ✅ PASS (with documented gap) | **Baseline:** `context-pipe v0.5.7`

## Test A — `read` on 50,000-byte file
`read` → passes through natively ✅ (under threshold)

## Test B — `read` on 51,201-byte file
`read` → `File is 50.0KB. Use pipe_read_file(...) instead.` ✅ Blocked.

## Test C — `bash head` on 51,201-byte file (known back door)
```bash
head -3 over_threshold.txt
```
**stdout:** `XXXXXXX...` (file content) ⚠️ **Back door confirmed.**
The `bash` tool is not intercepted. This is a documented, intentional gap — intercepting bash would break `git`, `npm`, `python`, and all test commands.

## Test D — `pipe_read_file` on large file
`pipe_read_file("...giant_heart_attack.log")` → routed through `standard-distill` pipe engine ✅

## Summary
| Gate | Status |
|---|---|
| `read` tool | ✅ Blocks > 51200 bytes |
| `bash` tool | ⚠️ Open back door (documented, by design) |
| `pipe_read_file` | ✅ Routes through engine correctly |
