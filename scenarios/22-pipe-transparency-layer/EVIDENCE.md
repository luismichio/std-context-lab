# Scenario 22 — Evidence: Pipe Transparency Layer

**Date:** 2026-05-30 | **Status:** ✅ PASS (all tests)

## Test A — Compact logging
```bash
echo "..." | mcp-pipe run transparent-compact --config pipes.json 2>stderr.log
```
**stderr:**
```
[PIPE] ✓ ...semantic-sift-cli.exe | 105 → 256 chars (+151 | 143.8%) | 4.8s
[PIPE] ✓ ...semantic-sift-cli.exe | 256 → 271 chars (+15 | 5.9%) | 1.5s
```
✅ One exit line per node, no entry line.

## Test B — Verbose logging
**stderr:**
```
[PIPE] trigger:cli:run | → ...semantic-sift-cli.exe
[PIPE] trigger:cli:run | ✓ ...semantic-sift-cli.exe | 32 → 183 chars (+151 | 471.9%) | 2.9s
[PIPE] trigger:cli:run | → ...semantic-sift-cli.exe
[PIPE] trigger:cli:run | ✓ ...semantic-sift-cli.exe | 183 → 198 chars (+15 | 8.2%) | 1.3s
```
✅ Entry + exit lines per node, trigger field present.

## Test C — Custom prefix `[XPIPE]`
**stderr:**
```
[XPIPE] ✓ ...semantic-sift-cli.exe | 20 → 235 chars (+215 | 1075.0%)
```
✅ Custom prefix `[XPIPE]` overrides `[PIPE]`.

## Test D — Env var fallback (`PIPE_LOG_LEVEL=compact`)
```bash
env PIPE_LOG_LEVEL=compact mcp-pipe run no-logging-pipe --config pipes.json <<< "test"
```
**stderr:**
```
[PIPE] trigger:cli:run | ✓ ...semantic-sift-cli.exe | 18 → 232 chars (+214 | 1188.9%) | 1.5s
```
✅ Env var triggers logging on pipe with no `logging` block.

## Test E — Per-pipe verbose wins over `PIPE_LOG_LEVEL=compact`
```bash
env PIPE_LOG_LEVEL=compact mcp-pipe run transparent-verbose --config pipes.json <<< "test"
```
**stderr:** Full verbose entry+exit lines (not compact).
✅ Per-pipe `logging` block overrides env var.

## Test F — No logging, no env var → silent
**stderr:** *(empty)*
✅ Zero `[PIPE]` lines when no logging configured.

## Test G — Rust parity (`cpipe`)
```bash
echo "..." | cpipe run transparent-compact --config pipes.json 2>stderr.log
```
**stderr:**
```
[PIPE] ✓ ...semantic-sift-cli.exe | 23 → 53 chars (+30 | 130.4%) | 1.9s
[PIPE] ✓ ...semantic-sift-cli.exe | 53 → 53 chars (+0 | 0.0%) | 1.3s
```
✅ Rust cpipe emits identical `[PIPE]` compact lines.
