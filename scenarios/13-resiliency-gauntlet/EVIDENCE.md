# Evidence: Scenario 13 (Resiliency Gauntlet)

**Verified On:** 2026-05-24
**Baseline:** `context-pipe v0.4.3` | `semantic-sift v0.3.2`

## Verification Command
```powershell
mcp-pipe run resilience-pipe --config pipes.json --input_file ../01-protocol-basics/sample.log
```

## Captured Evidence (Raw)
*   **Log File**: [run_resiliency_gauntlet.log](run_resiliency_gauntlet.log)
*   **Claim Proven**: Proved that the system gracefully handles and bypasses node failures via the `optional: true` schema.

## Gap Tests Added 2026-05-30 (baseline: context-pipe v0.5.2)

### Test G — `required-timeout-pipe`: Timeout on required node
Pipe has a node that sleeps 30s with `"timeout": 2`. **Bug found:** `node.get("timeout")` is never read by the orchestrator (see REPORT_039). Only `PIPE_NODE_TIMEOUT_MS` env var is respected. Tested with env var workaround:

```bash
PIPE_NODE_TIMEOUT_MS=2000 echo "test" | mcp-pipe run required-timeout-pipe --config pipes.json
```
**stdout:** `--- [Context-Pipe: Timeout] ---\nNode ...python.exe exceeded 2.0s.`
✅ Timeout halts the pipe cleanly (env var path). Node-level `timeout` field is broken (REPORT_039).

### Test H — `optional-condition-pipe`: `optional: true` + `condition` interaction

**Subtest H1 — condition false (small input):**
```bash
echo "short" | mcp-pipe run optional-condition-pipe --config pipes.json
```
**stdout:** sift audit header + `short`
✅ Condition `size:>5000` false → node skipped entirely. `optional` not relevant. Sift runs.

**Subtest H2 — condition true + exit non-zero (large input with optional):**
```bash
python -c "print('A'*10000)" | mcp-pipe run optional-condition-pipe --config pipes.json
```
**stdout:** sift audit header + all 10000 A's
✅ Condition true → node executes → exits 1 → optional bypasses failure → sift runs on original input.

### False pass discovered in original S13
`forever_sleep.py` reads **1 character** and exits immediately — it never sleeps at all. The gauntlet-pipe's `[TIMEOUT]` claim in the original evidence was incorrect. The per-node `"timeout"` field is completely ignored by the orchestrator (REPORT_039).
