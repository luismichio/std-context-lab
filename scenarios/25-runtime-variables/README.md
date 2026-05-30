# Scenario 25 — Runtime Variable Injection (Phase 12A)

## Claim Under Test
Callers can supply `KEY=VALUE` variables at invocation time via `--var` (CLI), `vars` param (MCP tool), or `pipe()` kwarg (Python API). The orchestrator substitutes `${KEY}` tokens in `cmd` and `args` before spawning each node. Missing variables fail fast with a clear error. Env var fallback is honoured. Per-pipe `vars` defaults can be overridden by the caller.

## Feature Reference
- `context_pipe/orchestrator.py` — `_substitute_vars(text, vars)`
- `context_pipe/cli.py` — `--var KEY=VALUE` (repeatable)
- `context_pipe/server.py` — `pipe_run` `vars` param
- `context_pipe/api.py` — `pipe()` `vars` kwarg
- `pipes.json` `"vars"` defaults block

## What to Verify

### Test A — Basic `--var` substitution in `args`
```bash
echo "hello world" | mcp-pipe run var-rate-pipe --var RATE=0.3
```
Confirm sifted output at rate 0.3 (more aggressive than default 0.5).

### Test B — Default `vars` block used when no `--var` supplied
```bash
echo "hello world" | mcp-pipe run var-rate-pipe
```
Confirm sifted output at default rate 0.5 (from `"vars": {"RATE": "0.5"}`).

### Test C — Caller `--var` overrides pipe default
```bash
echo "hello world" | mcp-pipe run var-rate-pipe --var RATE=0.1
```
Confirm rate 0.1 (caller wins over default 0.5).

### Test D — Missing variable fail-fast (REPORT_038 — part of fail is broken)
```bash
echo "test" | mcp-pipe run var-missing-pipe
```
**Expected:** error BEFORE node spawn. **Actual:** `${REQUIRED_VAR}` passed as literal to subprocess (only vars declared with empty default trigger the fail-fast — see REPORT_038).

### Test H — Empty declared default fail-fast (positive path of REPORT_038)
```bash
echo "test" | mcp-pipe run var-empty-default-fail-pipe
```
Expect: `--- [Context-Pipe: Variable Error] ---\nMissing pipe variable: TOKEN` — no subprocess spawned.

### Test I — Empty default satisfied by --var
```bash
echo "test" | mcp-pipe run var-empty-default-pass-pipe --var TOKEN=abc
```
Expect: sift runs.

### Test J — `--manifest` + `--var` combined
```bash
echo "test" | mcp-pipe run var-rate-pipe --var RATE=0.3 --manifest manifest.json
```
Expect: manifest records `"vars": {"RATE": "0.3"}`.

### Test K — Multiple `--var` flags
```bash
echo "test" | mcp-pipe run var-multi-pipe --var PREFIX=ALPHA --var SUFFIX=OMEGA
```
Confirm both substitutions applied in `args`.

### Test F — Env var fallback
```bash
export FALLBACK_RATE=0.2
echo "test" | mcp-pipe run var-env-fallback-pipe
```
Confirm `${FALLBACK_RATE}` resolves to `0.2` from `os.environ`.

### Test G — Agent channel via `pipe_run` vars param
Use `pipe_run("var-rate-pipe", input_text)` with vars — confirm substitution applies.

## Expected Artefact
`run_runtime_variables.log`

## Dual-Channel Check
| Channel | Command |
|---|---|
| Shell | `echo "test" \| mcp-pipe run var-rate-pipe --var RATE=0.3` |
| Agent | `pipe_run("var-rate-pipe", text)` with vars param |
