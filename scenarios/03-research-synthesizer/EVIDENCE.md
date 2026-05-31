# Evidence: Scenario 03 — Research Synthesizer

**Date:** 2026-05-31 | **Status:** ✅ PASS | **Baseline:** `context-pipe v0.5.7`

## Fix Applied
`pipes.json` server command updated to absolute path — `mcp-server-fetch.exe` not on subprocess PATH.

## Test — MCP fetch → markitdown → sift
```bash
cd scenarios/03-research-synthesizer
echo "https://example.com" | mcp-pipe run research-pipe --config pipes.json
```
**stdout:**
```
--- [Semantic-Sift Audit] ---
📊 Reduction: -5600.0% (0.0KB -> 0.1KB)
🛡️ Guard: Trace-Verified (No Echo)
⚡ Latency: 16.7ms
[Semantic-Sift: Heuristic Fallback (no model provided)]
```
✅ MCP node no longer hangs (REPORT_041 fixed in v0.5.5). Full chain: `mcp-server-fetch` → `markitdown` (Python mode) → `semantic-sift-cli` completed successfully.

## Key Finding
**REPORT_041 fix confirmed for S03.** MCP node type launches and returns correctly from module context.
