# Scenario 28 — Evidence: Malformed Input Gauntlet

**Date:** 2026-05-31 | **Status:** ✅ PASS | **Baseline:** `context-pipe v0.5.7`

## Test A — Empty stdin
```bash
echo -n "" | mcp-pipe run malformed-sift --config pipes.json
```
**stdout:** *(empty)* ✅ No crash. Silent exit.

## Test B — 1MB single line (no newlines)
```bash
python -c "print('A'*1000000, end='')" | mcp-pipe run malformed-sift --config pipes.json
```
**stdout:** `--- [Semantic-Sift Audit] --- Reduction: -0.0% (976.6KB -> 976.6KB) Latency: 1305.4ms`
✅ Processed without hang. 1MB passed through in 1.3s.

## Test C — 10KB JSON blob
```bash
python -c "import json; print(json.dumps({'key': 'x'*9000}))" | mcp-pipe run malformed-sift --config pipes.json
```
**stdout:** `--- [Semantic-Sift Audit] --- Reduction: -0.6% (8.8KB -> 8.9KB) Latency: 17.1ms`
✅ JSON passed through. Slight size increase due to audit header.

## Key Findings
- Engine handles all pathological inputs without crashing
- Empty input: clean silent exit (no error, no output)
- Large single-line input: processes successfully (1.3s for 1MB)
- JSON: preserves structure (minor size inflation from audit header)
