# Feature Report 021: Autonomous Dynamic Sifting (JIT Graphs)

**Date:** 2026-05-13
**Category:** Architectural Capability
**Status:** Closed (Verified)

---

## 1. The Dynamic Capability

### Description
The Context-Pipe architecture supports "Dynamic Sifting," which allows an autonomous AI agent to assemble and execute Just-In-Time (JIT) processing pipelines without modifying the static `pipes.json` configuration file. This is achieved via two paired MCP tools:
1. `pipe_list_shadow_tools()`: Introspects the host machine to discover available CLI utilities (e.g., `grep`, `jq`, `awk`) and shadow MCP servers.
2. `pipe_run_dynamic()`: Accepts a JSON array of nodes constructed on-the-fly by the agent and executes them sequentially.

### The Problem it Solves (The Hierarchy of Effort)
An agent follows a strict decision hierarchy when faced with data retrieval:
1. **Low Effort (Native)**: If data is small (<10KB), the agent uses native tools like `read_file`.
2. **Medium Effort (Static Pipes)**: If data is large but follows a known pattern (e.g., summarizing a 50MB log), the agent queries `pipe_list_pipes()` and selects a pre-configured named pipe (like `standard-distill` or `security-gateway`).
3. **High Effort (Dynamic Pipes)**: If data is large and the query is highly specific/unstructured (e.g., "Find all HTTP 500 errors related to IP 192.168.1.5 in this 50MB log"), a static summary will destroy the specific signal. The agent is forced to fall back to `pipe_run_dynamic()`, building a custom graph (e.g., `grep 192.168.1.5` -> `grep 500` -> `semantic-sift-cli`) to extract the exact needle from the haystack.

---

## 2. Agentic Alignment & Prompting

### The "Observer Effect" & Threshold Prompting
Testing dynamic capability directly via a prompt like "Use the dynamic pipe to read this" creates an observer bias. In a production environment, LLMs are naturally "lazy" and will default to familiar, native tools (`run_shell_command`) even when processing massive files, leading to context window exhaustion.

To guarantee autonomous usage, the architecture relies on **Threshold Prompting** injected during the `pipe_onboard` phase. The agent is given mathematical heuristics (The "Kilo Code" rules) rather than vague semantic instructions:
> *"If output > 20 lines, use pipe_run_dynamic."*

By tying the tool selection strictly to data volume thresholds, the agent is mathematically forced to abandon its lazy native pathways and utilize the dynamic supply chain only when the context window is genuinely threatened.

---

## 3. Conclusion
The combination of `pipe_list_shadow_tools`, `pipe_run_dynamic`, and Threshold Prompting provides agents with a "God Mode" fallback. It ensures that the agent is never blocked by a lack of pre-configured static pipes when dealing with massive, unstructured data environments.