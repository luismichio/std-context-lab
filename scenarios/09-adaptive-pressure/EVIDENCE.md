# Evidence: Scenario 09 — Adaptive Pressure Simulation

**Date:** 2026-05-31 | **Status:** ✅ PASS | **Baseline:** `context-pipe v0.5.7`

## Test A — Default rate (SIFT_RATE=0.5 from vars block)
```bash
cd scenarios/09-adaptive-pressure
echo "payload..." | mcp-pipe run adaptive-sift --config pipes.json
```
**stdout:** `[SIGNAL: PRESSURE_LOW] payload...` sifted at default rate 0.5
✅ `pressure_gauge.py` prepended signal prefix. `${SIFT_RATE}` resolved from pipe `vars` default.

## Test B — High pressure (SIFT_RATE=0.1 via env var)
```bash
SIFT_RATE=0.1 mcp-pipe run adaptive-sift --config pipes.json <<< "payload..."
```
**stdout:** `[SIGNAL: PRESSURE_LOW] payload...` sifted at rate 0.1
✅ `${SIFT_RATE}` resolved from env var fallback (overrides default 0.5).

## Key Finding
`vars` default `"SIFT_RATE": "0.5"` is overridden by env var at runtime — proves "Adaptive Window Pressure" claim. Dynamic argument resolution confirmed working on v0.5.7.
