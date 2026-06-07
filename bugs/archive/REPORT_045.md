# REPORT_045 — semantic-sift telemetry logger fails hard on malformed telemetry JSON

**Date**: 2026-06-02
**Scenario**: 06 - A2A Handoff ROI (VS Code pass)
**Status**: ✅ Closed (verified 2026-06-07)
**Target Repo**: semantic-sift
**Priority**: Medium - observability degraded, noisy runtime errors

---

## Description

When the telemetry file contains malformed JSON, telemetry logging throws `JSONDecodeError` during `json.load()` and emits a stack trace. The logger does not attempt recovery (backup/repair/reset), so telemetry writes continue to fail until manual intervention.

---

## Root Cause

`log_telemetry()` assumes `TELEMETRY_FILE` is valid JSON whenever the file exists:

- opens file
- calls `json.load(f)`
- no local recovery path on parse failure

Relevant location: [target_repos/semantic-sift/semantic_sift/telemetry.py](target_repos/semantic-sift/semantic_sift/telemetry.py#L438)

---

## Evidence/Reproduction

### Trigger during scenario run
```powershell
Write-Output "Agent A output ..." | .\.venv\Scripts\mcp-pipe.exe handoff --from-agent AgentA --to-agent AgentB
```

### Observed output excerpt
```text
Failed to write telemetry record for tool 'unknown:AgentA'
json.decoder.JSONDecodeError: Extra data: line 363 column 2 ...
```

---

## Impact

- Telemetry for affected sessions/tools is dropped.
- Runtime output is polluted with traceback noise.
- ROI/balance sheet data becomes incomplete and unreliable.

---

## Proposed Fix

1. Add resilient read path in `log_telemetry()`:
- wrap `json.load` with `try/except JSONDecodeError`
- on failure, move bad file to `.pipe_telemetry.json.corrupt.<timestamp>`
- reinitialize empty telemetry structure and continue write.
2. Add a compact warning log line (no full traceback by default).
3. Optionally support JSONL fallback if JSON object parse fails.

---

## Acceptance Criteria

- Malformed telemetry file does not raise unhandled traceback during normal tool flow.
- Logger self-heals and subsequent telemetry writes succeed.
- Corrupt original is preserved for forensic debugging.

---

## Verification Update (2026-06-07)

Executed a forced-malformation test against current `semantic-sift`:

1. Wrote malformed JSON into `TELEMETRY_FILE`.
2. Called `log_telemetry(...)`.
3. Verified backup + reinit behavior.

Observed output:

```text
Telemetry file '.pipe_telemetry.json' is malformed (...). Backing up to '.pipe_telemetry.json.corrupt.<timestamp>' and reinitializing.
corrupt_created= True
has_session= True
```

Result: logger self-heals and persists new telemetry. This issue is resolved.
