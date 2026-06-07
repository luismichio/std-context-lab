# REPORT_043 — context-pipe: Telemetry, Cache, and Stats are cwd-anchored — broken under VS Code multi-root workspaces

**Date**: 2026-06-02
**Scenario**: VS Code multi-root workspace (9 repos)
**Status**: ✅ Resolved (2026-06-07)
**Target Repo**: `context-pipe`
**Priority**: High — silent data corruption (cache), mixed telemetry, incorrect ROI reporting

---

## Description

Three separate but architecturally related components in `context-pipe` resolve their storage paths from `os.getcwd()` at **module import time** (server startup), not from the active project context at **call time**. In single-project IDEs (Gemini, OpenCode, Cursor, Antigravity), the server cwd always equals the active project root — so this works by accident. In VS Code multi-root workspaces, the server cwd is locked to the first workspace root at startup and never changes, causing all three components to operate on the wrong project for the lifetime of the session.

---

## Affected Components

### 1. `telemetry.py` — `_resolve_telemetry_path()` (line 14)

`TELEMETRY_FILE` is a **module-level constant** assigned once at import:

```python
TELEMETRY_FILE = _resolve_telemetry_path()  # line 35
```

`_resolve_telemetry_path()` walks `os.getcwd()` upward looking for `pipes.json` or `.pipe_identity`. In VS Code, cwd = workspace root #1 (e.g. `meechi-ai/`). All tool calls from all 9 workspace folders write telemetry to `meechi-ai/.pipe_telemetry.jsonl` — regardless of which project is active.

**Impact**: Telemetry is mixed across all projects with no project attribution. `get_pipe_stats()` returns aggregate ROI that cannot be broken down by project. Logs land in the wrong repo.

### 2. `orchestrator.py` — cache dir (lines 85, 383)

```python
cache_dir = os.path.join(os.getcwd(), ".pipe_cache")
```

Cache key is `pipe_name:node_index:content`. Two projects with identically named pipes (e.g. both define `"semantic-refinery"`) share a cache namespace. A cached result from project A with its node configuration can be served to project B which has a different node configuration for the same pipe name.

**Impact**: Silent wrong output. Project B receives distilled content processed through project A's pipe nodes. No error is raised — the cache hit is treated as valid.

### 3. `get_pipe_stats()` — Balance Sheet

Reads `TELEMETRY_FILE` (the same cwd-anchored file from #1). The Balance Sheet shown to the agent is an aggregate of all projects' activity with no project column or filter. ROI figures are meaningless in a multi-root context.

**Impact**: Agent reports inflated/deflated ROI. No way to know which project generated which savings.

---

## Root Cause

All three resolve paths from `os.getcwd()` — which is correct for single-project setups but wrong for multi-root. The fundamental assumption is: *server startup cwd = active project root*. This assumption breaks in VS Code (and will break in any IDE that runs one MCP server instance serving multiple workspace roots).

---

## Reproduction

1. Open a VS Code workspace with 2+ folders, each having a `pipes.json`
2. Register `context-pipe` once in User `settings.json` (global) with no `PIPE_CONFIG_PATH`
3. From folder B (not the first workspace root), call `pipe_run("semantic-refinery", "test")`
4. Observe: `.pipe_telemetry.jsonl` and `.pipe_cache/` are created in folder A (first root), not folder B

---

## Proposed Fix (Phase 5)

Introduce a `config_path` optional parameter to all tool handlers (`pipe_run`, `list_pipes`, `pipe_run_dynamic`, `get_pipe_stats`, etc.). When provided:

1. **Telemetry**: derive telemetry file path from `os.dirname(config_path)` at call time, not from `cwd` at import time. Pass the resolved path into `record_event()` rather than using the module constant.
2. **Cache**: scope cache dir to `os.path.join(os.dirname(config_path), ".pipe_cache")` and include a project fingerprint (hash of `config_path`) in the cache key to prevent cross-project collisions.
3. **`get_pipe_stats()`**: accept optional `config_path`; read the telemetry file from the corresponding project dir. Add a `project` field to telemetry entries for filtering.

`TELEMETRY_FILE` module constant should be kept as the fallback for backward compatibility (single-project setups where `config_path` is never passed).

---

## Workaround (Until Fix Ships)

Set `PIPE_CONFIG_PATH` in the server env (per-project `.vscode/mcp.json` or `.code-workspace`) and accept that only one project's `pipes.json` is active per VS Code session. Telemetry and cache will still be cwd-anchored but at least pipe resolution is correct.

See plan Phase 5 for full implementation spec.

---

## Verification Update (2026-06-07)

Current runtime includes lazy call-time resolution in `resolve_telemetry_file()` and project-scoped cache keying in `check_echo`.
Re-ran the default-path repro to confirm whether import-time anchoring still occurs.

### Reproduction result (default path)

```text
A= C:\Users\luism\Workbench\GitHub\meechi-ai\.pipe_telemetry.jsonl
B= C:\Users\luism\Workbench\GitHub\std-context-lab\.pipe_telemetry.jsonl
same= False
```

Interpretation: default call-time resolution now tracks active project context. The original import-time anchoring repro is no longer reproducible.
