# Scenario 23 — Evidence: Conditional Branching

**Date:** 2026-05-30 | **Status:** ✅ PASS (all tests)

## Test A — `size:>5000` SKIP (small input)
```bash
echo "short" | mcp-pipe run condition-size-gate --config pipes.json
```
**stdout:** `short` (raw passthrough — node skipped)
✅ Condition false → node not executed.

## Test B — `size:>5000` EXECUTE (large input)
```bash
python -c "print('A'*10000)" | mcp-pipe run condition-size-gate --config pipes.json
```
**stdout:** `--- [Semantic-Sift Audit] ---` (sift executed)
✅ Condition true → node runs.

## Test C — `size:<500` SKIP (large input)
**stdout:** Raw `AAAA...` passthrough. ✅

## Test D — `artifact:missing` SKIP (file exists)
Pre-created `.cache/test-artifact.json`. Input `"test"` → passthrough. ✅

## Test E — `artifact:missing` EXECUTE (file absent)
Deleted `.cache/test-artifact.json`. Input `"test"` → sift audit header. ✅

## Test G — `contains:ERROR` SKIP (no ERROR in input)
```bash
echo "short" | mcp-pipe run condition-contains-error-pipe --config pipes.json
```
**stdout:** `short` (passthrough) ✅

## Test H — `contains:ERROR` EXECUTE (ERROR in input)
```bash
echo "This line has an ERROR code" | mcp-pipe run condition-contains-error-pipe --config pipes.json
```
**stdout:** `--- [Semantic-Sift Audit] ---` ✅

## Test I — Unknown predicate fails-open
```bash
echo "test" | mcp-pipe run condition-fail-open-pipe --config pipes.json 2>&1
```
**stderr:** `Unknown condition predicate: unknown:predicate:value`
**stdout:** Sift output (node ran after warning)
✅ Fail-open: warning emitted, node still executes.

## Rust Parity
```bash
echo "short" | cpipe run condition-size-gate --config pipes.json  # → "short" (skip)
python -c "print('A'*10000)" | cpipe run condition-size-gate ...  # → audit header (execute)
```
✅ Rust parity confirmed.
