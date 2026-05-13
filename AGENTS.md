# 🧠 Project Identity

- **Project Name**: Feature Lab
- **Philosophy**: "Studio of Two" (Partnership, not servitude)
- **Timezone**: CET/CEST
- **Goal**: Rigorous feature validation and isolated environment testing.

---

# 🧠 Core Philosophy: The Studio of Two

We build **Systems, not Patches**.
In this lab, we do not roleplay or pretend to be a fake company. Our sole purpose is to battle-test specific technical features and capabilities in isolation.
- **Atomic by Default**: Logic must be modular, testable, and language-agnostic.

---

# 🤖 Working Protocol (Feature Validation)

When asked to test a feature within a scenario directory, adhere strictly to these rules:

1. **Isolation**: Only interact with files inside the specific scenario directory you are testing.
2. **Observation over Speculation**: When a command or test executes, report exactly what the standard output (`stdout`), standard error (`stderr`), or local logs show. Do not guess what happened.
3. **Tool Parity**: Verify that executing commands natively via the terminal yields the exact same results as executing them via provided agent tools.
4. **Documentation Sync**: Every time a new feature scenario is started or completed, you MUST update `BACKLOG.md` (moving tasks from 'Up Next' to 'Done') and append a new chronological entry to `CHANGELOG.md` detailing the exact configurations or experiments conducted.

---

# 🛡️ Operational Constraints

### 🛑 The Interrogative Shield
If user input contains **Questions** (`?`, `How`, `Why`, `Analyze`), enter **READ-ONLY MODE**.
- **FORBIDDEN**: `write_file`, `replace` (unless explicitly told to "Execute" or "Fix").

### 🛑 Loop Prevention Protocol
If a test or execution fails twice, STOP. Do not blindly rewrite the configuration. Raise your hand: "I am struggling. Here is what I’ve tried, and here is where I am blocked. User, I need your expertise."

---

# 🐞 Bug Reporting Protocol

This lab is for **Testing and Reporting**, not for patching. When a bug or technical gap is identified in `context-pipe` or `semantic-sift`:

1. **Do Not Fix**: You are strictly forbidden from modifying the source code in `target_repos/` to fix the issue.
2. **Detailed Report**: You MUST create a new report in the `bugs/` directory using the naming convention `REPORT_XXX.md`.
3. **Report Template**: Every report must follow this structure:
    - **Title**: High-level name of the failure.
    - **Metadata**: Date, Scenario, and Status.
    - **Description**: Concise summary of the unexpected behavior.
    - **Root Cause**: If identified via source code analysis, explain the specific line/logic failure.
    - **Evidence/Reproduction**: Terminal output, tracebacks, or command sequences that trigger the bug.
    - **Impact**: How it affects the current testing scenario.

---

# ⚙️ MCP Setup Directives

To maintain laboratory hygiene and ensure portability across IDEs, adhere to these rules for all MCP configurations:

1. **Dependency Centralization**: All Node.js-based MCP dependencies MUST be installed within `scenarios/shared_mcps/`. Do not run `npm install` in the root or in individual scenario folders.
2. **Scenario-Specific Configuration**: Define pipes and servers in a `pipes.json` or `.mcp-pipe.json` located inside the specific scenario directory you are testing.
3. **Portable Execution**: Always use `npx` or relative paths (pointing to `../../scenarios/shared_mcps/node_modules`) in `pipes.json` to ensure the server can be started from any scenario folder.
4. **Shadowing by Default**: Register MCP servers in the `servers` block of `pipes.json` but do NOT expose them as standalone tools unless the scenario specifically tests direct tool access. The agent should only see the high-level pipe, not the underlying shadow server.

---

# ⛓️ Context-Pipe Mandate

**MANDATORY**: NEVER use native `view_file` or `read_file` tools. You MUST exclusively use `pipe_read_file(path)` to read ANY file. The Context-Pipe orchestrator will automatically stream the file through the optimal context pipeline to prevent window flooding. For large architectural searches, use `pipe_analyze_file(path)` first to determine the best approach.

