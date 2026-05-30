# Scenario 24 — DAG Validator Nodes + Loop Guard (Phase 11B/C)

## Claim Under Test
`type: "validator"` nodes route execution to named `branch_sequences` based on exit code. `id` and `next` fields enable explicit DAG jumps. A 100-step loop guard prevents infinite cycles, emitting `--- [Context-Pipe: Loop Guard] ---`.

## Feature Reference
- `orchestrator.py` — DAG traversal replacing linear `run_pipe()` loop
- `"type": "validator"` node type + `branches` map
- `"branch_sequences"` top-level pipe field
- `"id"` and `"next"` node keys
- 100-step loop guard — `--- [Context-Pipe: Loop Guard] ---`
- Rust parity: `crates/cpipe/src/orchestrator.rs`

## What to Verify

### Test A — Validator routes exit 0 to success branch
Run `validator-exit-router` with content that causes the validator to exit 0. Confirm the `"0"` branch (`pass-sift`) executes. Output has sift audit header.

### Test B — Validator routes exit 1 to fallback branch
Run same pipe with content that causes exit 1. Confirm `"1"` branch (`fail-passthrough`) executes. Output is raw passthrough.

### Test C — `default` branch catches unknown exit code
Validator exits with code 2 (no explicit branch). Confirm `"default"` branch runs instead of failing.

### Test D — `id` + `next` explicit jump
Run `explicit-jump-pipe`. Confirm execution jumps from node `A` directly to node `C` (skipping `B`) via `"next": "node-c"`. Output only shows evidence of A and C processing.

### Test E — `branch_sequences` named sub-graph
Run `branch-sequences-pipe`. Confirm validator branches into the `"on-fail"` named sequence, which runs a separate set of nodes.

### Test F — Loop Guard triggers at 100 steps
Run `loop-guard-pipe` (intentional `next` cycle). Confirm execution terminates with `--- [Context-Pipe: Loop Guard] ---` in output after 100 steps. No infinite hang.

### Test G — Rust parity
Run Tests A and F via `cpipe run`. Confirm identical branching and loop guard behaviour.

### Test E — `artifact-fork-pipe`: True Two-Route Fork

Validator exits 0 if `.cache/spec.json` exists, 1 if missing. Routes to mutually exclusive `branch_sequences` — exactly one fires per execution.

**Route 1 — artifact MISSING → `route-create`**
```bash
rm -f .cache/spec.json && echo "input" | mcp-pipe run artifact-fork-pipe --config pipes.json
```
Expect: `[CREATED] .cache/spec.json` prefix in output. Sift not spawned.

**Route 2 — artifact EXISTS → `route-sift`**
```bash
echo "input" | mcp-pipe run artifact-fork-pipe --config pipes.json
```
Expect: `--- [Semantic-Sift Audit] ---` header. Artifact on disk unchanged.

> **Design note:** `condition` predicates evaluated sequentially cannot guarantee a true fork — node 1 can mutate state and satisfy node 2’s condition in the same run. `type: "validator"` + `branch_sequences` is the correct primitive for mutual exclusion.

### Test F — `validator-loop-pipe`: Validator Cycle Loop Guard
Validator exits 0 and branches to a sequence that `next: "start"` back to itself. Must trigger 100-step loop guard.

```bash
echo "test" | mcp-pipe run validator-loop-pipe --config pipes.json
```
Expect: `--- [Context-Pipe: Loop Guard] ---`

### Test G — `nested-validator-pipe`: Validator in `branch_sequences`
Outer validator exits 1 → branch to `inner-val-seq` → inner validator exits 0 → branch to `inner-sift-seq` → sift runs.

```bash
echo "input" | mcp-pipe run nested-validator-pipe --config pipes.json
```
Expect: `--- [Semantic-Sift Audit] ---`

## Expected Artefact
`run_dag_validator.log`

## Dual-Channel Check
| Channel | Command |
|---|---|
| Shell | `echo "test" \| mcp-pipe run validator-exit-router` |
| Agent | `pipe_run("validator-exit-router", "test content")` |
