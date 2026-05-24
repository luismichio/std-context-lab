# Bug Report 028: Persistent PowerShell Parser Error (v0.4.5)

**Date:** 2026-05-24
**Scenario:** Environment Setup / Hook Execution
**Status:** Closed (Verified)

### Verification (2026-05-24)
The standard names were restored and the `&` operator was manually injected into `.gemini/settings.json`. The PowerShell parser error is resolved. v0.4.5 source contains the automated fix for future onboards.


---

## 1. Regression: Missing Call Operator (CRITICAL)

### Description
Despite the fixes in `v0.4.5`, command hooks in the Gemini CLI continue to fail on Windows with a PowerShell parser error: `Unexpected token '-W'`. 

### Evidence
- **Source Code (v0.4.5)**: `build_runtime_hook_command` now correctly prepends `& ` on Windows.
- **Local State**: `.gemini/settings.json` still contains hooks **without** the `&` operator.
- **Root Cause**: The `pipe_onboard` tool failed to update the existing hooks because the existing hooks used different names (e.g., `"cpipe beforetool"`) than what is currently defined in the `v0.4.5` source code (`"context-pipe"`). The deduplication/replacement logic failed to identify them as the same tool.

### Impact on Lab
All Gemini CLI hooks are broken on Windows until `settings.json` is manually repaired.

---

## 2. Recommended Fix
Users must manually delete the broken hook blocks from `.gemini/settings.json` and re-run `python lab_update.py` to ensure the modern, fixed hooks (with the `&` operator) are injected.
