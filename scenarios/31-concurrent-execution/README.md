# Scenario 31 — Concurrent Execution (Phase 6)
## Claim Under Test
Multiple simultaneous `mcp-pipe` invocations against the same `pipes.json` must all complete successfully without race conditions, corruption, or deadlocks.
## Helper
`run_concurrent.py <n_workers> <pipe_name> <config>` — spawns N parallel subprocess invocations and reports results.
## Tests
| Test | Workers | Pipe | Expected |
|---|---|---|---|
| A | 5 | `concurrent-sift` | All 5 complete OK, no corruption |
| B | 10 | `concurrent-sift` | All 10 complete OK |
| C | 5 | `concurrent-tee` | All 5 write to same tee sink — no crash |
