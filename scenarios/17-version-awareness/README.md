# Scenario 17: Version Awareness & Self-Update

## Objective
To test if the `context-pipe` orchestrator is "Version Aware", meaning it can automatically discover if the user's local installation is out of date compared to the remote GitHub repository, and provide actionable "Self-Heal" instructions.

## Setup
- **Action**: Manually downgraded the local `pyproject.toml` version of `mcp-context-pipe` to `0.2.0`.
- **Tool**: Executed `pipe_verify()` via the `context-pipe` MCP server to check the installation health.

## Execution
Run the following MCP call:
```python
pipe_verify()
```

## Findings
- **Version Awareness**: ✅ **VERIFIED**. The `pipe_verify` tool successfully checked the GitHub repository and detected that the local version (`0.2.0`) was older than the remote release (`0.3.1`).
- **Self-Heal Instructions**: ✅ **VERIFIED**. The system surfaced actionable update instructions: `⚠️ Update Available: A newer version (v0.3.1) is available. Run pip install --upgrade mcp-context-pipe to apply.`
- **Resolved Gap**: **Verified & Closed Feature Request #019**. The orchestrator now possesses self-healing network-based tag checking.
