# Scenario 27 — MCP Banner Tolerance (Phase 13)

## Claim Under Test
The Python and Rust engines gracefully skip up to 50 non-JSON stdout lines emitted by noisy MCP servers before JSON-RPC begins (banner tolerance). By default these lines are silently discarded. With `"verbose": true` on the server config, skipped lines are surfaced to `stderr`. A server emitting more than 50 non-JSON lines returns an error instead of hanging indefinitely.

## Feature Reference
- `context_pipe/orchestrator.py` — `_run_mcp_node()` stdout pre-filter
- `crates/cpipe/src/orchestrator.rs` — `read_jsonrpc_line(reader, max_skip)` helper
- `config_loader.py` / `config.rs` — `verbose: bool` on server config schema
- `pipes.json` — `"servers"` block with `"verbose": true`

## What to Verify

### Test A — Silent banner skip (default)
Configure `noisy-echo-server` (emits 3 banner lines before JSON-RPC). Run a pipe using an MCP node against it. Confirm:
- Pipe executes successfully
- **No** banner lines appear in stdout or stderr

### Test B — Verbose banner surfacing
Add `"verbose": true` to the server config. Re-run same pipe. Confirm:
- `stderr` contains `[cpipe] MCP server stdout (non-JSON): <banner text>` for each banner line
- Pipe still executes successfully

### Test C — 50-line safety limit
Configure `overflow-banner-server` (emits 51 non-JSON lines). Run pipe. Confirm:
- Execution does **not** hang indefinitely
- Returns a structured error after 51 lines (not a timeout crash)

### Test D — Clean server (no banner)
Configure a well-behaved MCP server (no banner). Confirm:
- Pipe executes normally
- Zero `[cpipe]` lines on stderr regardless of `verbose`

### Test E — Rust parity
Run Tests A and B via `cpipe run`. Confirm identical banner-skip and verbose behaviour.

## Test Infrastructure Notes
A minimal "noisy" MCP server is needed for this scenario. Use `mock_noisy_server.py` — a Python script that:
1. Prints N banner lines to stdout before JSON-RPC
2. Then behaves as a minimal MCP server (returns a fixed tool result)

See `mock_noisy_server.py` in this directory.

## Expected Artefact
`run_mcp_banner_tolerance.log`

## Dual-Channel Check
| Channel | Command |
|---|---|
| Shell | `mcp-pipe run banner-pipe < input.txt` |
| Agent | `pipe_run("banner-pipe", input_text)` |
