# Report 030: Missing pi.dev Integration — No Extension, No Platform Detection

**Date:** 2026-05-25
**Scenario:** Multi-Platform Parity
**Status:** ✅ Resolved — context-pipe v0.5.0 (verified 2026-05-30)

---

## Description

context-pipe v0.4.5 has **no integration for [pi.dev](https://pi.dev)** — a minimal terminal coding harness with an extensible TypeScript plugin system. Every other major agent platform (Gemini CLI, OpenCode, Cursor, Claude Code, Windsurf, etc.) has a dedicated onboarding injector, platform detection, and documentation entry — but pi.dev is completely absent.

This is a **feature gap**, not a regression. The 21 verified scenarios all pass on Shell and Gemini CLI, but pi.dev users cannot use context-pipe without manual setup.

## Architectural Obstacle: pi.dev is "No MCP"

This is the **critical distinction** from every other supported platform.

All existing context-pipe integrations (Gemini CLI, OpenCode, Cursor, Claude Code, etc.) work by **registering context-pipe as an MCP server** in the client's configuration — either via `mcpServers` in JSON config or via hook-based interception (`PostToolUse`, `AfterTool`, etc.) that routes tool results through the Python wrapper.

**pi.dev explicitly rejects this approach.** Its README states:

> **No MCP.** Build CLI tools with READMEs (see Skills), or build an extension that adds MCP support.

pi.dev's architecture:
- **No `mcpServers` config** — there is no MCP server registry in pi.dev's settings
- **No hook system** — no `PostToolUse`, `AfterTool`, `PreCompress` or similar lifecycle hooks for tool execution
- **No `hooks.json` or `settings.json` injection point** for MCP servers

Instead, pi.dev uses a **TypeScript extension system**:
- Extensions are `.ts` files loaded from `~/.pi/agent/extensions/` or `.pi/extensions/`
- Tools are registered natively via `pi.registerTool()` using TypeBox schemas
- Event interception uses `pi.on("tool_call", ...)` and `pi.on("tool_result", ...)`
- Each tool communicates with external processes via `child_process` (spawning Python directly)

This means the integration **cannot follow the existing pattern** used by every other platform. You cannot `pipe_onboard` pi.dev by adding an MCP server entry to a JSON config. Instead, you must:
1. Write a TypeScript extension that spawns `python -m context_pipe.cli` as a subprocess
2. Register each context-pipe operation as a native pi tool
3. Intercept built-in `read` tool calls via `pi.on("tool_call", ...)`
4. Auto-pipe large outputs via `pi.on("tool_result", ...)`

## Root Cause (Remaining Integration Points)

The following integration points are missing:

### 1. No pi.dev Extension File

context-pipe provides `.opencode/plugins/context-pipe.ts` for OpenCode, `.openclaw/plugins/` for OpenClaw, and hook injection for Gemini CLI, Cursor, Claude Code, etc. There is **no `.pi/extensions/context-pipe.ts`** or equivalent pi package.

A pi.dev extension is a TypeScript module placed in `~/.pi/agent/extensions/` (global) or `.pi/extensions/` (project-local) that exports a factory function using the `ExtensionAPI`. It needs to:

- Register context-pipe's MCP tools as native pi tools (`pipe_read_file`, `pipe_run`, etc.)
- Intercept `tool_call` events to redirect native `read` to `pipe_read_file` for large files
- Intercept `tool_result` events to auto-pipe large outputs
- Register slash commands (`/pipe-stats`, `/pipe-verify`, `/pipe-list`)

### 2. No Platform Detection in `platforms.py`

File: `context_pipe/platforms.py` → `detect_client_id()`

The function checks env vars (`ANTIGRAVITY_AGENT`, `OPENCODE`, `CURSOR_TRACE_ID`, etc.) and parent process names (`antigravity`, `opencode`, `cursor`, etc.) to identify the calling platform. pi.dev is **not checked**:

- Missing env var detection for `PI_CODING_AGENT_DIR` (set when pi.dev is running)
- Missing parent process name entry for `"pi"`

### 3. No Onboarding Injection in `onboarding.py`

File: `context_pipe/onboarding.py` → `inject_hooks()`

The function dispatches to platform-specific injectors (`_inject_cursor`, `_inject_gemini`, `_inject_opencode`, etc.). There is **no `_inject_pi()`** function that would:

- Create `.pi/extensions/context-pipe.ts` in the target project
- Add context-pipe to pi.dev's `settings.json` under `extensions` or `packages`
- Optionally inject the mandate into the project's `AGENTS.md` for pi.dev tool names

### 4. No Documentation Entry

File: `doc/INTEGRATION_ENCYCLOPEDIA.md`

pi.dev is **absent** from both:
- Section 1 "Supported Environments & Compatibility Map"
- Section 2 "Master Configuration Matrix"

### 5. No Configuration Schema

There is no pi.dev-specific configuration schema in Section 3 of the integration encyclopedia. pi.dev extensions are loaded from:
- `~/.pi/agent/extensions/*.ts` (global)
- `.pi/extensions/*.ts` (project-local)
- Or via `pi install` from npm/git packages

The extension does NOT need to be registered as an MCP server — pi's philosophy is "No MCP." Instead, tools are registered natively via `pi.registerTool()`.

**Existing config schemas in the encyclopedia (A–D) are all MCP-based and irrelevant to pi.dev.** A new schema type "E" would need to be added describing the TypeScript extension registration pattern.

## Impact

| Dimension | Impact |
|---|---|
| **Platform parity** | pi.dev is the only major coding agent without context-pipe support |
| **Context safety** | pi.dev users can flood their context window with raw file reads |
| **Adoption** | Manual setup required — no `pipe_onboard` automation |
| **Telemetry** | pi.dev sessions are not attributed in the Balance Sheet |

## Reproduction

Confirmed gap — this is a missing feature, not a regression. Evidence:

```bash
# 1. context-pipe does not recognize pi.dev as a platform
$ python -c "from context_pipe.platforms import detect_client_id; print(detect_client_id())"
Generic CLI    # <--- pi.dev not detected; falls through to generic

# 2. pi.dev has no native MCP config — the standard MCP-based onboarding won't work
$ ls ~/.pi/agent/settings.json 2>/dev/null && cat ~/.pi/agent/settings.json
# pi.dev settings have no 'mcpServers' key — only 'extensions', 'skills', 'packages'

$ grep mcpServers ~/.pi/agent/settings.json 2>/dev/null || echo "No mcpServers in pi.dev config"
No mcpServers in pi.dev config

# 3. No context-pipe extension exists in pi.dev's auto-discovery paths
$ ls ~/.pi/agent/extensions/ 2>/dev/null || echo "No extensions directory"
No extensions directory

# 4. No .pi/ directory exists in the context-pipe project itself
$ ls target_repos/context-pipe/.pi/ 2>/dev/null || echo "No .pi/ directory"
No .pi/ directory

# 5. onboarding.py has no pi.dev injector — calling with environment='pi' does nothing pi-specific
$ python -c "from context_pipe.onboarding import inject_hooks; print(inject_hooks('.', 'pi'))"
# (only runs generic actions like gitignore, pipes.json, mandate injection — no pi.dev setup)
```

## Recommendation

Add a full pi.dev integration. Unlike other platforms, this requires a **new integration paradigm** — not MCP server registration but native TypeScript extension:

1. **`context_pipe/.pi/extensions/context-pipe.ts`** — TypeScript extension registering all CPP tools via `pi.registerTool()`, intercepting `tool_call` for native `read` blocking, and auto-piping large `tool_result` outputs.
   - Must register tools: `pipe_read_file`, `pipe_analyze_file`, `pipe_run`, `pipe_run_dynamic`, `list_pipes`, `get_pipe_stats`, `pipe_verify`, `pipe_audit_last`, `pipe_list_shadow_tools`, `pipe_agent_handoff`
   - Must register commands: `/pipe-stats`, `/pipe-verify`, `/pipe-list`

**Backend target: Rust `cpipe` binary preferred, Python fallback.**

The extension should call the **Rust `cpipe` binary** when available, falling back to `python -m context_pipe.cli`.

| Criterion | Python (`python -m context_pipe.cli`) | Rust (`cpipe`) |
|---|---|---|
| **Startup latency** | ~1000ms (cold Python import) | **~2ms** (native binary) |
| **Dependencies** | Requires Python + venv + `mcp-context-pipe` | Self-contained `.exe` |
| **CLI compatibility** | Same subcommands (`run`, `stats`, `verify`, etc.) | **Identical subcommands** + `verify` and `handoff` |
| **Availability** | Installed via `pip install mcp-context-pipe` | Installed via `scripts/fetch_cpipe.py` or cargo |
| **Version** | v0.4.5 | v0.4.5 |
| **Coexistence** | — | Designed to coexist (Python onboarding code already checks for Rust binary)" |

The Rust binary has the same CLI interface (`cpipe run <name>`, `cpipe stats`, `cpipe verify`, etc.) and is already detected by `discover_sift_executable()`-style logic in the Python onboarding. The project's stated philosophy is **"Coexistence First"** — "Coexists harmoniously with the Python package in the same workspace."

The extension should:
   - Try `cpipe` on PATH first (fast path)
   - Fall back to `python -m context_pipe.cli` (compatibility)
   - Show a startup warning if neither is found

2. **`context_pipe/platforms.py`** — Add `("PI_CODING_AGENT_DIR", "pi.dev")` to `_ENV_MAP` and `("pi", "pi.dev")` to `_PROC_MAP` in `detect_client_id()`

3. **`context_pipe/onboarding.py`** — Add `_inject_pi()` that creates `.pi/extensions/context-pipe.ts` and writes a minimal `package.json` for pi package discovery, plus dispatch in `inject_hooks()`

4. **`doc/INTEGRATION_ENCYCLOPEDIA.md`** — Add pi.dev section with:
   - Compatibility note: "No MCP. Native TypeScript extension required."
   - New Schema **"E"** for pi.dev: extension path in `extensions` array or pi package in `packages`
   - Config entry for `~/.pi/agent/settings.json` under `extensions` or `packages` keys

## Related

- pi.dev Extension API docs: `C:\Users\luism\AppData\Roaming\npm\node_modules\@earendil-works\pi-coding-agent\docs\extensions.md`
- pi.dev README: same path, `README.md`
- Existing platform reference: `.opencode/plugins/context-pipe.ts` (similar TypeScript plugin pattern)
