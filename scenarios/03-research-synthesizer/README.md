# Scenario 03: Research Synthesizer

## Objective
To validate a complex, multi-node mental supply chain that chains an MCP server, a binary converter, and a neural refinery.

## Setup
- **Pipeline**: `research-pipe`
    - Node 1: `mcp:fetch/fetch` (Python-based MCP Server)
    - Node 2: `markitdown` (Binary document converter)
    - Node 3: `semantic-sift-cli semantic` (Heuristic/Neural refinery)

## Execution
Run the following command from the root:
```bash
echo "https://example.com" | mcp-pipe run research-pipe -v
```

## Findings
- **CLI Server Registry**: ✅ **VERIFIED FIXED**. The terminal `mcp-pipe run` command now successfully passes the shadow server registry to the orchestrator, allowing the `fetch` node to execute without absolute path hacks.
- **Audit Header Resiliency**: ✅ **VERIFIED FIXED**. The orchestrator now generates correct telemetry headers (e.g., `📊 Context: 185.0% Augmentation`) even when nodes return complex outputs or fallbacks.
- **Supply Chain Success**: ✅ The data flowed through the entire chain, from raw URL to a distilled context payload.
- **Latency**: ⚠️ The total pipe latency was ~5s, primarily due to the cold-start time of the fetcher and sifter.
