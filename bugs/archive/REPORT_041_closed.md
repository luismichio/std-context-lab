# Report 041: `_run_mcp_node` Hangs from Module Context — Identical Logic Works as Standalone Function

**Date:** 2026-05-30 (v0.5.4)
**Scenario:** 27 — MCP Banner Tolerance (Phase 13)
**Status:** 🔴 Open

## Description

`_run_mcp_node()` in `orchestrator.py` hangs 100% of the time when called from within the module, even though the **exact same logic** completes successfully (~0.2s) when written as a standalone function. The hang occurs inside `async with stdio_client(server_params) as (read, write):` — the subprocess starts but nothing produces an `initialize` response.

This is **not** the same bug as REPORT_040 (encoding params). REPORT_040 is fixed in v0.5.4. The encoding fix is confirmed present in the source, and raw `stdio_client` + `_StdoutToleranceWrapper` + `ClientSession` tests pass. This is a separate, unresolved issue affecting full pipe execution.

## Root Cause

**Unknown.** Despite extensive debugging, the reason for the hang could not be identified.

What is known:
- `_run_mcp_node` is defined at line 244 of `orchestrator.py`
- The v0.5.4 source has all fixes (encoding params, async protocol)
- The `.pyc` cache confirms the compiled bytecode matches the source
- `StdioServerParameters` and `resolve_placeholders` imports are the same objects whether imported via `context_pipe.orchestrator` or `mcp.client.stdio` / `context_pipe.config_loader`
- The standalone replica (identical code, same imports) works instantly

Hypotheses (unconfirmed):
1. **Import-time side effect** — Something in `orchestrator.py`'s module-level code alters event loop behavior on Windows
2. **Windows pipe initialization race** — `ProactorEventLoop` subprocess pipe setup may race when the calling function is in a specific module
3. **`stdio_client` subprocess env interaction** — `get_env_with_venv_path()` prepends to PATH, which (combined with other env vars) may cause the Python subprocess to load a different `site-packages` with conflicting MCP SDK version

## Evidence / Reproduction

### Setup
- Windows 10/11
- `context-pipe v0.5.4` installed via `pip install -e target_repos/context-pipe`
- `mock_noisy_server.py` with `--banners 0` (clean server, no banners)

### Fails — calling `_run_mcp_node` from module:

```python
import asyncio, os
import context_pipe.orchestrator as o

async def test():
    result = await o._run_mcp_node(
        {"server": "es", "tool": "echo", "input_key": "text"},
        "hello",
        {"es": {"command": ".../python.exe",
                "args": ["...mock_noisy_server.py", "--banners", "0"],
                "verbose": False}},
        os.environ.copy(),
    )
# → HANGS inside stdio_client, no timeout raised for 20+ seconds
```

### Works — same logic as standalone function:

```python
import asyncio, os, shlex
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import ClientSession
from context_pipe.orchestrator import _StdoutToleranceWrapper, _extract_text
from context_pipe.config_loader import resolve_placeholders

async def my_run_mcp_node(node, stdin_data, server_registry, env):
    # ... identical code as _run_mcp_node ...
    server_params = StdioServerParameters(
        command=cmd[0], args=cmd[1:], env=child_env,
        encoding="utf-8", encoding_error_handler="replace",
    )
    async with stdio_client(server_params) as (read, write):
        read = _StdoutToleranceWrapper(read, verbose=False)
        async with ClientSession(read, write) as session:
            await session.initialize()
            # ... call_tool ...
# → Returns in ~0.2s every time
```

### Debug traces from instrumentation:

```
[DEBUG] _run_mcp_node called
[DEBUG] server keys=['clean-echo-server', ...]
[DEBUG] env has PATH: True
[DEBUG] env has SYSTEMROOT: True
[DEBUG] calling original...
# → Nothing after this — hangs inside stdio_client context manager
```

### What was tested (all fail when calling `_run_mcp_node`):
- `asyncio.wait_for(o._run_mcp_node(...), timeout=5)` → `TimeoutError` after 5s
- Monkey-patching `o._run_mcp_node` → replacement also hangs when called via `run_pipe`
- Calling via `run_pipe` (which passes `get_env_with_venv_path()` as env) → hangs
- Calling via `context-pipe run clean-mcp-pipe` → hangs
- Calling via `mcp-pipe run clean-mcp-pipe` (Rust binary v0.4.5) → hangs

## Impact

| Dimension | Impact |
|---|---|
| **Scope** | All pipes using `type: "mcp"` nodes — blocks S03, S07, S27 |
| **Severity** | 🔴 Major — MCP node pipes remain non-functional despite encoding fix |
| **Reproducibility** | 100% on this Windows environment |
| **Workaround** | None for full pipe execution; raw MCP client test works as proof of concept |

## Related
- `context_pipe/orchestrator.py` line 244+ (`_run_mcp_node` function)
- `context_pipe/orchestrator.py` line 145 (`run_pipe` calls `_run_mcp_node`)
- Context-Pipe v0.5.4
- REPORT_037 (async protocol) — fixed, not related
- REPORT_040 (encoding params) — fixed, not related
- Scenario 27 — MCP Banner Tolerance
