# Report 040: Missing `encoding` Params on `StdioServerParameters` — `UnicodeDecodeError` on Windows Banner Lines

**Date:** 2026-05-30
**Scenario:** 27 — MCP Banner Tolerance (Phase 13)
**Status:** 🔴 Open

## Description
On Windows, `StdioServerParameters` omits the `encoding` and `encoding_error_handler` parameters. When an MCP server emits non-UTF8 banner bytes on stdout (e.g., the `\x97` em-dash byte), the MCP SDK's internal `TextReceiveStream` decoder crashes with `UnicodeDecodeError` instead of gracefully handling the character.

The error manifests as validation failures when the `stdout_reader` task attempts to parse the mangled line as JSONRPC:

```
Failed to parse JSONRPC message from server
Invalid JSON: expected value at line 1 column 1
input_value='Mock MCP Server v1.0 \ufffd banner line 1\r'
```

The `\ufffd` replacement character indicates that `TextReceiveStream` already tried `utf-8` decoding and substituted the replacement character — but `model_validate_json` then rejects it as invalid JSON.

## Root Cause
In `context_pipe/orchestrator.py`, `_run_mcp_node` creates a `StdioServerParameters` without `encoding` or `encoding_error_handler`:

```python
# Current code (orchestrator.py ~line 294)
server_params = StdioServerParameters(
    command=cmd[0],
    args=cmd[1:],
    env=child_env,
)
```

The MCP SDK's `StdioServerParameters` passes these directly to `open_process` → `asyncio.create_subprocess_exec`. On Windows, the default encoding for `StreamReader` is locale-dependent (typically `cp1252`), and there's no `encoding_error_handler`, so non-ASCII bytes in banner lines can cause decode errors.

## Evidence / Reproduction

### Prerequisites
- Windows OS
- An MCP server that prints non-UTF8 banner lines to stdout before entering JSONRPC mode
- `context-pipe v0.5.3` (or any version using `_StdoutToleranceWrapper`)

### Reproduction
```bash
# Run the mock noisy server with banners containing non-UTF8 bytes
echo "test" | mcp-pipe run clean-mcp-pipe --config scenarios/27-mcp-banner-tolerance/pipes.json

# Output (truncated):
# Failed to parse JSONRPC message from server
# Invalid JSON: expected value at line 1 column 1
# input_value='Mock MCP Server v1.0 \ufffd banner line 1\r'
```

### Raw test showing the fix works
When `encoding='utf-8'` and `encoding_error_handler='replace'` are passed to `StdioServerParameters`, the banner tolerance code works correctly:

```python
params = StdioServerParameters(
    command=cmd[0],
    args=cmd[1:],
    env=child_env,
    encoding='utf-8',
    encoding_error_handler='replace',
)
async with stdio_client(params) as (read, write):
    read = _StdoutToleranceWrapper(read, verbose=False)
    async with ClientSession(read, write) as session:
        await session.initialize()
        result = await session.call_tool('echo', {'text': 'hi'})
        # SUCCESS: TextContent(text='[ECHO] hi')
```

## Impact
| Dimension | Impact |
|---|---|
| **Scope** | All MCP server pipes on **Windows** where the server emits non-UTF8 characters in banner lines |
| **Severity** | ⚠️ Moderate — only affects servers with non-UTF8 banner output on Windows |
| **Workaround** | Ensure MCP servers emit only ASCII/UTF-8 on stdout, or wrap server output in a UTF-8 encoder |

## Fix (for maintainers)
Add `encoding` and `encoding_error_handler` to the `StdioServerParameters` constructor in `context_pipe/orchestrator.py` `_run_mcp_node`:

```python
server_params = StdioServerParameters(
    command=cmd[0],
    args=cmd[1:],
    env=child_env,
    encoding='utf-8',
    encoding_error_handler='replace',
)
```

## Related
- `context_pipe/orchestrator.py` ~line 294 (`_run_mcp_node` `StdioServerParameters`)
- Scenario 27 — MCP Banner Tolerance
- MCP SDK `stdio_client` → `StreamReader` → `TextReceiveStream`
