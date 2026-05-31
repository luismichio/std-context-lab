# Scenario 32 — Enforcement Probing (Phase 6)
## Claim Under Test
The `read` tool enforcement correctly blocks at the 51200-byte threshold. The `bash` tool back door is a known, documented gap. `pipe_read_file` routes large files correctly through the sift engine.
## Tests
| Test | Method | File | Expected |
|---|---|---|---|
| A | `read` | 50,000 B | Pass |
| B | `read` | 51,201 B | Blocked → `pipe_read_file` |
| C | `bash head` | 51,201 B | **Passes (known back door)** |
| D | `pipe_read_file` | Large file | Routed through pipe engine |
## Known Gap
`bash` is a general-purpose execution environment and cannot be intercepted without breaking legitimate workflows (`git`, `npm`, test commands). The `read` tool is the semantic gate — `bash` is intentionally outside scope.
