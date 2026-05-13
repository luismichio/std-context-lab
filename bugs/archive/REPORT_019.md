# Feature Request 019: Update Awareness & Self-Heal Suggestions

**Date:** 2026-05-13
**Scenario:** Environment Setup / Health Check
**Status:** Open (Design Phase)

---

## 1. Missing Version Awareness

### Description
The Context-Pipe system (orchestrator and refinery) is currently "silent" regarding its own version state. Users must manually track GitHub releases and re-run installation commands, which leads to confusion when bug fixes are released but not active in the user's environment.

### The Gap
When new code is pulled via Git, the virtual environment metadata (and the persistent MCP server process) remains on the old version until a manual `uv pip install -e` and a session restart occur. There is no automated signal to the user that they are running an outdated version.

### Proposed Solution
1. **GitHub Check**: Add logic to `pipe_verify` to query the latest release tag from the `context-pipe` GitHub repository.
2. **Comparison**: Compare the remote version against the local package version (via `importlib.metadata`).
3. **Actionable Alerts**: If an update is found, `pipe_verify` and `pipe_onboard` should output a clear warning:
   > ⚠️ **Update Available**: A newer version (v0.3.0) is available in target_repos. 
   > Run `uv pip install -e target_repos/context-pipe` and restart your IDE to apply.

---

## 2. Impact on UX
Significantly reduces "Setup Fatigue" and ensures that developers are always testing against the latest, most stable code without needing to constantly check logs or source files manually.
