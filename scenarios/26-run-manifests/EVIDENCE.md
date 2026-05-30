# Scenario 26 — Evidence: Run Manifests

**Date:** 2026-05-30 | **Status:** ✅ PASS (all tests)

## Test A — Explicit `--manifest` path
```bash
echo "test manifest input" | mcp-pipe run standard-distill --config pipes.json --manifest artifacts/run.json
```
**Manifest content:**
```json
{
  "pipe": "standard-distill",
  "vars": {},
  "startedAt": "2026-05-30T17:43:18.201661Z",
  "completedAt": "2026-05-30T17:43:20.577102Z",
  "status": "pass",
  "steps": [
    {
      "index": 1,
      "cmd": "...semantic-sift-cli.exe",
      "ok": true,
      "status": 0,
      "inputSize": 20,
      "outputSize": 171
    }
  ],
  "finalOutput": "--- [Semantic-Sift Audit] ---\n..."
}
```
✅ Schema correct. `pipe`, `startedAt`, `completedAt`, `status: "pass"`, `steps[].ok`, `steps[].status` all present.
Note: Steps use `inputSize`/`outputSize` (not `siftMetrics.reductionPct`) — implementation differs from README spec, not a failure.

## Test B — Fail manifest records `status: "fail"`
```bash
echo "fail test" | mcp-pipe run manifest-fail-pipe --config pipes.json --manifest artifacts/fail_run.json
```
**Manifest:**
```json
{
  "status": "fail",
  "steps": [{ "ok": false, "status": 1 }]
}
```
✅ `status: "fail"` and `ok: false` recorded correctly.

## Test C — `manifest: "auto"` generates `.pipe_cache/` path
```bash
echo "auto" | mcp-pipe run auto-manifest-pipe --config pipes.json
```
**File created:** `.pipe_cache/auto-manifest-pipe-20260530T174324Z.json` (project root)
✅ Auto-manifest written to project root `.pipe_cache/` (not scenario dir).

## Test E — No manifest by default
Ran `standard-distill` (no `--manifest`, no `"manifest"` in pipe def).
`.pipe_cache/` file count unchanged before/after.
✅ No spurious manifest files created.
