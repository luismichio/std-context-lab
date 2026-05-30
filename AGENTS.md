<!-- CPP_SECTION_START:mandate -->
#  CRITICAL INSTRUCTION: FILE I/O OVERRIDE
**WARNING**: Using native file readers will flood the context window and destroy the session.

- **REQUIRED**: Standard practice in this Studio is to use `pipe_read_file(path)` and `pipe_analyze_file(path)` for all large local file reads (>1KB).
## 1. File & Large-Output I/O
- **FORBIDDEN TOOLS**: `view_file`, `grep_search`, `list_directory`. Do NOT use these under any circumstances for outputs > 1KB.
- **REQUIRED TOOLS**: You MUST exclusively use `pipe_read_file(path)` and `pipe_analyze_file(path)` for ALL local file reads.
- NEVER read raw outputs from `web_search` or search tools. Pipe them through `pipe_run("rerank-and-sift", raw_output)`.
- For ANY tool output exceeding 100 lines (logs, API responses, search results), route through a context pipe before presenting to the user.

## 2. Named Pipes  When to Use `pipe_run`
- Call `list_pipes()` first to see all available named pipes in this project.
- Use `pipe_run(pipe_name, input_text)` when:
  - A named pipe exists that matches the content type (e.g. `semantic-refinery` for code, `standard-distill` for logs).
  - You want a reproducible, audited transformation that is tracked in the Balance Sheet.
- After every `pipe_run`, the audit header shows compression ratio and latency  include this in your response to the user.

## 3. Dynamic Pipes  When to Use `pipe_run_dynamic`
- Use `pipe_run_dynamic(nodes_json, input_text)` when no named pipe fits and you need to compose a one-off processing graph.
- **Workflow** (always follow this sequence):
  1. Call `pipe_list_shadow_tools()` to discover available nodes (configured pipes + PATH tools like `jq`, `rg`, `markitdown`).
  2. Construct a `nodes_json` array from those capabilities.
  3. Call `pipe_run_dynamic(nodes_json, input_text)`.
- **Rules**:
  - Every `nodes_json` array MUST end with `{"cmd": "semantic-sift-cli", "args": ["semantic"]}` or equivalent sifting node.
  - Shell utilities (`grep`, `awk`, `jq`, `rg`, etc.) require `allow_shell=True`  only use when the final node is a sifter.
  - Never put shell metacharacters (`|`, `;`, `&`, `$`) in a `cmd` value - use `args` instead.
- **Example**  extract ERROR lines then distil:
  ```json
  [{"cmd": "grep", "args": ["ERROR"]}, {\"cmd\": "semantic-sift-cli", "args": ["logs"]}]
  ```

## 4. A2A Agent Handoff  When to Use `pipe_agent_handoff`
- ALWAYS call `pipe_agent_handoff(output, from_agent="X", to_agent="Y")` when passing one agent's output to another agent's context window.
- This prevents context flooding at multi-agent boundaries regardless of framework (CrewAI, ADK, LangGraph, custom).
- If you know the content type, pass `pipe_name` explicitly (e.g. `pipe_name="semantic-refinery"`). Otherwise omit it and routing is automatic.

## 5. Observability  Balance Sheet
- Call `get_pipe_stats()` at any time to see cumulative ROI: chars saved, chars added, avg latency, total events.
- After significant processing sessions, proactively report the Balance Sheet to the user so they can see the value delivered.
<!-- CPP_SECTION_END:mandate -->

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
4. **Documentation & Evidence Sync**: Every time a new feature scenario is started or completed, you MUST:
    - Update `BACKLOG.md` (moving tasks from 'Up Next' to 'Done').
    - Append a new chronological entry to `CHANGELOG.md` detailing the exact configurations or experiments conducted.
    - **Create or update `EVIDENCE.md`** inside the scenario directory, containing the exact execution command and the resulting output as empirical proof of success.

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

## ⛓️ Context-Pipe Mandate

**MANDATORY**: NEVER use native `view_file` or `read_file` tools. You MUST exclusively use `pipe_read_file(path)` to read ANY file. The Context-Pipe orchestrator will automatically stream the file through the optimal context pipeline to prevent window flooding. For large architectural searches, use `pipe_analyze_file(path)` first to determine the best approach.

**ONBOARDING RULE**: If `context-pipe` (CPP) is available, you MUST ONLY run `pipe_onboard`. Do NOT run `sift_onboard`, as CPP handles the registration of the semantic-sift kernel as a shadow node. Running both leads to redundant hook configurations and telemetry duplication.

**UPDATE WORKFLOW**: When updating core tools in `target_repos/`, use the unified update script located in the root directory:
1. Run `python lab_update.py` from the project root.
   - This script automatically pulls source updates, fetches binaries, detects version mismatches, and rebuilds the Rust core if necessary.
2. Verify the final versions in `LAB_STATUS.md`.


