# Evidence: Scenario 07 — Mental Supply Chain (E2E Flagship)

**Date:** 2026-05-31 | **Status:** ✅ PASS | **Baseline:** `context-pipe v0.5.7`

## Fix Applied
`pipes.json` server command updated to absolute path — `mcp-server-fetch.exe` not on subprocess PATH.

## Test — 5-node E2E pipeline
```bash
cd scenarios/07-mental-supply-chain
mkdir -p .tee
echo "https://example.com" | mcp-pipe run e2e-supply-chain --config pipes.json
```
**stdout:**
```
[Ship-It Mock] Successfully created ticket 'shipped_issue.md' with 149 characters.
```
✅ All nodes executed in sequence:
1. `mcp:fetch/fetch` — fetched example.com via MCP
2. `markitdown` — converted HTML → Markdown (Python mode)
3. `findstr` — pass-through filter
4. `prettier` — Markdown formatter (Node.js via absolute path)
5. `semantic-sift-cli` — sifted with tee snapshot to `.tee/`
6. `auditor_script.js` — Node.js auditor
7. `ship_it_mock.js` — created `shipped_issue.md`

## Key Finding
**REPORT_041 fix confirmed for S07.** Full E2E orchestration across MCP servers, Node.js scripts, and Rust sift engine works correctly on v0.5.7.
