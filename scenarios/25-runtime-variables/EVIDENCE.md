# Scenario 25 — Evidence: Runtime Variable Injection

**Date:** 2026-05-30 | **Status:** ⚠️ PARTIAL (1 bug found — REPORT_038)

## Test A — `--var RATE=0.3` injected
```bash
echo "hello world test input" | mcp-pipe run var-rate-pipe --config pipes.json --var RATE=0.3
```
**stdout:** `--- [Semantic-Sift Audit] ---` (pipe ran with RATE=0.3) ✅

## Test B — Pipe `vars` default (RATE=0.5)
```bash
echo "hello world test input" | mcp-pipe run var-rate-pipe --config pipes.json
```
**stdout:** Audit header present (default 0.5 used) ✅

## Test C — Caller `--var` overrides default
```bash
echo "hello world test input" | mcp-pipe run var-rate-pipe --config pipes.json --var RATE=0.1
```
**stdout:** Audit header present (0.1 override applied) ✅

## Test D — Missing variable fail-fast ❌ BUG (REPORT_038)
```bash
echo "test" | mcp-pipe run var-missing-pipe --config pipes.json
```
**Expected:** `mcp-pipe: error: Missing pipe variable: REQUIRED_VAR`
**Actual:**
```
Error in node ...semantic-sift-cli: argument --rate: invalid float value: '${REQUIRED_VAR}'
```
❌ Literal `${REQUIRED_VAR}` passed to subprocess. No pre-spawn check. **→ REPORT_038**

## Test E — Multiple `--var` flags
```bash
echo "content" | mcp-pipe run var-multi-pipe --config pipes.json --var PREFIX=ALPHA --var SUFFIX=OMEGA
```
**stdout:** `ALPHA:content:OMEGA`
✅ Both substitutions applied correctly.

## Test F — Env var fallback
```bash
FALLBACK_RATE=0.2 mcp-pipe run var-env-fallback-pipe --config pipes.json <<< "env fallback test"
```
**stdout:** Audit header (FALLBACK_RATE=0.2 from env used) ✅

## Test F2 — Missing env var → same bug as Test D
**stdout:** `argument --rate: invalid float value: '${FALLBACK_RATE}'`
❌ Same literal pass-through bug. **→ REPORT_038**

## Test F3 — `var-empty-default-fail-pipe`: fail-fast with declared empty default
```bash
echo "test" | mcp-pipe run var-empty-default-fail-pipe --config pipes.json
```
**stdout:** `--- [Context-Pipe: Variable Error] ---\nMissing pipe variable: TOKEN`
✅ The fail-fast declared-empty-default path works. No subprocess spawned.

## Test F4 — `var-empty-default-pass-pipe`: same empty default satisfied by --var
```bash
echo "test" | mcp-pipe run var-empty-default-pass-pipe --config pipes.json --var TOKEN=abc
```
**stdout:** `--- [Semantic-Sift Audit] ---` (sift ran successfully)
✅ Empty default satisfied by runtime injection.

## Test G — `--manifest` + `--var` combined
```bash
echo "test" | mcp-pipe run var-rate-pipe --config pipes.json --var RATE=0.3 --manifest .context-pipe/manifest-test.json
```
**Manifest (.context-pipe/manifest-test.json):**
```json
{
  "pipe": "var-rate-pipe",
  "vars": {"RATE": "0.3"},
  "status": "pass",
  "steps": [...]
}
```
✅ Manifest records resolved var values. Both features compose correctly.
