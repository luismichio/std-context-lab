# Scenario 18: Autonomous Dynamic Sifting

## Objective
To prove the "Dynamic Sifting" capability, allowing an autonomous AI agent to assemble and execute Just-In-Time (JIT) processing pipelines without modifying the static `pipes.json`.

## Setup
- **File**: `needle_in_haystack.log` (A generated 1,000-line noise file with one "needle").
- **Workflow**: Just-In-Time Graph assembly.
- **Pipeline**: Dynamic
    - Node 1: `grep` (Search)
    - Node 2: `semantic-sift-cli` (Refinery)

## Execution
Run the following command from the scenario directory:
```bash
mcp-pipe run-dynamic '[{"cmd": "grep", "args": ["needle"]}, {"cmd": "semantic-sift-cli", "args": ["semantic"]}]' --input_file needle_in_haystack.log --allow_shell
```

## Findings
- **JIT Assembly**: ✅ The orchestrator successfully interpreted an ad-hoc JSON graph and executed it.
- **Shell Synergy**: ✅ The `allow_shell` flag correctly permitted the use of `grep` as a pre-filter.
- **Autonomous Recovery**: ✅ Proved that agents can bypass static configuration to find specific signals in massive data.

## Phase 11 Feature Parity via run-dynamic (2026-05-30)
All Phase 11 features (`type:"validator"` + `branches`, `condition`, `id`+`next`) are supported by `run_dynamic_pipe` because node schemas pass through unmodified to `run_pipe`. Verified:

| Feature | Dynamic | pipes.json |
|---|---|---|
| `type:"validator"` + `branches` | ✅ (exit 0 → sift) | ✅ (S24) |
| `condition` (size, artifact, contains) | ✅ (first node skipped) | ✅ (S23) |
| `id` + `next` explicit jump | ✅ (skip B) | ✅ (S24) |
