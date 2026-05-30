# Scenario 27 — Evidence: MCP Banner Tolerance

**Date:** 2026-05-31 | **Status:** ✅ PASS (v0.5.5)

## Fix History

| Bug | Description | Fixed In |
| :--- | :--- | :--- |
| REPORT_037 | `_StdoutToleranceWrapper` missing async context manager protocol | v0.5.3 |
| REPORT_040 | `StdioServerParameters` missing encoding params on Windows | v0.5.4 |
| **REPORT_041** | `_run_mcp_node` hangs from module context (shlex posix=False + server_args) | **v0.5.5** |

## Test A — Silent banner skip (default)

```bash
echo "test" | mcp-pipe run banner-pipe --config pipes.json
```

**stdout:** `--- [Semantic-Sift Audit] ---` + `[ECHO] test`
**stderr:** `Failed to parse JSONRPC message` (3x — MCP SDK internal reader, cosmetic)

✅ Pipe executes successfully. No hang. Correct echo output.
⚠️ MCP SDK logs JSON parse warnings for each banner line on stderr (MCP SDK behavior, not context-pipe regression).

## Test B — Verbose banner surfacing

```bash
echo "test" | mcp-pipe run banner-verbose-pipe --config pipes.json
```

**stderr:** Contains 3 `[cpipe] MCP server stdout (non-JSON): ...` lines (verbose surfacing)
✅ Verbose mode surfaces banner-related entries on stderr.

## Test C — 50-line safety limit

Not retested on v0.5.5 — mock server currently emits 3 banners. Need `mock_noisy_server.py` configured for 51+ lines.

## Test D — Clean server (no banner)

Not retested on v0.5.5 — banner-free MCP setup needs verification.

## Summary

**REPORT_041 is confirmed fixed.** The MCP node no longer hangs. Banner tolerance works in the sense that:
- The pipe completes successfully with correct output
- The MCP SDK logs parse warnings for non-JSON banner lines but recovers
- Verbose mode surfaces banner-related entries via `[cpipe]` prefix

The MCP SDK's own `stdout_reader` logs `Failed to parse JSONRPC message` for each banner line — this is cosmetic noise from the SDK layer below the `_StdoutToleranceWrapper`. The pipe succeeds regardless.
