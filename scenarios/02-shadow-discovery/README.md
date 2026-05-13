# Scenario 02: Shadow Discovery

## Objective
To prove the "Zero Tool Bloat" claim by discovering and executing MCP tools from a "Shadow Server" (not registered in the global IDE environment).

## Setup
- **Shadow Server**: `@modelcontextprotocol/server-everything` (Installed in `scenarios/shared_mcps/`).
- **Configuration**: Registered only in the local `pipes.json` (Scenario-specific) and the root `pipes.json`.

## Execution
1. **Introspection**: List tools on the shadow server.
   ```bash
   mcp-pipe tool everything --list-tools
   ```
2. **Direct Execution**: Call a shadow tool via the shell-to-MCP bridge.
   ```bash
   echo "Hello" | mcp-pipe tool everything echo --input-key message
   ```

## Findings
- **Discovery**: ✅ The orchestrator successfully introspected the server and listed its 10+ tools despite the server being hidden from the IDE.
- **Shadow Execution**: ✅ Direct bridging via `mcp-pipe tool` worked perfectly, capturing standard output from the Node-based MCP server.

## Resolved Bug
**Verified & Closed Bug #001**: During initial testing (`v0.2.2`), the `mcp-pipe run` command failed to pass the `server_registry` to the orchestrator. This was fixed upstream. The `v0.3.1` regression sweep confirmed that shadow MCP nodes now function perfectly inside named pipelines called from the CLI.
