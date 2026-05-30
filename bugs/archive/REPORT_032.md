# Report 032: `pipe_read_file` Fails — Stale Extension File Not Regenerated After Update

**Date:** 2026-05-30
**Scenario:** Multi-Platform Parity / Update Workflow
**Status:** ✅ Resolved — lab_update.py fixed 2026-05-30

---

## Description

After updating context-pipe from v0.4.7 → v0.5.0, calling `pipe_read_file` in this pi.dev session produces a hard failure:

```
Command failed: "C:/Users/luism/Workbench/GitHub/std-context-lab/.venv/Scripts/python.exe"
  -m context_pipe.cli run auto --file
usage: mcp-pipe [-h] [--version] <command> ...
mcp-pipe: error: unrecognized arguments: --file
```

The tool appears to be registered and callable, but silently does nothing useful — exactly the class of failure described in REPORT_031.

---

## Root Cause

**The `.pi/extensions/context-pipe.ts` file in the project root was never regenerated after the v0.5.0 update.**

The file is the **v0.4.7 template** (containing all 5+1 REPORT_031 defects) — confirmed by cross-referencing its content against `git show v0.4.7:context_pipe/onboarding.py` lines 1242–1243.

The failure is produced by a **two-fault chain**:

### Fault 1 — Wrong `execute` signature (REPORT_031 Defect #1)

The stale extension registers `pipe_read_file` as:

```typescript
async execute(input) {
  const args = ["run", input.pipe_name || "auto", "--file", input.path];
  return callCli(args);
}
```

Per the pi `ExtensionAPI`, the first argument to `execute` is `toolCallId` (a string, e.g. `"call_abc123"`), **not** the user-supplied parameters. So:

- `input` = `"call_abc123"` (a string)
- `input.pipe_name` = `undefined` → defaults to `"auto"` ✓
- `input.path` = `undefined` → `["run", "auto", "--file", undefined].join(" ")` = `"run auto --file "` ← **no path**

### Fault 2 — `--file` is not a valid CLI flag

The v0.4.7 template uses `--file`, but the `mcp-pipe run` subcommand has **never** accepted `--file`. The correct flag is `--input-file` (and even that is not used by the v0.5.0 template, which reads the file in TypeScript and passes content via stdin instead).

The combination of both faults produces the exact observed error: `run auto --file` with no trailing path, which the CLI rejects immediately.

### Why the file was not regenerated

The `_inject_pi()` function in v0.5.0 uses `open(pi_extension_path, "w", ...)` — it **always overwrites** the file with the new fixed template. There is no `if not os.path.exists` guard. If `onboard` had been re-run, the file would have been fixed.

However, `lab_update.py` attempts to run onboarding at the end of its update cycle with:

```bash
python -m context_pipe.onboarding --environment Gemini
```

This command **failed** during the v0.5.0 update (observed and logged in CHANGELOG 2026-05-30):

```
Error: usage: onboarding.py [-h] [--target-dir TARGET_DIR] [environment]
onboarding.py: error: unrecognized arguments: --environment
```

The `--environment` flag was removed/renamed between v0.4.7 and v0.5.0 — the `lab_update.py` script uses the old calling convention. Because onboarding failed, `_inject_pi()` was never called, and the stale extension file was never overwritten with the fixed v0.5.0 template.

---

## Evidence / Reproduction

### 1. Stale file confirmed — matches v0.4.7 template

```bash
# v0.4.7 onboarding template (from git history)
$ git show v0.4.7:context_pipe/onboarding.py | grep -n "execute(input\|--file"
1242:    async execute(input) {
1243:      const args = ["run", input.pipe_name || "auto", "--file", input.path];

# Live file in project root — IDENTICAL to v0.4.7 template
$ grep -n "execute(input\|--file" .pi/extensions/context-pipe.ts
41:    async execute(input) {
42:      const args = ["run", input.pipe_name || "auto", "--file", input.path];
```

### 2. `--file` has never been a valid CLI flag

```bash
$ python -m context_pipe.cli run --help
usage: mcp-pipe run [-h] [--config PATH] [--input-file PATH] ...
# No --file flag — always been --input-file
```

### 3. `undefined` propagation confirmed (Node.js)

```bash
$ node -e "
const args = ['run', undefined || 'auto', '--file', undefined];
console.log('joined:', args.join(' '));
"
joined: run auto --file      # ← undefined becomes empty, --file has no value
```

### 4. Onboarding failure during update (CHANGELOG 2026-05-30)

```
Error: usage: onboarding.py [-h] [--target-dir TARGET_DIR] [environment]
onboarding.py: error: unrecognized arguments: --environment
```

The `--environment` flag was removed in v0.5.0. `lab_update.py` still uses the old calling convention, so `_inject_pi()` was never triggered.

### 5. v0.5.0 onboarding command signature (confirmed)

```bash
$ python -m context_pipe.onboarding --help
usage: onboarding.py [-h] [--target-dir TARGET_DIR] [environment]
# Correct call: python -m context_pipe.onboarding pi
# (positional argument, no --environment flag)
```

---

## Impact

| Dimension | Impact |
|---|---|
| **Functionality** | `pipe_read_file` is the primary mandatory tool — it is completely broken |
| **Context safety** | Every file read falls through to the native `read` tool, flooding the context window |
| **REPORT_031 status** | All 5+1 defects appear "fixed" in `onboarding.py` source but are **live and active** in the deployed extension |
| **Silent failure** | The tool registers without error; the failure only surfaces at call time — hardest class of bug |
| **Update workflow** | `lab_update.py` silently swallows the onboarding failure — no warning is emitted to the user |

---

## Fix Required (for maintainers, not this agent)

Two independent fixes are needed:

### Fix A — `lab_update.py`: Update the onboarding call to use the v0.5.0 CLI signature

```python
# Old (broken):
subprocess.run([python, "-m", "context_pipe.onboarding", "--environment", "Gemini"])

# Correct (v0.5.0):
subprocess.run([python, "-m", "context_pipe.onboarding", "pi",
                "--target-dir", str(project_root)])
```

Also add error checking: if onboarding fails, print a **visible warning** rather than continuing silently.

### Fix B — `lab_update.py` or `context-pipe`: Detect and warn about stale extension files

After updating, check if existing `.pi/extensions/context-pipe.ts` contains a version comment or known-bad strings (e.g. `--file`, `execute(input)`) and warn the user that a re-onboard is needed. Ideally, `_inject_pi()` should embed a `// context-pipe v{VERSION}` comment in the generated file header to enable staleness detection.

---

## Immediate Workaround

Re-run onboarding manually with the correct v0.5.0 signature:

```bash
python -m context_pipe.onboarding pi --target-dir .
```

This will overwrite `.pi/extensions/context-pipe.ts` with the v0.5.0 fixed template.

---

## Related

- **REPORT_031** (archived) — Original 5-defect report on the buggy template; fixes are correct in source but not deployed
- **REPORT_030** (archived) — Original pi.dev integration feature request
- CHANGELOG 2026-05-30 — Update session where onboarding silently failed
- Stale file: `.pi/extensions/context-pipe.ts` (project root)
- Source fix: `target_repos/context-pipe/context_pipe/onboarding.py` `_inject_pi()` (correct in v0.5.0)
- Update script: `lab_update.py` (incorrect onboarding call on final step)
