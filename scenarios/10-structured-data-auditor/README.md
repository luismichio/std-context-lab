# Scenario 10: The Structured Data Auditor

## Objective
To prove that `context-pipe` intentionally bypasses sifting for structured JSON data (to prevent data corruption) and to demonstrate how to explicitly distil database results using a multi-node supply chain.

## Setup
- **Dataset**: `mock_telemetry.db` (Local SQLite database with 1,000 bloated JSON rows).
- **Tooling**: `@modelcontextprotocol/server-sqlite` (MCP).
- **Test A (Raw Bypass)**: Call `sqlite/read_query` directly.
- **Test B (Explicit Distillation)**: Chain `sqlite/read_query` -> `yq` -> `semantic-sift`.

## Execution
Run the following script:
```bash
python run_pipe_manual.py
```

## Findings
- **Structured Data Exemption**: ✅ **PROVEN**. When the SQLite node returned a valid JSON list, the orchestrator immediately bypassed all subsequent sifting logic. This confirms that "Zero Save" results for tools like Supabase are a **safety feature**, not a bug.
- **Supply Chain Power**: ✅ Demonstrated that users can opt-in to distillation for structured data by explicitly flattening it via `jq` or `yq` first.
- **Automation**: ✅ Proved that the "Mental Supply Chain" can handle mixed data types (Structured JSON vs. Unstructured Text) intelligently.
