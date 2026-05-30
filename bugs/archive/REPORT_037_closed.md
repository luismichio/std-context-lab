# Report 037: `_StdoutToleranceWrapper` Missing Async Context Manager Protocol — All MCP Nodes Broken

**Date:** 2026-05-30
**Scenario:** 27 — MCP Banner Tolerance (Phase 13)
**Status:** 🔴 Open

---

## Description

The Phase 13 banner tolerance feature (`_StdoutToleranceWrapper` in `context_pipe/orchestrator.py`) breaks **all** MCP node pipe execution. Any pipe containing a `type: "mcp"` node fails immediately with:

```
--- [Context-Pipe: MCP Unexpected Error] ---
unhandled errors in a TaskGroup (1 sub-exception)
```

The root cause is that `_StdoutToleranceWrapper` does not implement the async context manager protocol (`__aenter__`/`__aexit__`) required by the MCP SDK's `_receive_loop`.

---

## Root Cause

`_StdoutToleranceWrapper` is injected as the `read` stream in `_run_mcp_node()`:

```python
# context_pipe/orchestrator.py lines 288-290
read = _StdoutToleranceWrapper(read, verbose=False)
# or
read = _StdoutToleranceWrapper(read, verbose=True)
```

The class implements `receive()` and `aclose()` but is missing the async context manager dunder methods:

```python
class _StdoutToleranceWrapper:
    async def receive(self): ...     # ✅ present
    async def aclose(self): ...      # ✅ present
    # ❌ missing __aenter__
    # ❌ missing __aexit__
    # ❌ missing __aiter__ / __anext__
```

The MCP SDK's `ClientSession._receive_loop` (in `mcp/shared/session.py` line 353) uses `self._read_stream` as an **async context manager**:

```python
async with self._read_stream as stream:
    ...
```

Since `_StdoutToleranceWrapper` has no `__aenter__`/`__aexit__`, Python raises:

```
TypeError: '_StdoutToleranceWrapper' object does not support the asynchronous context manager protocol
```

This is caught by anyio's `TaskGroup.__aexit__` and re-raised as an `ExceptionGroup`, which context-pipe catches and returns as the `MCP Unexpected Error` message.

---

## Evidence / Reproduction

### Full traceback (extracted via direct `_run_mcp_node` call)

```
ExceptionGroup: unhandled errors in a TaskGroup (1 sub-exception)
  File "mcp/client/stdio/__init__.py", line 183, in stdio_client
    anyio.create_task_group() as tg,
  File "mcp/shared/session.py", line 353, in _receive_loop
    self._read_stream,
    ^^^^^^^^^^^^^^^^^
TypeError: '_StdoutToleranceWrapper' object does not support the asynchronous context manager protocol
```

### Reproduction

```bash
# Any pipe with a type:"mcp" node fails:
echo "test" | mcp-pipe run any-mcp-pipe --config pipes.json
# Output: --- [Context-Pipe: MCP Unexpected Error] ---
#         unhandled errors in a TaskGroup (1 sub-exception)
```

### Regression scope

This regression was introduced in v0.5.0 (Phase 13). **All MCP node pipes that worked before v0.5.0 are now broken.**

---

## Impact

| Dimension | Impact |
|---|---|
| **Scope** | ALL `type: "mcp"` node pipes — not just banner-emitting servers |
| **Regression** | Phase 13 broke a previously working feature (MCP nodes) |
| **Severity** | 🔴 Critical — `_StdoutToleranceWrapper` is unconditionally applied at line 288 |
| **Workaround** | None — cannot be bypassed by config |

---

## Fix (for maintainers)

Add `__aenter__`, `__aexit__`, `__aiter__`, and `__anext__` to `_StdoutToleranceWrapper` to delegate to the underlying stream:

```python
class _StdoutToleranceWrapper:
    async def __aenter__(self):
        await self._orig.__aenter__()
        return self

    async def __aexit__(self, *args):
        return await self._orig.__aexit__(*args)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return await self.receive()
        except anyio.EndOfStream:
            raise StopAsyncIteration
```

---

## Related

- `context_pipe/orchestrator.py` lines 198–225 (`_StdoutToleranceWrapper` class)
- `context_pipe/orchestrator.py` lines 285–295 (`_run_mcp_node` wrapper injection)
- Scenario 27 — MCP Banner Tolerance
- Phase 13 implementation (v0.5.0)
