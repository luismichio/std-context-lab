# Bug Report 029: Failing Global Hooks (ctx-m)

**Date:** 2026-05-24
**Scenario:** Hook Execution
**Status:** Invalid (Restored to context-mode)

---

## 1. Command Not Found: `ctx-m`

### Description
The Gemini CLI reports failures for the `ctx-m` command during various hook events (`BeforeTool`, `AfterTool`, etc.).

### Evidence
```
ℹ ctx-m : The term 'ctx-m' is not recognized as the name of a cmdlet, function, script file, or operable program.
  At line:1 char:1
  + ctx-m g beforetool; if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
```

### Root Cause
A global Gemini configuration (located at `C:\Users\luism\.gemini\settings.json`) has registered hooks that attempt to call `ctx-m`. This tool or alias is either missing from the system PATH or is not correctly initialized in the hook's shell environment.

### Impact on Lab
While not directly related to `context-pipe`, these failing global hooks generate noisy error messages and can obscure legitimate `cpipe` failures.

---

## 2. Recommended Fix
Verify the installation of the tool providing `ctx-m` (likely `context-mode` extension) or remove the global hook definitions if they are no longer needed.
