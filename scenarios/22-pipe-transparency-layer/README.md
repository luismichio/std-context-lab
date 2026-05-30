# Scenario 22 — Pipe Transparency Layer (Phase 9)

## Claim Under Test
Real-time `[PIPE]` log lines are emitted to `stderr` during node execution when a `logging` block is declared in the pipe definition. Logs are configurable per-pipe via `compact` and `verbose` levels and via env var fallback.

## Feature Reference
- `context_pipe/orchestrator.py` — `_emit_pipe_log()` private function
- `logging` block in `pipes.json` per-pipe definition
- Env var fallback: `PIPE_LOG_LEVEL`, `PIPE_LOG_PREFIX`
- Rust parity: `crates/cpipe/src/orchestrator.rs`

## What to Verify

### Test A — Compact logging
Run `mcp-pipe run transparent-compact` and confirm `stderr` emits one `[PIPE] ✔` exit line per node (node name + char counts + latency). No entry line.

### Test B — Verbose logging
Run `mcp-pipe run transparent-verbose` and confirm `stderr` emits both entry (`[PIPE] → node`) and exit (`[PIPE] ✔ node | N → M chars | Xs`) lines per node.

### Test C — Custom prefix
Run `mcp-pipe run custom-prefix-pipe` and confirm the `[XPIPE]` prefix overrides the default `[PIPE]` prefix.

### Test D — Env var fallback
Set `PIPE_LOG_LEVEL=compact` and run a pipe with no `logging` block. Confirm logs appear via env var.

### Test E — Per-pipe wins over env var
Set `PIPE_LOG_LEVEL=compact`, run `transparent-verbose`. Confirm verbose wins (pipe definition overrides env var).

### Test F — No logging block, no env var
Run `mcp-pipe run standard-distill` with no env var set. Confirm zero `[PIPE]` lines on stderr.

### Test G — Rust parity
Run same pipes via `cpipe run <pipe>` and confirm identical `[PIPE]` log behaviour.

## Expected Artefact
`run_pipe_transparency.log`

## Dual-Channel Check
| Channel | Command |
|---|---|
| Shell | `mcp-pipe run transparent-compact < input.txt 2>stderr.log && cat stderr.log` |
| Agent | `pipe_run("transparent-compact", input_text)` — inspect audit header for logging evidence |
