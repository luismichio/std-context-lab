# Feature Request 025: Project-Wide Awareness & Hybrid Mandates

**Date:** 2026-05-24
**Category:** Architectural Capability / UX
**Status:** Closed (Verified)

---

## 1. The "Single-Environment" Silo (The Problem)

### Description
The `pipe_onboard` tool currently operates in a "Single-Environment" silo. If a user runs `pipe_onboard --environment Gemini`, the tool assumes only Gemini CLI needs configuration. It ignores other IDE signatures (like `.cursorrules` or `.clinerules`) present in the same project root.

### Risks
1.  **Broken Habits**: If an agent is "Shielded" in Gemini but "Unshielded" in Cline within the same repo, it will fail to develop the necessary proactive habits (e.g., using `pipe_read_file`) required for the unshielded environment.
2.  **Configuration Drift**: Onboarding in one IDE does not protect the context when the same project is opened in another.
3.  **Instruction Vacuum**: "Shielded" environments currently receive ZERO mandates, which makes the system entirely reliant on hooks. If a hook fails or is bypassed, there is no instructional fallback for the agent.

---

## 2. Proposed Solution: The Hybrid Strategy

### A. Two-Tiered Mandate System
Replace the current "all-or-nothing" mandate injection with a tiered approach:

*   **Tier 1: Universal Baseline (All Platforms)**
    *   A concise "Golden Rule" established in `AGENTS.md` and all detected rule files.
    *   *Content*: "Standard practice in this Studio is to use `pipe_read_file` for all large I/O."
*   **Tier 2: Technical Manual (Unshielded Platforms Only)**
    *   The full technical specification (Named Pipes, Dynamic Graphs, A2A Handoff).
    *   Automatically appended to Tier 1 when an unshielded IDE is detected.

### B. Project Horizon Scanning
The onboarding tool should transition from being **Environment-Centric** to **Project-Centric**:
1.  **Scan for Signatures**: Automatically detect `.cursor/`, `.clinerules`, `.windsurfrules`, `.agents/`, etc.
2.  **Multi-Target Injection**: In a single run, update ALL detected instruction targets with the appropriate Tier (1 or 2).
3.  **Platform Detection in Mandates**: Ensure the mandates use the correct tool names for each specific IDE target discovered.

---

## 3. Benefits
- **Habit Consistency**: The agent develops the same "Context-Safe" behavior regardless of which IDE is currently active.
- **Self-Healing Infrastructure**: Tier 1 acts as a "Manual Safety" fallback for Tier 2's automated hooks.
- **Developer Efficiency**: `lab_update.py` becomes a "One Command to Rule Them All" that synchronizes the entire multi-IDE workspace in one pass.
