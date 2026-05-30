# Scenario 26 — Run Manifests (Phase 12B)

## Claim Under Test
After a pipe completes, `--manifest <path>` writes a structured JSON artifact recording the full execution trace: pipe name, completion timestamp, status, per-step results, sift metrics. `"manifest": "auto"` in the pipe definition enables automatic path generation at `.pipe_cache/<pipe-name>-<iso>.json`.

## Feature Reference
- `context_pipe/orchestrator.py` — `run_pipe()` `manifest_path` param
- `context_pipe/cli.py` — `--manifest <path>` flag
- `context_pipe/server.py` — `pipe_run` `manifest_path` param
- `pipes.json` — `"manifest": "auto"` per-pipe field

## What to Verify

### Test A — Explicit `--manifest` path
```bash
echo "test input" | mcp-pipe run standard-distill --manifest artifacts/run.json
```
Confirm `artifacts/run.json` is created. Validate schema:
- `pipe` key present
- `completedAt` ISO timestamp
- `status` is `"pass"` or `"fail"`
- `steps[]` with `index`, `cmd`, `ok`, and `siftMetrics` (where applicable)

### Test B — Manifest on failure
Run `manifest-pipe` with a deliberately broken node (optional: false) that exits non-zero.
Confirm manifest records `status: "fail"` and the failed step's `ok: false`.

### Test C — `"manifest": "auto"` generates path
Run `auto-manifest-pipe` (has `"manifest": "auto"` in pipe definition) with no `--manifest` flag.
Confirm a file appears at `.pipe_cache/auto-manifest-pipe-<timestamp>.json`.

### Test D — Manifest content integrity
Open the manifest from Test A or C. Confirm:
- `siftMetrics.reductionPct` is a float
- `siftMetrics.latencyMs` is a number
- Step count matches node count in the pipe

### Test E — No manifest by default
Run `mcp-pipe run standard-distill` with no `--manifest` flag and no `"manifest"` in pipe definition.
Confirm no `.json` file is created in `.pipe_cache/`.

## Expected Artefact
`run_manifests.log`, `artifacts/run.json`

## Dual-Channel Check
| Channel | Command |
|---|---|
| Shell | `echo "test" \| mcp-pipe run standard-distill --manifest artifacts/run.json` |
| Agent | `pipe_run("standard-distill", text)` — check for manifest side-effect |
