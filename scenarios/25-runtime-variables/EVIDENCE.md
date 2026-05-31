# Scenario 25 — Evidence: Runtime Variable Injection

**Date:** 2026-05-31 | **Status:** ✅ PASS (all tests — REPORT_038 confirmed fixed in v0.5.3)

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

## Test D — Missing variable fail-fast ✅ FIXED (REPORT_038 closed v0.5.3)
```bash
echo "test" | mcp-pipe run var-missing-pipe --config pipes.json
```
**Actual (v0.5.7):**
```
ValueError: Missing pipe variable: REQUIRED_VAR
```
✅ Fail-fast before spawn. Undeclared `${REQUIRED_VAR}` raises error immediately.

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

## Test F2 — Missing env var ✅ FIXED (REPORT_038)
**Actual (v0.5.7):** `ValueError: Missing pipe variable: FALLBACK_RATE`
✅ Same fail-fast applies to undeclared env var fallbacks.

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
