# Scenario 23 — Conditional Branching / `condition` Predicates (Phase 11A)

## Claim Under Test
Any node in a pipe can declare a `condition` key. The orchestrator evaluates the predicate **before** the node executes — if false, the node is skipped entirely (no subprocess spawned). Five predicates are supported: `size:>N`, `size:<N`, `artifact:missing:<path>`, `artifact:exists:<path>`, `contains:<string>`. Unknown predicates fail-open (warn + run).

## Feature Reference
- `context_pipe/orchestrator.py` — `_evaluate_condition(predicate, input_data)`
- `crates/cpipe/src/orchestrator.rs` — `evaluate_condition()`

## What to Verify

### Test A — `size:>N` skip (input is small)
Input is 100 chars. Run `condition-size-gate` pipe. Node with `condition: "size:>5000"` must be **skipped**. Final output = pass-through only.

### Test B — `size:>N` execute (input is large)
Input is 10,000 chars. Same pipe. Node with `condition: "size:>5000"` must **execute**. Output is sifted.

### Test C — `size:<N` skip (input is large)
Input is 10,000 chars. Node with `condition: "size:<500"` must be **skipped**.

### Test D — `artifact:missing:<path>` skip (file exists)
Pre-create `.cache/test-artifact.json`. Run `condition-artifact-pipe`. Node with `condition: "artifact:missing:.cache/test-artifact.json"` must be **skipped**.

### Test E — `artifact:missing:<path>` execute (file absent)
Delete `.cache/test-artifact.json`. Same pipe. Node must **execute**.

### Test F — `artifact:exists:<path>` (inverse of D/E)
Node with `condition: "artifact:exists:.cache/test-artifact.json"` — executes when file present, skips when absent.

### Test G — `contains:<string>` skip
Input does not contain `"ERROR"`. Node with `condition: "contains:ERROR"` must be **skipped**.

### Test H — `contains:<string>` execute
Input contains `"ERROR"`. Same pipe. Node must **execute**.

### Test I — Unknown predicate fails-open
Node with `condition: "unknown:predicate"` must warn but still execute (fail-open).

### Test J — Rust parity
Run Tests A and B via `cpipe run condition-size-gate`. Confirm identical skip/execute behaviour.

## Expected Artefact
`run_conditional_branching.log`

## Dual-Channel Check
| Channel | Command |
|---|---|
| Shell | `echo "short" \| mcp-pipe run condition-size-gate` |
| Agent | `pipe_run("condition-size-gate", short_text)` |
