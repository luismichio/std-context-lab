# Evidence: Scenario 15 — Recursive Supply Chains

**Date:** 2026-05-31 | **Status:** ✅ PASS | **Baseline:** `context-pipe v0.5.7`

## Test — Recursive pipe calls inner-distiller as subprocess node
```bash
cd scenarios/15-recursive-supply-chains
echo "ERROR: disk full on node-3. ERROR: disk full on node-3. WARN: retrying. INFO: done." | mcp-pipe run recursive-distill --config pipes.json
```
**stdout:**
```
--- [Semantic-Sift Audit] ---
📊 Reduction: 1.2% (0.1KB -> 0.1KB)
🛡️ Guard: Trace-Verified (No Echo)
⚡ Latency: 0.6ms
-----------------------------
ERROR: disk full on node-3...
```
**Wall time:** 4.3s (subprocess chain: outer mcp-pipe → inner mcp-pipe → semantic-sift-cli)

✅ **Pipeline Encapsulation confirmed.** `recursive-distill` successfully spawned `inner-distiller` as a subprocess node. Inner pipe ran `semantic-sift-cli logs` and returned sifted output. Outer pipe passed through result.

## Key Findings
- **Latency 0.6ms** = outer pipe's own overhead. Subprocess time (~4s) is wall time.
- **Echo Guard** (`Trace-Verified (No Echo)`) confirms no redundant re-sifting — already-sifted output passes through cleanly.
- **Modular design proven** — complex supply chains composable from simpler pipes without modifying inner logic.
