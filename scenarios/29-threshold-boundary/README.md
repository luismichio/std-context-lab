# Scenario 29 — Threshold Boundary (Phase 5)
## Claim Under Test
The pi.dev `read` tool interception threshold is exactly 51200 bytes (50KB). Files at or below this size pass through natively. Files above are blocked and routed to `pipe_read_file`.
## Tests
| Test | File | Size | Expected |
|---|---|---|---|
| A | under_threshold.txt | 50,000 B | `read` passes through |
| B | at_threshold.txt | 51,200 B | `read` passes through (= not >) |
| C | over_threshold.txt | 51,201 B | `read` BLOCKED → `pipe_read_file` |
## Helper
`make_file.py <path> <size>` — creates a file with exactly N bytes.
