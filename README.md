# std-context-lab

This repository is an isolated sandbox to battle-test the [context-pipe](https://github.com/luismichio/context-pipe) and [semantic-sift](https://github.com/luismichio/semantic-sift) tools.

## 🚀 Agnostic Setup Instructions

To initialize this lab on your local machine, follow these steps. This setup follows the **Sovereign Dual-Repo Pattern**.

### 1. Prerequisites
- [uv](https://github.com/astral-sh/uv) (Python package manager)
- [Rust / Cargo](https://rustup.rs/) (For native sifting)
- [Node.js / npm](https://nodejs.org/) (For shadow MCPs)

### 2. Environment Initialization
Create a shared virtual environment and install the target repositories in editable mode:
```bash
# Create venv
uv venv

# Install target repos in editable mode with neural extras
uv pip install -e "target_repos/context-pipe"
uv pip install -e "target_repos/semantic-sift[neural]"

# Install common lab utilities
uv pip install yq markitdown
```

### 3. Compile Native Sidecar
The heuristic refinery requires the compiled Rust core:
```bash
cd target_repos/semantic-sift/crates/sift-core
cargo build --release
```

### 4. Install Shadow MCPs
```bash
cd scenarios/shared_mcps
npm install
```

### 5. IDE Configuration
This lab is environment-agnostic. To use the tools:
- **MCP Registration**: Point your AI assistant (Gemini CLI, Cursor, VS Code) to the `context_pipe.server` and `semantic_sift.server` modules using the Python interpreter in `.venv/Scripts/python`.
- **Hooks**: For transparent sifting, register `target_repos/context-pipe/pipe_hook.py` as a post-tool execution hook in your IDE settings.

## 🖥️ IDE/Environment Onboarding SOP

When opening this lab in a new IDE (Cursor, VSCode, etc.), follow this protocol to ensure full feature parity:

1. **Set the Interpreter**: Select the `.venv` at the repository root as your IDE's Python interpreter.
2. **Register MCPs**: Register the `context-pipe` and `semantic-sift` servers in your IDE settings using the venv python path and the `-m <module>.server` arguments.
3. **Run Onboarding**: Ask your AI assistant to run `pipe_onboard(environment="NAME")`. This automates hook injection for your specific platform.
4. **Verify Health**: Run `pipe_verify()` to confirm core tools are connected and the refinery is responding.
5. **Update Matrix**: Open `LAB_STATUS.md` and mark **Scenario 01** as verified for your current IDE once the basic pipe run succeeds.

## 🧪 Testing Scenarios
All 17 technical claims and battle-tested use cases are consolidated in [SCENARIOS.md](./SCENARIOS.md). 

Detailed setup scripts and artifacts for each individual experiment are located in the `/scenarios` directory. Each scenario folder also includes its own `README.md` containing deep technical execution steps and localized findings.

## 🔄 Regression Testing
When a new version of the upstream tools is released, we follow a strict re-verification protocol. See the [Regression Testing SOP](./REGRESSION_SOP.md) for details on how to test updates against the "Core Four" scenarios to maintain the `LAB_STATUS.md` baseline.

## 🐞 Bug Reporting
Found a bug? Do not patch the `target_repos/`. Instead, create a standardized report in the `/bugs` directory following the protocol in `AGENTS.md`.
