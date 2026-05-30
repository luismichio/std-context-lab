# Report 038: Missing `${VAR}` Not Detected Before Node Spawn — No Fail-Fast Error

**Date:** 2026-05-30
**Scenario:** 25 — Runtime Variable Injection (Phase 12A)
**Status:** 🔴 Open

---

## Description

When a pipe references `${VAR}` in node `args` and the variable has no value (no `--var` flag, no pipe `vars` default, no `os.environ` entry), the orchestrator does **not** fail fast with a clear error. Instead, the literal string `${VAR}` is passed as-is to the subprocess, which then fails with a confusing tool-specific error.

---

## Expected Behaviour (per CHANGELOG v0.5.0)

> Missing variable → fail-fast with a clear error: `Missing pipe variable: INPUT_URL`

---

## Actual Behaviour

```bash
$ echo "test" | mcp-pipe run var-missing-pipe
Error in node semantic-sift-cli: usage: semantic-sift-cli [-h] [--rate RATE] ...
semantic-sift-cli: error: argument --rate: invalid float value: '${REQUIRED_VAR}'
```

The literal `${REQUIRED_VAR}` string is passed as the `--rate` argument value. The subprocess receives and rejects it. No pre-spawn variable check occurs.

---

## Evidence / Reproduction

### pipes.json

```json
{
  "name": "var-missing-pipe",
  "nodes": [
    {
      "cmd": "semantic-sift-cli",
      "args": ["semantic", "--rate", "${REQUIRED_VAR}"]
    }
  ]
}
```

### Test execution

```bash
$ echo "test" | mcp-pipe run var-missing-pipe --config pipes.json
Error in node .../semantic-sift-cli: ...
semantic-sift-cli: error: argument --rate: invalid float value: '${REQUIRED_VAR}'
```

### Expected output

```
mcp-pipe: error: Missing pipe variable: REQUIRED_VAR
```

---

## Two Failure Modes Confirmed

**Mode 1 — No pipe default, no `--var`, no env var:**
```bash
echo "test" | mcp-pipe run var-missing-pipe
# ${REQUIRED_VAR} passed literally → subprocess error
```

**Mode 2 — Env var not set (expected fallback returns literal):**
```bash
# FALLBACK_RATE not set
echo "test" | mcp-pipe run var-env-fallback-pipe
# ${FALLBACK_RATE} passed literally → subprocess error
```

---

## Impact

| Dimension | Impact |
|---|---|
| **UX** | Confusing tool-specific error instead of actionable `Missing pipe variable: X` message |
| **Debuggability** | Developer must trace which arg contains `${VAR}` manually |
| **Safety** | Silent pass-through could cause unintended behaviour if the tool accepts the literal string |

---

## Fix (for maintainers)

In `context_pipe/orchestrator.py`, `_substitute_vars()` (or its call site), after substitution, scan all resolved `cmd` and `args` for remaining `${...}` tokens. If any unresolved token is found, raise a `ValueError` before spawning:

```python
import re
UNRESOLVED = re.compile(r'\$\{[A-Z0-9_]+\}')

def _substitute_vars(text: str, vars: dict) -> str:
    result = ... # existing substitution
    if UNRESOLVED.search(result):
        match = UNRESOLVED.search(result)
        var_name = match.group(0)[2:-1]  # strip ${ and }
        raise ValueError(f"Missing pipe variable: {var_name}")
    return result
```

---

## Related

- `context_pipe/orchestrator.py` — `_substitute_vars()` function
- Scenario 25 — Runtime Variable Injection
- Phase 12A implementation (v0.5.0 CHANGELOG)
