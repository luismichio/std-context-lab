# Scenario 28 — Malformed Input Gauntlet (Phase 5)
## Claim Under Test
The sift engine must not crash, hang, or corrupt output on pathological inputs: empty stdin, binary data, 1MB single-line, invalid UTF-8, and large JSON blobs.
## Pipes
- `malformed-sift` — single `semantic-sift-cli semantic` node
## Tests
| Test | Input | Expected |
|---|---|---|
| A | Empty stdin | Silent (no output, no crash) |
| B | 1MB single line (no newlines) | Processes without hang |
| C | 10KB JSON blob | Passes through without structural corruption |
| D | Invalid UTF-8 bytes | Sanitised, no crash |
