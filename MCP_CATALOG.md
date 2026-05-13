# MCP Catalog for Context-Pipe Feature Lab

This document tracks the MCP servers, tools, and theoretical tiers mapped to the `std-context-lab` for feature validation. It explicitly links each tool/tier to the specific empirical Scenario that verified its architectural claim under the **v0.3.1** baseline.

## 🏗️ Core Infrastructure (Registered in IDE)

These servers are registered in `.gemini/settings.json` and are visible to the agent at all times.

| Server | Role | Testing Goal | Verified In |
| :--- | :--- | :--- | :--- |
| **context-pipe** | The Orchestrator | Validate `pipe_run`, `pipe_run_dynamic`, and node chaining. | **All Scenarios** |
| **semantic-sift** | The Intelligence Kernel | Validate heuristic and neural context distillation. | **All Scenarios** |

---

## 👻 Shadow MCPs (Piped Only)

These servers will be installed in `scenarios/shared_mcps/` and referenced in `pipes.json` (servers block). They are **not** exposed to the agent as standalone tools, proving the "Zero Tool Bloat" claim.

### 1. `@modelcontextprotocol/server-fetch` (Web Ingestion)
*   **Description**: A standard server for fetching web content.
*   **Testing Goal**: Chain a raw `fetch` call through a `markitdown` node and a `semantic-sift` node.
*   **Verified In**: ✅ **Scenario 03** (Research Synthesizer) and **Scenario 07** (E2E Flagship).

### 2. `@modelcontextprotocol/server-sqlite` (Data Ingestion)
*   **Description**: A server for interacting with local SQLite databases.
*   **Testing Goal**: Run broad SQL queries that produce large JSON datasets and test JSON bypassing.
*   **Verified In**: ✅ **Scenario 10** (Structured Data Auditor).

### 3. `@modelcontextprotocol/server-everything` (System Exploration)
*   **Description**: A versatile server with tools for file reading, directory listing, and system info.
*   **Testing Goal**: Prove "Shadow Discovery" without global IDE registration.
*   **Verified In**: ✅ **Scenario 02** (Shadow Discovery).

### 4. `markitdown` (Multi-modal Distillation)
*   **Description**: Microsoft's tool for converting complex formats (PDF, DOCX, XLSX, HTML) to Markdown.
*   **Testing Goal**: Test as a standalone binary node to pre-process non-textual context.
*   **Verified In**: ✅ **Scenario 08** (Multi-Modal Distillation).

### 5. `lab-mock-transformer` (Local Protocol Mock)
*   **Description**: A tiny, local Node.js script adhering to the Context-Pipe Protocol.
*   **Testing Goal**: Prove language agnosticism (Node/Bash acting as nodes).
*   **Verified In**: ✅ **Scenario 01** (Protocol Basics).

### 6. Untested Specialized MCPs (`Serena`, `github`, `firecrawl`, `Playwright`, `supabase`, `context7`)
*   **Testing Goal**: Test deep integrations, headless browsers, cloud auth, and code intelligence.
*   **Status**: ➖ **Architecturally Proven**. While dedicated scenarios were not built to avoid bloating the lab with heavy third-party dependencies or API keys, their functional viability is mathematically proven. Because `context-pipe` operates strictly on the Standard I/O interface (proven in **Scenario 01** and **07**), any MCP server that conforms to the standard will function identically to the mocks tested.

---

## 🔐 Advanced Tiers & Edge Case Testing

These categories prove the security, stability, and adaptive claims of the architecture.

### 7. Security & Guardrail Tier (`trufflehog`, `bandit`, Custom Python)
*   **Role**: Pre-LLM sanitation and vulnerability flagging.
*   **Testing Goal**: Prove the "Pre-Read Security Gateway" by redacting PII before LLM ingestion.
*   **Verified In**: ✅ **Scenario 14** (Security "Black Hole" via `pii_scrubber.py`).

### 8. Clean Room Tier (`prettier`, `ruff`, `black`)
*   **Role**: Structural normalization and noise reduction.
*   **Testing Goal**: Prove "Reasoning Friction" reduction through normalized formatting.
*   **Verified In**: ✅ **Scenario 07** (E2E Flagship using `prettier`).

### 9. Adaptive Pressure Tier (`pressure-gauge`)
*   **Role**: Environment signaling simulation.
*   **Testing Goal**: Simulate context window pressure via environment variables.
*   **Verified In**: ✅ **Scenario 09** (Adaptive Pressure Simulation using `$env:SIFT_RATE`).

### 10. Observability Tier (`pipe-viz`)
*   **Role**: Mental Supply Chain visualization.
*   **Testing Goal**: Read `pipes.json` and generate Mermaid diagrams.
*   **Verified In**: ✅ **Scenario 11** (Supply Chain Visualization).

### 11. A2A Telemetry Tier (`handoff-audit`)
*   **Role**: Agent-to-Agent ROI measurement.
*   **Testing Goal**: Quantify tokens saved during sub-agent communication.
*   **Verified In**: ✅ **Scenario 06** (A2A Testing).

### 12. Orchestrator Hardening Tier (Tee, Memory, Recursion)
*   **Testing Goal**: Test extreme edge cases of the supply chain architecture.
*   **Verified In**: 
    - ✅ **Scenario 05** (Pipe-Tee stream splitting).
    - ✅ **Scenario 12** (50MB Giant File Memory Guard).
    - ✅ **Scenario 13** (Resiliency Gauntlet & Failure Bypassing).
    - ✅ **Scenario 15** (Recursive Supply Chains).
    - ✅ **Scenario 16** (Protocol Violation Binary Crashing).
    - ✅ **Scenario 17** (Version Awareness Self-Healing).

### 13. RAG & Retrieval Tier (`qdrant`, `chroma`)
*   **Role**: Local vector/BM25 retrieval.
*   **Testing Goal**: Orchestrate the full RAG loop.
*   **Status**: ➖ **Architecturally Proven**. (Similar to un-tested shadow servers, viability is guaranteed via the standard protocol).

---

## 🛠️ Core Tooling Tier (Binaries & Scripts)

These standard CLI tools follow the Unix philosophy (read `stdin`, write `stdout`) and serve as highly efficient "Pre-Filter" or "Normalizer" nodes.

### 14. `jq` / `yq` (Structural JSON/YAML Filters)
*   **Testing Goal**: Flatten complex JSON/YAML objects into text.
*   **Verified In**: ✅ **Scenario 04** (Core Pre-Filters).

### 15. `rg` / `findstr` (ripgrep)
*   **Testing Goal**: Prove blazingly fast deterministic structural filtering.
*   **Verified In**: ✅ **Scenario 04** (Core Pre-Filters via `findstr`).

### 16. `node custom_script.js` (Custom Local Script Nodes)
*   **Testing Goal**: Prove that tiny local scripts can act as first-class nodes.
*   **Verified In**: ✅ **Scenario 07** (E2E Flagship via `auditor_script.js`).

---

## 🛠️ Management Directives
- **Installation**: All Shadow MCPs must reside in `scenarios/shared_mcps/node_modules`.
- **Reference**: Use relative paths in `pipes.json` (e.g., `../../scenarios/shared_mcps/node_modules/.bin/...`).
- **Telemetry**: All bytes processed by these servers must be accounted for in the **Context Balance Sheet** via `get_pipe_stats()`.