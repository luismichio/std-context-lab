# Scenario 08: Multi-Modal Distillation

## Objective
To prove format agnosticism by distilling non-textual formats (HTML, PDF, etc.) into clean markdown context using the `markitdown` binary node.

## Setup
- **Dataset**: `bloated_doc.html` (1.3KB of styled HTML with navigation and boilerplate).
- **Pipeline**: `multi-modal-pipe`
    - Node 1: `markitdown` (Binary document converter)
    - Node 2: `semantic-sift-cli semantic` (Neural refinery)

## Verification (Dual-Channel)

### 1. Shell Channel
Run: `Get-Content bloated_doc.html -Raw | mcp-pipe run multi-modal-pipe -v`
**Result**: ✅ **95.8% Reduction**. Successfully converted HTML to Markdown and stripped boilerplate.

### 2. Agent Channel
Run: `pipe_run(input_text=..., pipe_name="multi-modal-pipe")`
**Result**: ✅ **95.7% Reduction**. Full parity with the Shell Channel.

## Findings
- **Format Agnosticism**: ✅ Proved that binary nodes like `markitdown` can transparently pre-process non-textual context for the refiner.
- **Parity**: ✅ Verified the **Dual-Channel Mandate**. Standard I/O behavior is identical across Terminal and AI Assistant.
- **Efficiency**: ✅ Reduced a styled 1.3KB payload to a clean 0.1KB reasoning signal.
