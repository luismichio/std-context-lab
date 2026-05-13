# Regression Testing Standard Operating Procedure (SOP)

This document defines the strict protocol for re-verifying the `std-context-lab` scenarios when a new version of `context-pipe` or `semantic-sift` is released upstream, or when testing in a new IDE environment.

## 1. The Core Principle: Explicit Version Tracking
**A simple checkbox is meaningless.** If we test OpenCode to `v0.4.0` but Gemini stays at `v0.3.1`, writing a simple `✅` under both hides the truth and creates regression drift. 

Therefore, the `LAB_STATUS.md` matrix MUST use the exact version string (e.g., `v0.3.1`) to explicitly state the code version that was empirically executed and passed in that specific environment column.

## 2. The Strict Regression Procedure
To retest the ecosystem after an update or when moving to a new IDE:

### Step 1: Environment Update (Run Once)
Pull the latest code and refresh the virtual environment.
```bash
# Update local repositories
cd target_repos/context-pipe && git fetch && git pull
cd ../semantic-sift && git fetch && git pull
cd ../../

# Refresh editable installations
uv pip install -e target_repos/context-pipe
uv pip install -e target_repos/semantic-sift[neural]
```

### Step 2: Health Check (Run per Environment)
Run the native verification tool via the MCP server or CLI within the specific environment.
```python
# Agent Channel
pipe_verify()
```

### Step 3: Comprehensive Execution
The agent or user must explicitly execute the scenarios listed in `SCENARIOS.md` within the target environment. **If a scenario is not explicitly executed and tested, it is NOT verified.** There are no shortcuts or assumptions of parity.

### Step 4: Status Update
- **If a scenario passes**: Update its specific cell in the `LAB_STATUS.md` matrix to the exact version string (e.g., `v0.4.0`) for that environment. Update its `Last Verified In` tag in `SCENARIOS.md`.
- **If a scenario fails**: Log a new bug report in `bugs/REPORT_XXX.md` noting the specific regression, environment, and version (e.g., "Fails in Cursor only on v0.4.0"). Change the corresponding cell in `LAB_STATUS.md` to `❌ (v0.4.0)`. 
- **If a scenario is skipped/untested**: Its cell in the matrix must remain at its older verified version (e.g., leaving it at `v0.3.1` while others move to `v0.4.0`) or remain as `-` if never tested.
