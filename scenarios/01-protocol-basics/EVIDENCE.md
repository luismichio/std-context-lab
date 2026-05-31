# Evidence: Scenario 01 — Protocol Basics

**Date:** 2026-05-31 | **Status:** ✅ PASS | **Baseline:** `context-pipe v0.5.7`

## Note
Must run from the scenario directory — `transformer.js` is referenced by relative path in `pipes.json`.

## Test — Node.js transformer → semantic-sift
```bash
cd scenarios/01-protocol-basics
echo "ERROR: test log line. WARNING: another line. INFO: all good." | mcp-pipe run basics-pipe --config pipes.json
```
**stdout:**
```
--- [Semantic-Sift Audit] ---
📊 Reduction: 1.2% (0.1KB -> 0.1KB)
🛡️ Guard: Trace-Verified (No Echo)
⚡ Latency: 0.6ms
-----------------------------
[LAB-TEST-TRANSFORMED] ERROR: test log line. WARNING: another line. INFO: all good.
```
✅ `[LAB-TEST-TRANSFORMED]` prefix confirms `transformer.js` ran. Multi-language orchestration (Node.js → Rust/Python) confirmed working.
