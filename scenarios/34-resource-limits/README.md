# Scenario 34 — Resource Limits (Phase 6)
## Claim Under Test
The engine handles 100MB+ inputs without memory exhaustion, correctly reports throughput metrics, and completes in bounded time.
## Helper
`generate_load.py <size_mb>` — streams N MB of log-like text to stdout.
## Tests
| Test | Input | Expected |
|---|---|---|
| A | 100MB text | Completes, no OOM, reports reduction % |
| B | 10 rapid consecutive calls | All complete, no state leakage |
