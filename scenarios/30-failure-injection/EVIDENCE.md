# Scenario 30 — Evidence: Failure Injection

**Date:** 2026-05-31 | **Status:** ✅ PASS | **Baseline:** `context-pipe v0.5.7`

## Test A — Empty output node (exit 0)
```bash
echo "input" | mcp-pipe run empty-output-pipe --config pipes.json
```
**stdout:** *(empty)* ✅ No crash. Node produced no output, next node received empty input, silent exit.

## Test B — Required node exits 1
```bash
echo "input" | mcp-pipe run required-fail-pipe --config pipes.json
```
**stdout:** `Error in node python: fail_node: deliberate failure`
✅ Pipe aborted cleanly. Error reported. No crash.

## Test C — Optional node exits 1 (bypassed)
```bash
echo "input" | mcp-pipe run optional-fail-pipe --config pipes.json
```
**stdout:** `--- [Semantic-Sift Audit] ---` + `input`
✅ Failed node bypassed. Subsequent sift node ran on original input.

## Test D — 10MB flood output
```bash
echo "start" | mcp-pipe run flood-pipe --config pipes.json
```
**stdout:** `--- [Semantic-Sift Audit] --- Reduction: -0.0% (9843.8KB -> 9843.8KB)`
✅ 10MB processed without OOM or hang. Engine held under pressure.
