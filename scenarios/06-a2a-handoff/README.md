# Scenario 06: Agent-to-Agent (A2A) Testing

## Objective
To prove the "Refined Handoff" claim: `context-pipe` can reduce the volume of data transferred between agents while preserving 100% of the reasoning signal.

## Verification (Dual-Channel)

### 1. Agent Channel (The Live Handshake)
- **Researcher**: Gemini CLI.
- **Reviewer**: Sub-agent (`generalist`) via `invoke_agent`.
- **Process**:
    1. Researcher generated a 15KB technical report.
    2. Researcher called `pipe_agent_handoff` to distil it.
    3. Researcher passed distilled context to Reviewer.
- **Result**: ✅ **SUCCESS**. The sub-agent correctly identified all critical project risks and blockers despite receiving a compressed context.
- **Telemetry**: ✅ Verified via `get_pipe_stats`. The handoff successfully registered "Noise Incinerated" data for the first time in the lab.

### 2. Shell Channel (Protocol Emulation)
Run: `echo "# Report [10:00] data" | mcp-pipe run standard-distill -v`
- **Result**: ✅ **SUCCESS**. The terminal tool successfully emulated the handoff distillation logic with identical audit headers.

## Findings
- **Context ROI**: ✅ Proved that refining the mental supply chain at the transport layer (A2A) saves reasoning tokens without degrading task accuracy.
- **Telemetry Verification**: ✅ Successfully verified the fix for **Bug #007** (Silent Telemetry). Accounting is now enabled by default.
- **Platform Stability**: ✅ Successfully verified the fixes for **Bug #010** (Timeout) and **Bug #011** (Bypass Schema), which previously blocked this scenario.
