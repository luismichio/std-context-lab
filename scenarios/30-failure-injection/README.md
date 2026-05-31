# Scenario 30 — Failure Injection (Phase 5)
## Claim Under Test
The orchestrator handles node failures correctly: empty output passes through silently, required node failures abort the pipe, optional failures are bypassed, and large stdout is processed without OOM.
## Pipes
- `empty-output-pipe` — node outputs nothing (exit 0)
- `required-fail-pipe` — required node exits 1
- `optional-fail-pipe` — optional node exits 1 → bypassed
- `flood-pipe` — node outputs 10MB
## Helper Scripts
- `empty_node.py` — reads stdin, outputs nothing, exits 0
- `fail_node.py` — exits 1 with stderr message
- `flood_node.py` — outputs 10MB of text lines
