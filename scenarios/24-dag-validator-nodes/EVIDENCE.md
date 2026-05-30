# Scenario 24 — Evidence: DAG Validator Nodes + Loop Guard

**Date:** 2026-05-30 | **Status:** ✅ PASS (all tests)

## Test A — Validator exit 0 → `pass-sift` branch
```bash
echo "test content" | mcp-pipe run validator-exit-router --config pipes.json
```
**stdout:** `--- [Semantic-Sift Audit] ---` (sift branch executed)
✅ Exit code 0 routed to `pass-sift`.

## Test B — Validator exit 1 → `fail-passthrough` branch
```bash
echo "test content" | mcp-pipe run validator-exit-1-router --config pipes.json
```
**stdout:** `[PASSTHROUGH] test content`
✅ Exit code 1 routed to `fail-passthrough`.

## Test D — `id` + `next` explicit jump (B skipped)
```bash
echo "input" | mcp-pipe run explicit-jump-pipe --config pipes.json
```
**stdout:** `[C][A]input`

Interpretation:
- Node A ran: output = `[A]input`
- `next: "node-c"` jumped to node C (skipping B)
- Node C ran: output = `[C][A]input`
- `[B-SHOULD-NOT-APPEAR]` is absent ✅

✅ Explicit DAG jump confirmed. Node B skipped.

## Test E — `artifact-fork-pipe`: True Two-Route Fork

**Route 1 — artifact MISSING → `route-create` branch**
```bash
rm -f .cache/spec.json
echo "input data for spec creation" | mcp-pipe run artifact-fork-pipe --config pipes.json
```
**stdout:** `[CREATED] .cache/spec.json` + input text
**artifact on disk:** `{"created_by": "context-pipe-lab", "input": "input data for spec creation\n"}`
✅ Only the create script ran. Sift was never spawned.

**Route 2 — artifact EXISTS → `route-sift` branch**
```bash
echo "this content will be sifted" | mcp-pipe run artifact-fork-pipe --config pipes.json
```
**stdout:** `--- [Semantic-Sift Audit] ---` (sift executed)
**artifact on disk:** unchanged from Route 1 (create script not called)
✅ Only the sift ran. Mutual exclusion confirmed.

**Key finding:** inverse `condition` predicates (`artifact:missing` + `artifact:exists`) do NOT create a true fork — node 1 can change state and satisfy node 2’s condition in the same run. `type: "validator"` + `branch_sequences` is the correct primitive.

## Test F — Loop Guard (100-step limit)
```bash
echo "loop" | mcp-pipe run loop-guard-pipe --config pipes.json
```
**stdout:**
```
--- [Context-Pipe: Loop Guard] ---
Maximum pipe execution steps (100) exceeded. Possible infinite loop.
```
✅ Loop guard triggered cleanly at 100 steps. No infinite hang.

## Test G — Validator Loop (validator branches back to itself)
```bash
echo "test" | mcp-pipe run validator-loop-pipe --config pipes.json
```
**stdout:** `--- [Context-Pipe: Loop Guard] ---\nMaximum pipe execution steps (100) exceeded. Possible infinite loop.`
✅ The loop guard is universal — it counts every iteration regardless of whether the cycle is formed by `id`+`next` or by validator branching back to itself.

## Test H — Nested Validator (validator inside `branch_sequences`)
```bash
echo "nested dag test" | mcp-pipe run nested-validator-pipe --config pipes.json
```
**Path:** outer-val exits 1 → branch `inner-val-seq` → inner-validator exits 0 → branch `inner-sift-seq` → sift runs.
**stdout:** `--- [Semantic-Sift Audit] ---` (sift executed)
✅ Nested DAG with two levels of validator routing works correctly.
