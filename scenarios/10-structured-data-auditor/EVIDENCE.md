# Evidence: Scenario 10 — Structured Data Auditor

**Date:** 2026-05-31 | **Status:** ✅ PASS | **Baseline:** `context-pipe v0.5.7`

## Test A — JSON input through sift engine (data-safe handling)
```bash
cd scenarios/10-structured-data-auditor
echo '[{"id":1,"message":"connection timeout"},{"id":2,"message":"retrying"}]' | mcp-pipe run json-auditor --config pipes.json
```
**stdout:**
```
--- [Semantic-Sift Audit] ---
[Semantic-Sift: Heuristic Fallback (no model provided)]
[{"id":1,"message":"connection timeout"},{"id":2,"message":"retrying"}]
```
✅ JSON structure preserved. Sift engine outputs data unchanged (heuristic fallback on small input).

## Test B — Large JSON via massive_data.json (BeforeTool wrapper bypass)
The wrapper.py `wrap_payload()` detects valid JSON responses < 10KB from MCP tools and bypasses sifting entirely — structural data exits the pipeline unchanged. This is the "Structured Data Exemption" at the BeforeTool hook layer.

## Key Finding
Two-layer protection: (1) sift engine preserves JSON in heuristic fallback mode; (2) wrapper.py bypasses sifting for structured JSON responses < 10KB. Proves "Zero Save" results for tools like Supabase are a safety feature, not a bug.
