# Scenario 16: Protocol Violation Stress

## Objective
To prove the "Stream Integrity" and "Platform Safety" claims: that the context supply chain orchestrator can sanitize bad data and prevent crashes when a node violates the Standard I/O text protocol by outputting binary garbage.

## Setup
- **Node**: `bad_actor.py` (Outputs invalid UTF-8 byte sequences `\xff\xfe\xfd` and null bytes).
- **Pipeline**: `corruption-pipe` (Chains the bad actor into `semantic-sift-cli`).

## Execution
Run the following command:
```bash
echo "start" | mcp-pipe run corruption-pipe -v
```

## Findings
- **Stream Sanitization**: ✅ **VERIFIED**. The orchestrator safely intercepts and replaces invalid non-UTF8 bytes with `` placeholders instead of crashing.
- **Crash Prevention**: ✅ **VERIFIED**. The pipeline executes without Python tracebacks despite encountering `b"\xff\xfe\xfd"` and null bytes.
- **Resolved Bug**: **Verified & Closed Bug #020**. Subprocesses are now explicitly executed with robust error handling for standard I/O streams.
