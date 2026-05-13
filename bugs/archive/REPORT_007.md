# Bug Report 007: Silent Telemetry Gap

**Date:** 2026-05-11
**Scenario:** 06 - A2A Testing / ROI Measurement
**Status:** Closed (Verified)

---

## 1. Telemetry Disabled by Default (Opt-In)

### Description
The Context-Pipe orchestrator fails to record any telemetry data by default. The `get_pipe_stats` tool returns zero chars and zero events even after successful pipe executions.

### Verification (2026-05-11)
Successfully verified that `telemetry.py` now correctly defaults to Opt-Out (telemetry is ON by default) unless explicitly disabled, aligning with documentation claims.

### Root Cause
In `context_pipe/telemetry.py`, the `PIPE_TELEMETRY_DISABLED` flag is set to `True` unless the environment variable `CPP_TELEMETRY_OPTED_IN` is explicitly set to `true`. 

### Rationale Check
The project documentation claims: *"Every byte saved is accounted for in the Context Balance Sheet automatically."* and *"Every pipe run is traceable."* 
However, the implementation forces a secret opt-in step that is not mentioned in the Quickstart or the main README, leading to a silent failure of the accounting system for most users.

---

## 2. Impact on Lab
Laboratory ROI measurements were impossible until the secret environment variable was identified via source code audit. Technical claims regarding "Automatic Accounting" are currently misleading in the primary documentation.
