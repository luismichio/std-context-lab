# Scenario 04: Core Pre-Filters

## Objective
To prove that deterministic CLI tools (like `findstr`, `jq`, `rg`) can significantly optimize the context pipeline by pruning noise at the structural level before data reaches more intensive refinery nodes.

## Setup
- **Dataset**: `noisy_app.log` (5,000 lines of mixed DEBUG/INFO/CRITICAL logs).
- **Pipeline**: `log-optimizer`
    - Node 1: `findstr "CRITICAL"` (Structural pre-filter)
    - Node 2: `semantic-sift-cli logs` (Heuristic refinery)

## Execution
Run the following command:
```bash
Get-Content noisy_app.log -Raw | mcp-pipe run log-optimizer
```

## Findings
- **Token Efficiency**: ✅ The pre-filter removed >99% of the noise (DEBUG/INFO lines) instantly using a deterministic local binary.
- **Supply Chain Synergy**: ✅ `semantic-sift` successfully processed the remaining lines to strip redundant timestamps and formatting, yielding a perfect context summary for an AI agent.

## Resolved Bugs
- **Verified & Closed Bug #003**: During initial testing (`v0.2.2`), `context-pipe` failed to resolve binaries (like `yq`) on Windows. This was fixed upstream. The `v0.3.1` regression sweep confirmed that `.exe` resolution works flawlessly.
- **Verified & Closed Bug #001**: During initial testing, the orchestrator crashed in verbose mode (`-v`) if a binary resolution failed. This was fixed upstream and verified to gracefully surface the `help_msg` without crashing in the `v0.3.1` sweep.
