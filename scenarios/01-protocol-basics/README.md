# Scenario 01: Protocol Basics

## Objective
To verify the fundamental Context-Pipe Protocol (CPP) contract: language-agnostic tools communicating via `stdin` and `stdout`.

## Setup
- **Language**: Node.js
- **Tool**: `transformer.js` (A simple script that appends `[LAB-TEST-TRANSFORMED]` to every line).
- **Pipeline**: `basics-pipe`
    - Node 1: `transformer.js` (JavaScript)
    - Node 2: `semantic-sift-cli` (Python/Rust)

## Execution
Run the following command from the scenario directory:
```bash
Get-Content sample.log | mcp-pipe run basics-pipe
```

## Findings
- **Language Agnosticism**: ✅ The Python-based orchestrator successfully spawned a Node.js process and piped its output into a Python/Rust refinery.
- **Protocol Fidelity**: ✅ The `stdin`/`stdout` streams were handled without data corruption or encoding issues.
- **Refinery Integration**: ✅ `semantic-sift` correctly distilled the already-transformed lines, proving that "Sifting" works on pre-processed context.
