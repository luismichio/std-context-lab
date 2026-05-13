# Bug Report 002: Gitignore Automation Gap

**Date:** 2026-05-11
**Scenario:** Environment Setup / Onboarding
**Status:** Closed (Verified)

---

## 1. Missing `.gitignore` Logic

### Description
The `pipe_onboard` tool successfully initializes the project structure but fails to protect its own artifacts. It does not automatically update the project's `.gitignore` file with the internal directories and telemetry files it generates.

### Verification (2026-05-11)
Successfully verified that `pipe_onboard` now calls `update_gitignore()` and correctly appends `.pipe_cache/`, `.pipe_identity`, and `.pipe_telemetry.json` to the workspace `.gitignore`.

### Artifacts Leaked (if not manually ignored)
- `.pipe_cache/`
- `.pipe_identity`
- `.pipe_telemetry.json`

### Root Cause
Analysis of `context_pipe/onboarding.py` reveals a total absence of `.gitignore` manipulation logic. In contrast, the sibling repository `semantic-sift` explicitly includes an `update_gitignore` function in its onboarding module.

---

## 2. Impact on Lab
User must manually maintain `.gitignore` to prevent machine-specific paths and local cache data from being committed to the repository, reducing the "plug-and-play" experience of the platform.
