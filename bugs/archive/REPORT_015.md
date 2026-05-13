# Bug Report 015: Orchestrator Lack of Failure-Bypass Logic

**Date:** 2026-05-12
**Scenario:** 13 - Resiliency Gauntlet
**Status:** Open

---

## 1. Fail-Fast Orchestration

### Description
The `context-pipe` orchestrator aborts the entire pipeline execution immediately if any single node fails (FileNotFound, Timeout, or Non-zero Exit Code).

### Root Cause
In `context_pipe/orchestrator.py` -> `run_pipe()`, all `except` blocks for node execution terminate the loop and `return error_text, trace`. There is no mechanism to mark a node as "Optional" or to catch errors and continue with the next node in the chain using the `current_input` from the last successful node.

### Evidence
In Scenario 13, a 5-node pipe was defined. Node 1 failed to resolve a binary. Instead of surfacing the help message and passing the raw input to Node 2, the orchestrator returned immediately, and the remaining 4 nodes were never executed.

---

## 2. Impact on Lab
Complex "Mental Supply Chains" are fragile. If a non-essential "Pre-Filter" or "Telemetry" node fails, the entire context retrieval process is blocked, leading to a degraded user experience.

### Recommended Fix
Introduce an `optional: true` flag in the `pipes.json` node schema. If a node is optional, the orchestrator should log the error in the trace but continue execution using the output of the previous successful node.
