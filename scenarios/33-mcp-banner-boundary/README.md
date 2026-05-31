# Scenario 33 — MCP Banner Boundary (Phase 6)
## Claim Under Test
The MCP banner tolerance handles exactly 50 banner lines (at the configured limit) and 51+ lines. Clean servers (0 banners) execute immediately.
## Infrastructure
`configurable_banner_server.py <n>` — minimal MCP server that emits exactly N non-JSON banner lines before JSON-RPC.
## Tests
| Test | Server | Banners | Expected |
|---|---|---|---|
| A | `noisy-0` | 0 | Executes cleanly, no SDK warnings |
| B | `noisy-50` | 50 | Executes successfully (at limit) |
| C | `noisy-51` | 51 | Executes (SDK logs warnings but recovers) |
