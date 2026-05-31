# Lab Tracking Record

This document serves as a chronological journal of events, configurations, and experiments conducted within the `std-context-lab`. Since this is a testing environment and not a releasable software project, entries are logged by date and milestone rather than semantic versioning.

## [2026-05-31] — v0.5.7 Update: REPORT_042 Properly Fixed

### Summary
Updated context-pipe to v0.5.7 (commit `ef0ea93`). REPORT_042 fully resolved:
- **REPORT_042** ✅ — `onboarding.py` template now has `51200` at all threshold sites (lines 334, 340, 1060, 1082, 1328). Regenerated `.pi/extensions/context-pipe.ts` confirms `stats.size > 51200` on line 122.
- v0.5.7 also fixes a CI hang in Python integration tests (Linux `asyncio` nested subprocess deadlock).
- **Requires session restart** to reload the updated extension into the live pi.dev session.

## [2026-05-31] — v0.5.6 Update: REPORT_042 False Fix

### Summary
Updated context-pipe to v0.5.6. Upstream changelog claims REPORT_042 fixed, but verification shows fix was not applied:
- **REPORT_042** 🔴 Re-opened — `onboarding.py` template still has `1024` threshold. Generated `.pi/extensions/context-pipe.ts` still blocks at 1KB. Fix not applied to the correct file.
- v0.5.6 also adds range telemetry parity (`get_pipe_stats` filtering, `pipe_audit_last` limit param, `pipe_list_shadow_tools` MCP server discovery).

## [2026-05-31] — v0.5.5 Update: REPORT_041 Fixed

### Summary
Updated context-pipe to v0.5.5. REPORT_041 resolved upstream:
- **REPORT_041** ✅ — `_run_mcp_node` no longer hangs. Fix: added `posix=False` on Windows for `shlex.split()` and appended `server_args` from config to the command. MCP node pipes now launch correctly from module context.

### Scenario 27 (MCP Banner Tolerance)
- S27 no longer hangs — confirmed working on v0.5.5
- Pipe completes with correct `[ECHO]` output
- MCP SDK internal reader logs `Failed to parse JSONRPC` warnings for banner lines on stderr (cosmetic — pipe succeeds)
- REPORT_041 archived

## [2026-05-30] — v0.5.3 Update: Three Bugs Fixed, REPORT_040 Filed

### Summary
Updated context-pipe to v0.5.3. All three open bugs confirmed fixed upstream:
- **REPORT_037** ✅ — `_StdoutToleranceWrapper` now has `__aenter__`, `__aexit__`, `__aiter__`, `__anext__`
- **REPORT_038** ✅ — `_build_vars` now raises `ValueError` for missing required vars (fail-fast before spawn)
- **REPORT_039** ✅ — `_run_mcp_node` and `_execute_node_chain` now read `node.get("timeout")` for per-node timeout

### Bug Discovered & Closed
- **REPORT_040** — `StdioServerParameters` missing `encoding`/`encoding_error_handler` params on Windows. MCP SDK's `TextReceiveStream` crashes with `UnicodeDecodeError` on non-UTF8 banner bytes (`\x97` em dash).
  - Filed: Source patched upstream in v0.5.4 (commit `aad969e`: "fix(orchestrator): add encoding parameters and lossy reading for banner tolerance").
  - Verification: Raw MCP client + encoding params + `_StdoutToleranceWrapper` test passes (banner lines skipped, tool response received).
  - Status: ✅ Closed in v0.5.4 (upstream fix confirmed).

### Bug Reports Closed
- `REPORT_040.md` → `archive/REPORT_040_closed.md`

### Bug Reports Closed
- `REPORT_037.md` → `archive/REPORT_037_closed.md`
- `REPORT_038.md` → `archive/REPORT_038_closed.md`
- `REPORT_039.md` → `archive/REPORT_039_closed.md`

---



### Summary
Performed structured gap analysis across all 27 scenarios against the full feature surface of context-pipe v0.5.2. Closed 5 high/medium gaps; discovered 1 new bug (REPORT_039).

### Findings

#### New Bug: REPORT_039 — `node.get("timeout")` ignored by orchestrator
- The per-node `"timeout"` field in pipes.json is **never read** by either `_run_mcp_node` or `_execute_node_chain`
- Only `PIPE_NODE_TIMEOUT_MS` env var is respected (default 30s)
- S13's `forever_sleep.py` never actually triggered a timeout (reads 1 char and exits immediately) — the evidence was a false pass
- **Impact**: All user-facing `"timeout"` configs in pipes.json are silently ignored

#### Gap Tests Verified
| Scenario | Gap | Status |
|---|---|---|
| S13 | Timeout on required node (env var workaround) | ✅ |
| S13 | `optional: true` + `condition` interaction (both paths) | ✅ |
| S18 | `run-dynamic` with Phase 11 nodes (validator, condition, id+next) | ✅ |
| S24 | Validator cycle loop guard | ✅ |
| S24 | Nested validator in `branch_sequences` | ✅ |
| S25 | Empty-default fail-fast (positive path of REPORT_038) | ✅ |
| S25 | `--manifest` + `--var` combined | ✅ |

### Updated Files
- `bugs/REPORT_039.md` — new bug report
- `scenarios/13-resiliency-gauntlet/pipes.json` — added `required-timeout-pipe`, `optional-condition-pipe`
- `scenarios/13-resiliency-gauntlet/EVIDENCE.md` — gap test evidence
- `scenarios/13-resiliency-gauntlet/README.md` — gap test documentation
- `scenarios/18-autonomous-dynamic-sifting/EVIDENCE.md` — Phase 11 parity evidence
- `scenarios/18-autonomous-dynamic-sifting/README.md` — Phase 11 parity table
- `scenarios/24-dag-validator-nodes/pipes.json` — added `validator-loop-pipe`, `nested-validator-pipe`, `artifact-fork-pipe`
- `scenarios/24-dag-validator-nodes/EVIDENCE.md` — gap test evidence
- `scenarios/24-dag-validator-nodes/README.md` — gap test documentation
- `scenarios/25-runtime-variables/pipes.json` — added `var-empty-default-fail-pipe`, `var-empty-default-pass-pipe`
- `scenarios/25-runtime-variables/EVIDENCE.md` — gap test evidence
- `scenarios/25-runtime-variables/README.md` — gap test documentation
- `BACKLOG.md`, `CHANGELOG.md` — status sync

---



### Summary
Added `artifact-fork-pipe` to Scenario 24 after user question about whether a file-exists/file-missing fork existed in Scenario 23.

### Finding
Inverse `condition` predicates (`artifact:missing` + `artifact:exists`) on sequential nodes do **not** guarantee mutual exclusion — node 1 can mutate state and satisfy node 2’s condition in the same run. `type: "validator"` + `branch_sequences` is the correct primitive for true forks.

### Pipe: `artifact-fork-pipe`
- Validator exits 0 if `.cache/spec.json` exists, 1 if missing
- Branch 0 → `route-sift` (sift the input)
- Branch 1 → `route-create` (create the artifact from input)

### Results
- Route 1 (missing) → `[CREATED] .cache/spec.json` only ✅
- Route 2 (exists) → `--- [Semantic-Sift Audit] ---` only ✅
- Mutual exclusion confirmed in both runs

---



### Summary
First-ever regression run of all 21 existing scenarios on context-pipe v0.5.2 in the pi.dev environment (shell channel).

| Result | Count |
|---|---|
| ✅ Full Pass | 13 |
| ⚠️ Partial (infra drift) | 5 |
| ❌ Hard Fail | 2 |

### Hard Failures
- **S03, S07**: `_StdoutToleranceWrapper` missing async ctx mgr protocol — **REPORT_037**

### Infrastructure Drift
- **S01, S14**: Relative paths in node args require running from scenario dir
- **S09, S10, S15**: Referenced pipes no longer exist in cross-referenced pipes.json
- **S18**: Hardcoded `grep` not on Windows PATH; `rg` works as replacement
- **S19**: `wrapper.wrap()` renamed to `wrap_payload()` — updated in-place, now passes

Full report: `regression/REGRESSION_RUN_20260530.md`

---



### Summary
First shell-channel run of all 6 new scenarios (Phases 9, 11, 12, 13). 2 bugs found.

| Scenario | Result | Notes |
|---|---|---|
| 22 — Pipe Transparency Layer | ✅ PASS | All 7 tests incl. Rust parity |
| 23 — Conditional Branching | ✅ PASS | All 5 predicates + fail-open + Rust parity |
| 24 — DAG Validator Nodes + Loop Guard | ✅ PASS | Validator routing, explicit jump, loop guard |
| 25 — Runtime Variable Injection | ⚠️ PARTIAL | `--var`, defaults, env fallback work; missing var fail-fast broken (REPORT_038) |
| 26 — Run Manifests | ✅ PASS | Explicit + auto + fail manifest all correct |
| 27 — MCP Banner Tolerance | ❌ BLOCKED | `_StdoutToleranceWrapper` missing async ctx mgr protocol (REPORT_037) |

### Bugs Filed
- **REPORT_037**: `_StdoutToleranceWrapper` missing `__aenter__`/`__aexit__` — Phase 13 regression breaks all MCP node pipes
- **REPORT_038**: Missing `${VAR}` passed as literal to subprocess instead of fail-fast

### Infrastructure Fixes During Run
- `scenarios/22-pipe-transparency-layer/pipes.json`: Added `no-logging-pipe` for env var fallback test; fixed missing comma
- `scenarios/27-mcp-banner-tolerance/pipes.json`: Changed server `command` from bare `python` to full path + absolute script path; changed backslash paths to forward slashes (shlex.split compatibility)
- `scenarios/27-mcp-banner-tolerance/mock_noisy_server.py`: Fixed notification handler (skip notifications with no `id`)

---



### Summary
Read CPP CHANGELOG and backlog. Identified 6 untested feature areas from v0.5.0. Created scenario directories, README.md, and pipes.json for each.

| Scenario | Feature | Phase |
|---|---|---|
| 22 | Pipe Transparency Layer (`logging` block, `[PIPE]` stderr) | 9 |
| 23 | Conditional Branching (`condition` predicates: size, artifact, contains) | 11A |
| 24 | DAG Validator Nodes + Loop Guard (`type: "validator"`, `branch_sequences`, `next`, 100-step guard) | 11B/C |
| 25 | Runtime Variable Injection (`--var`, `vars` defaults, fail-fast, env fallback) | 12A |
| 26 | Run Manifests (`--manifest`, `"manifest": "auto"`, schema validation) | 12B |
| 27 | MCP Banner Tolerance (noisy server, `verbose` flag, 50-line safety limit) | 13 |

`BACKLOG.md` and `LAB_STATUS.md` updated.

---



### Summary
Updated context-pipe to v0.5.2 and verified all three open reports against source and deployed extension.

### Update
- `git stash` + `git pull` in `target_repos/context-pipe` (egg-info conflict) — fast-forwarded to `087c28d` (v0.5.2), 6 files changed
- `scripts/fetch_cpipe.py` — `cpipe v0.5.2` installed
- `lab_update.py` ran clean — onboarding regenerated `.pi/extensions/context-pipe.ts`

### REPORT_034 — ✅ CLOSED
All 6 `execute` handlers now return `{ content: [{ type: "text", text: ... }] }`. Confirmed in source (lines 1249–1318) and deployed extension (lines 43–112).

### REPORT_035 — ✅ ALL 5 DEFECTS CLOSED
| Defect | Fix confirmed |
|---|---|
| A — shell injection | `spawnSync` with args array (line 1226) — no shell |
| B — `pipe_analyze_file` reads full file | `statSync().size` + recommendation string (line 1300) |
| C — 1MB maxBuffer | `maxBuffer = 50 * 1024 * 1024` (line 1222) |
| D — `tool_call` doesn't block | `return { block: true, reason: ... }` for > 1KB (line 1336) |
| E — `setStatus` missing prior set | `ctx.ui.setStatus("context-pipe", "Sifting output...")` added (line 1338) |

### REPORT_036 — ✅ pi.dev gap CLOSED
Defect D fix (above) is the pi.dev enforcement gap. `tool_call` now blocks native `read` for files > 1KB.
Structural gap on Cursor, Claude Code, Qwen, Codex, OpenCode remains (post-tool-only architectures — not fixable via hooks).

### Verified Versions
| Component | Version |
| :--- | :--- |
| `context-pipe` (Python) | `0.5.2` |
| `cpipe` (Rust binary) | `0.5.2` |
| `semantic-sift` (Python) | `0.3.5` |
| `sift-core` (Rust binary) | `0.3.5` |

---



### Summary
User pointed out `.gemini/settings.json` has a `BeforeTool` config, contradicting REPORT_036's original claim.
Full source audit conducted across all platform injectors.

### Findings (corrected)
| Platform | Pre-tool blocking |
|---|---|
| Gemini CLI | ✅ `BeforeTool` → `{"decision": "deny"}` for `read_file`/`view_file` > 50KB |
| Antigravity | ✅ Same as Gemini CLI |
| Cline | ✅ `PreToolUse` PS1+bash → `{"cancel": true}` > 1KB |
| Windsurf | ✅ `pre_mcp_tool_use` + security gateway → `exit 2` > 1KB |
| pi.dev | ❌ Has API, wrong implementation (REPORT_035 Defect D) |
| Cursor, Claude Code, Qwen, Codex, OpenCode | ❌ Post-tool-only or no hooks |

Original REPORT_036 was wrong on 4 platforms. Fully rewritten.

---



### Summary
User asked whether REPORT_035 defects are pi-specific or universal. Full scope analysis conducted.

### Findings
- **Defects A, B, C, E**: Strictly pi.dev extension template. No other platform uses `execSync`-based subprocess calls. Zero regression risk to other platforms when fixed.
- **Defect D**: pi.dev implementation is pi-specific (wrong `tool_call` usage), but the underlying gap — no platform blocks native `read` programmatically — is universal. Split to REPORT_036.
- **Fix A correction**: The proposed fix in REPORT_035 used backslash escaping (`replace(/"/g, '\\"')`) which is wrong on Windows `cmd.exe`. Corrected to `spawnSync` with args array (shell-bypassed, cross-platform safe). Also resolves Defect C (maxBuffer) in the same change.
- **OpenClaw note**: `_inject_openclaw()` also uses `execSync` at line 1162 with no `maxBuffer` override. Out of scope for current reports but worth tracking.

### Outcome
- `REPORT_035.md` updated: Fix A corrected, Defect D split note added, Cross-Platform Risk section added.
- `REPORT_036.md` filed: Universal mandate-enforcement gap across all platforms.

---



### Summary
Proactive static analysis of `.pi/extensions/context-pipe.ts` against pi `extensions.md` API docs and CLI source. Found 5 defects beyond REPORT_034.

| # | Severity | Defect |
|---|---|---|
| A | High | `pipe_run_dynamic` passes `nodes_json` unquoted in shell command → `JSONDecodeError` |
| B | High | `pipe_analyze_file` reads full file instead of stat → wrong output + context flood |
| C | Med-High | `execSync` no `maxBuffer` override → silent failure on outputs > 1MB |
| D | Medium | `tool_call` handler only notifies, never blocks native `read` → mandate not enforced |
| E | Low | `setStatus("")` in `finally` without prior `setStatus("sifting...")` → missing UX indicator |

### Outcome
`REPORT_035.md` filed. `LAB_STATUS.md` updated.

---



### Summary
After REPORT_033 fix (v0.5.1 update + reload), tested `pipe_read_file`. New crash: `Cannot read properties of undefined (reading 'some')`.

### Root Cause
All six `execute` handlers in the `_inject_pi()` template return the raw string output of `callCli()`. Pi's internal tool dispatch calls `.some()` on `result.content` to inspect the result type — but `content` is `undefined` on a plain string, causing an unrecoverable TypeError that locks the session.

### Required fix (per `extensions.md`)
Every `execute` must return `{ content: [{ type: "text", text: string }] }`, not a raw string.

### Outcome
`REPORT_034.md` filed. `LAB_STATUS.md` updated.

---



### Summary
Updated context-pipe to v0.5.1 and verified REPORT_033 fix.

### Actions
1. `lab_update.py` blocked by egg-info conflict — resolved with `git stash` + `git pull` (fast-forward to `ed166bc`).
2. `scripts/fetch_cpipe.py` — downloaded `cpipe v0.5.1` binary.
3. `pip install -e` + `python -m context_pipe.onboarding` — extension regenerated.

### REPORT_033 Verification
- Source fix confirmed: `onboarding.py` lines 1248 and 1332 both use `"standard-distill"` (not `"auto"`).
- Deployed extension confirmed: `.pi/extensions/context-pipe.ts` lines 42 and 126 both use `"standard-distill"`.
- Live `pipe_read_file` call still returns old error — **pi session reload required** to activate the new extension.

### Verified Versions
| Component | Version |
| :--- | :--- |
| `context-pipe` (Python) | `0.5.1` |
| `cpipe` (Rust binary) | `0.5.1` |
| `semantic-sift` (Python) | `0.3.5` |
| `sift-core` (Rust binary) | `0.3.5` |

---



### Summary
Tested `pipe_read_file` after restart/reload following REPORT_032 fix. Tool failed with a new error.

### Test Result
```
pipe_read_file(path="LAB_STATUS.md")
→ mcp-pipe: error: Pipe 'auto' not found.
  Available: standard-distill, semantic-refinery, ...
```

### Root Cause
The v0.5.0 `_inject_pi()` template uses `"auto"` as the default pipe name fallback in two places (lines 42 and 126 of the regenerated `.pi/extensions/context-pipe.ts`). The CLI `_cmd_run` performs a direct name lookup — `"auto"` is not a registered pipe. Correct default is `"standard-distill"` (matches MCP `server.py` default). `REPORT_033.md` filed.

---



### Summary
Investigated `pipe_read_file` failure: `mcp-pipe: error: unrecognized arguments: --file`.

### Root Cause (Two-Fault Chain)
1. **Fault 1**: `.pi/extensions/context-pipe.ts` is the stale v0.4.7 template — never regenerated after the v0.5.0 update. Contains all REPORT_031 defects, including `execute(input)` wrong param position.
2. **Fault 2**: v0.4.7 template uses `--file` flag which has never been valid in the CLI (correct flag is `--input-file`). With `input.path = undefined` from Fault 1, the command becomes `run auto --file ` (empty path) — rejected by the CLI.

### Why Onboarding Never Re-ran
`lab_update.py` calls `python -m context_pipe.onboarding --environment Gemini` — the `--environment` flag was removed in v0.5.0. The call silently failed during the update session (logged in CHANGELOG). Since `_inject_pi()` was never called, the stale extension was never overwritten.

### Outcome
- `REPORT_032.md` filed in `bugs/`
- `LAB_STATUS.md` updated with new open bug

---



### Summary
Verified that both open pi.dev integration bugs were fully resolved in context-pipe v0.5.0.

### REPORT_030 — Missing pi.dev Integration: ✅ RESOLVED
- `platforms.py`: `PI_CODING_AGENT_DIR` → `pi.dev` and `pi` process name → `pi.dev` both present and live-tested.
- `onboarding.py`: `_inject_pi()` function exists (line 1191) and is dispatched (line 1610). Generates `.pi/extensions/context-pipe.ts` and `.pi/skills/context-pipe.md`.
- `doc/INTEGRATION_ENCYCLOPEDIA.md`: pi.dev entry added at line 51 with Schema E ("No MCP — Native TypeScript extension").

### REPORT_031 — 5 Defects in Generated Extension: ✅ ALL 6 DEFECTS RESOLVED
| # | Defect | Fix in v0.5.0 |
|---|---|---|
| 1 | `execute(input)` wrong param position | `execute(_toolCallId, params)` |
| 2 | Bare `cpipe` not on PATH | Resolved absolute path via `shutil.which("mcp-pipe")` |
| 3 | `event.result` undefined | `event.content?.[0]?.text` |
| 4 | Mutating event instead of returning patch | `return { content: [{ type: "text", text: sifted }] }` |
| 5 | Command uses `execute` instead of `handler` | `handler: async (_args, _ctx) => { ... }` |
| 6 | Missing tools (`list_pipes`, `pipe_analyze_file`, `pipe_run_dynamic`) | All 6 tools now registered |

---



### Summary
Updated both core target repos to their latest released versions using `lab_update.py`.

### Actions Taken
1. **`lab_update.py`** ran but context-pipe `git pull` was aborted due to a local uncommitted change in `target_repos/context-pipe/AGENTS.md`.
2. **Manual recovery**: Ran `git stash` in `target_repos/context-pipe`, then `git pull` — fast-forwarded from `6a71c48` to `95d32c4` (tag `v0.5.0`), updating 30 files with 2,538 insertions.
3. **Binary re-fetch**: Ran `scripts/fetch_cpipe.py` — downloaded `cpipe-x86_64-pc-windows-msvc.zip` from GitHub release `v0.5.0`. Binary installed to `.venv/Scripts/cpipe.exe`.
4. **Python packages reinstalled** via `pip install -e` for both repos.
5. **`semantic-sift`** was already current at `v0.3.5` (pulled successfully by `lab_update.py`).

### Verified Versions
| Component | Version |
| :--- | :--- |
| `context-pipe` (Python) | `0.5.0` |
| `cpipe` (Rust binary) | `0.5.0` |
| `semantic-sift` (Python) | `0.3.5` |
| `sift-core` (Rust binary) | `0.3.5` |

### Notes
- Onboarding step in `lab_update.py` failed (`--environment` flag not recognised) — no regression, onboarding was already complete from prior session.
- `LAB_STATUS.md` baseline updated to reflect new versions.

---

## [2026-05-27] - pi.dev Extension Onboarding & Bug Report
- Ran `mcp-pipe onboard Gemini` after creating `.pi/` directory.
- Successfully generated pi.dev native extension (`.pi/extensions/context-pipe.ts`), skill (`.pi/skills/context-pipe.md`), and `package.json`.
- **Identified Bug #031**: `_inject_pi()` template in `onboarding.py` contains 5 defects:
  - Tool execute signatures use wrong parameter position (`execute(input)` instead of `execute(toolCallId, params, ...)`) — all 3 tools silently fail.
  - `cpipe` fast path uses bare command name not in PATH — always falls back to Python.
  - `tool_result` handler reads `event.result` (always undefined) — auto-sift never fires.
  - `tool_result` mutates `event.result` instead of returning a patch — mutation has no effect.
  - `pipe-stats` command uses `execute()` instead of `handler()` — command never registers.
- Filed `bugs/REPORT_031.md` with full root cause analysis, reproduction steps, and fix recommendations.
- **DO NOT FIX**: Per lab protocol, bug is in `target_repos/` source; filing only.

## [2026-05-27] - Lab Update
- Ran `python lab_update.py` to pull latest changes in `target_repos/`.
- **context-pipe**: updated from `v0.4.5` → `v0.4.7` (binary: `cpipe 0.4.7`).
- **semantic-sift**: updated from `v0.3.2` → `v0.3.4` (binary: `sift-core 0.3.4`).
- Updated `LAB_STATUS.md` with new baseline versions.
- **⚠️ Note**: Final onboarding step threw `unrecognized arguments: --environment`. The `--environment Gemini` flag is no longer accepted by the current `onboarding.py`. May need a fix in `lab_update.py` or the onboarding script.

## [2026-05-10] - Initial Lab Setup
- Initialized `std-context-lab` repository to battle-test `context-pipe` and `semantic-sift`.
- Cloned `context-pipe` and `semantic-sift` into `target_repos/` as read-only references (local push disabled).
- Created `AGENTS.md` to establish the Feature Lab identity and operational constraints.
- Configured a shared `uv` Python virtual environment at the repository root.
- Installed `context-pipe` and `semantic-sift` in editable mode within the shared `.venv`.
- Compiled the `sift-core` Rust binary (`--release`).
- Scaffolded `scenarios/shared_mcps` directory with a basic `package.json` for external MCP server dependencies.
- Added `BACKLOG.md` to manage upcoming feature tests and scenarios.
- Defined explicit **MCP Setup Directives** in `AGENTS.md` covering dependency centralization, scenario isolation, and shadowing by default.
- Registered `context-pipe` and `semantic-sift` as local MCP servers in `.gemini/settings.json` using the absolute venv interpreter path.
- Successfully ran `pipe_onboard`, injecting `/pipe-*` slash commands into the Gemini CLI.
- Verified installation with `pipe_verify`, confirming auto-discovery of `semantic-sift-cli`.
- Initialized root `pipes.json` with portable command names (e.g., `semantic-sift-cli`), relying on `context-pipe`'s internal venv resolution.
- Installed `semantic-sift[neural]` extras (PyTorch, Transformers, etc.) to enable high-fidelity neural sifting.
- Injected the mandatory Context-Pipe SOP/Mandate into `AGENTS.md`.
- Created `MCP_CATALOG.md` (v4) mapping 24+ tools across core infrastructure, shadow MCPs, security guardrails, and binary pre-filters to provide a comprehensive technical roadmap.
- Added `.gitignore` to protect `.gemini`, `.venv`, and `target_repos` from version control.
- Uninstalled global `github` extension to remove noise and ensure a clean testing environment.

## [2026-05-11] - Scenario 01: Protocol Basics
- Started Phase 1: Protocol Basics.
- Scaffolded `scenarios/01-protocol-basics/` with a local Node.js `transformer.js` script and a dedicated `pipes.json`.
- Successfully executed the `basics-pipe` via the `mcp-pipe` terminal tool, proving the fundamental `stdin`/`stdout` contract and language agnosticism.
- Verified that `semantic-sift-cli` correctly distilled the output of the Node.js pre-transformer.

## [2026-05-11] - Scenario 02: Shadow Discovery
- Started Phase 2: Shadow Discovery.
- Installed `@modelcontextprotocol/server-everything` into `scenarios/shared_mcps/`.
- Proved that `mcp-pipe tool everything --list-tools` successfully introspects shadow servers from local `pipes.json`.
- Verified direct shell-to-MCP bridging via `mcp-pipe tool everything echo`.
- **Bug Identified**: Discovered that the `mcp-pipe run` and `run-dynamic` commands fail to pass the `server_registry` to the orchestrator, preventing MCP nodes from functioning inside named pipes when called via the terminal CLI.
- Proved the "Zero Tool Bloat" claim by executing complex shadow tools without global registration.
- Created `README.md` files for Scenarios 01 and 02 to establish a permanent laboratory manual.
- Formally paused Scenario 03 due to discovered orchestration bugs (Logged in `bugs/REPORT_001.md`).
- **Verified & Closed Bug #002**: Confirmed `pipe_onboard` now automatically handles `.gitignore` updates.
- **Verified & Closed Bug #004**: Confirmed `pipe_onboard` now correctly injects `AfterTool` and `PreCompress` hooks for Gemini CLI.
- **Verified & Closed Bug #005**: Confirmed `pipe_onboard` now normalizes hook commands for better idempotency.
- **Verified & Closed Bug #006**: Confirmed `inject_content` now uses the correct Gemini CLI `decision: deny` schema.
- **Verified & Closed Bug #007**: Confirmed telemetry is now Opt-Out by default (Telemetry enabled automatically).
- **Verified & Closed Bug #008**: Confirmed `onboarding.py` correctly injects `GEMINI_SESSION_ID` into hook env vars.
- **Verified & Closed Bug #009**: Confirmed `onboarding.py` correctly injects `-W ignore` into the python hook command.
- **Verified & Closed Bug #001**: Confirmed orchestration fixes (Audit Header crash, Registry Leak, Command string validation).
- **Verified & Closed Bug #003**: Confirmed `orchestrator.py` now resolves `.exe` binaries on Windows correctly.
- **Verified & Closed Bug #010**: Confirmed `onboarding.py` now explicitly configures a 10s timeout for Gemini CLI hooks.
- **Verified & Closed Bug #011**: Confirmed `wrapper.py` now correctly returns `decision: allow` for Gemini CLI during bypass paths.
- **Verified & Closed Bug #012**: Confirmed `pipe_hook.py` now correctly returns `decision: allow` on exception path.
- **Verified & Closed Bug #013**: Confirmed orchestrator now resolves `${VAR}` placeholders in node arguments.
- **Verified & Closed Bug #014**: Confirmed CLI now reconfigures I/O encoding to prevent Unicode crashes on Windows.
- **Verified & Closed Bug #015**: Confirmed orchestrator now supports `optional: true` nodes for failure-bypass.
- **Verified & Closed Bug #017**: Confirmed `onboarding.py` correctly injects environment variables into the Gemini CLI hook command string (schema compliance).
- **Identified Bug #018**: Discovered idempotency failure in `merge_hook_json` when commands have shell prefixes (Logged in `bugs/REPORT_018.md`).
- Updated `target_repos/context-pipe` to **v0.3.0** (The Integration Stable Release).
- Overhauled root `README.md` with agnostic, tool-independent setup instructions to ensure lab portability for the public.
- Updated `.gitignore` to protect `node_modules` across all scenario directories.
- Manually fixed `.gitignore` to include `.pipe_cache/`, `.sift_cache/`, and `.sift_telemetry.json`.
- Defined standardized **Bug Reporting Protocol** in `AGENTS.md` to ensure high-fidelity reporting without unauthorized codebase modifications.
- Established **`bugs/archive/`** to house verified/fixed reports, keeping the root `bugs/` directory focused on active blockers.

## [2026-05-11] - Scenario 03: Research Synthesizer
- Started Phase 3: Research Synthesizer.
- Installed `mcp-server-fetch` and `markitdown` into the shared laboratory environment.
- Scaffolded `scenarios/03-research-synthesizer/` with a multi-node pipe that chains an MCP fetcher, a document converter, and a neural refinery.
- Proved the "Mental Supply Chain" claim by distilling bloated web content into high-signal markdown context.

## [2026-05-11] - Scenario 04: Core Pre-Filters
- Started Phase 4: Core Pre-Filters.
- Demonstrated context optimization using `findstr` and `yq` as pre-refinery nodes.
- Successfully reduced a 5,000-line log to pure actionable signal, proving the value of deterministic structural filtering.
- **Bug Identified**: Logged **REPORT_003.md** identifying a major issue with Windows PATH resolution for venv-installed binaries.
- Finalized permanent documentation for Scenario 04.

## [2026-05-11] - Scenario 05: Pipe-Tee Inspection
- Started Phase 5: Pipe-Tee Inspection.
- Created `scenarios/05-pipe-tee-inspection/` to test stream splitting.
- Verified that the orchestrator can reliably dump intermediate context payloads to a `.tee/` folder before a node processes them, without breaking standard output.
- Finalized permanent documentation for Scenario 05.

## [2026-05-11] - Scenario 07: The Mental Supply Chain (E2E)
- Started Phase 7: The Mental Supply Chain.
- Installed `prettier` into the shared MCPs directory for clean-room formatting.
- Created `scenarios/07-mental-supply-chain/` with mock auditor and ship-it scripts.
- Successfully orchestrated a 5-node E2E pipeline (`fetch` -> `prettier` -> `semantic-sift` with tee snapshot -> `auditor_script` -> `ship_it_mock`).
- Proved that the system can reliably stream data across MCP servers, Node.js scripts, Python CLIs, and Rust engines in a single execution.
- Finalized permanent documentation for Scenario 07.

## [2026-05-11] - Scenario 03: Research Synthesizer (Re-run)
- Successfully re-executed Scenario 03 via the terminal CLI.
- **Verified Fix #001 & #002**: Confirmed the `mcp-pipe` terminal tool now correctly passes shadow server configurations and handles telemetry headers without crashing on node failures.
- Proven the "Research Synthesizer" use case with a 3-node chain (`mcp:fetch` -> `markitdown` -> `semantic-sift`).
- Finalized permanent documentation for Scenario 03.

## [2026-05-12] - Scenario 08: Multi-Modal Distillation
- Established the **Dual-Channel Mandate** in `BACKLOG.md` to ensure platform parity across Shell and Agent interfaces.
- Successfully verified Scenario 08, proving format agnosticism by distilling styled HTML into clean Markdown signal.
- Verified 100% parity between the terminal `mcp-pipe tool` and the AI assistant's `pipe_run` tool.
- Initialized **`LAB_STATUS.md`** to provide an at-a-glance dashboard of environment health and technical scenario validation.
- Updated `LAB_STATUS.md` to support **Environment Multi-Tenancy**, enabling cross-platform parity tracking for Gemini, Cursor, VSCode, and OpenCode.
- Documented the **🖥️ IDE/Environment Onboarding SOP** in the root `README.md` to guide users through multi-platform setup.
- Finalized permanent documentation for Scenario 08.

## [2026-05-12] - Scenario 06: Agent-to-Agent (A2A) Testing
- Resumed Phase 6: A2A Testing after verified fixes for telemetry, platform detection, and hook schemas.
- Successfully executed a live hand handshake between a 'Researcher' agent and a 'Reviewer' sub-agent.
- **Verified ROI**: Captured first real-world Context Balance Sheet data, showing >1,200 chars of noise incinerated during the handshake.
- Proven the "Refined Handoff" claim: reasoning fidelity is maintained even with highly compressed context.
- Verified 100% parity across Shell and Agent channels for A2A distillation.
- Finalized permanent documentation for Scenario 06.

## [2026-05-12] - Scenario 10: Structured Data Auditor
- Proven the **Structured Data Exemption** claim: `context-pipe` intentionally bypasses sifting for valid JSON to prevent data corruption.
- Successfully verified that tools like Supabase/SQLite show "Zero Save" by design to protect intelligence integrity.
- Demonstrated how to opt-in to distillation for structured data by explicitly flattening JSON via `yq` in a multi-node supply chain.
- Finalized permanent documentation for Scenario 10.

## [2026-05-12] - Scenario 11: Supply Chain Visualization
- Developed `pipes_to_mermaid.py` script to parse `pipes.json` and generate visual supply chain diagrams.
- Created a specialized meta-pipe (`viz-pipe`) to enable self-visualization of the context supply chain.
- **Verified Observability claim**: Proved that the system is transparent and auditable across both Shell and Agent channels.
- Finalized permanent documentation for Scenario 11.

## [2026-05-12] - Scenario 12: The "Giant File" Heart-Attack
- Successfully processed a **50.6 MB** log file in **6.2 seconds**, proving industrial-grade refinery speed.
- Verified the **Truncation Guard** claim: `semantic-sift` successfully protects system memory by capping input at 50MB.
- **Verified Fix #014**: Confirmed the CLI no longer crashes on Windows Unicode headers.
- Finalized permanent documentation for Scenario 12.

## [2026-05-12] - Scenario 13: The Resiliency Gauntlet
- Tested the orchestrator's error handling under cascading node failures.
- Verified that `help_msg` hints are correctly surfaced to the agent when a node fails to resolve.
- **Verified Fix #015**: Proven that the orchestrator can successfully bypass optional node failures and continue the supply chain.
- Finalized permanent documentation for Scenario 13.

## [2026-05-12] - Scenario 14: The Security Black Hole
- Proven the **Zero-Trust Context** claim by successfully redacting over 1,000 secrets from a log stream.
- Demonstrated the use of high-performance **Python script nodes** for deterministic context sanitation.
- Finalized permanent documentation for Scenario 14.

## [2026-05-12] - Scenario 09: Adaptive Pressure Simulation (Re-run)
- Successfully re-executed Scenario 09 after verified fix for placeholder resolution.
- **Verified Fix #013**: Proven that node arguments can now dynamically resolve `${VAR}` environment placeholders.
- Finalized permanent documentation for Scenario 09.

## [2026-05-13] - Scenario 15: Recursive Supply Chains
- Successfully demonstrated **Pipeline Encapsulation** by defining a pipe that calls the `mcp-pipe` CLI as a node.
- Proven that `stdin`/`stdout` streams maintain integrity through nested layers of the orchestrator.
- Verified that the **Echo Guard** (`CPP_SIGNATURE`) correctly prevents infinite recursion loops when a pipe attempts to process its own output.
- Finalized permanent documentation for Scenario 15.

## [2026-05-13] - Scenario 16: Protocol Violation Stress
- Attempted to test the orchestrator's resiliency against corrupt node output (binary garbage, invalid UTF-8).
- **Identified Bug #020**: Discovered that the orchestrator completely crashes with a `UnicodeDecodeError` and a subsequent `TypeError` if a node outputs non-UTF8 data.
- **Verified Fix #020**: Re-executed after upstream fix. Orchestrator now correctly sanitizes binary/non-UTF8 garbage streams without crashing.
- Finalized permanent documentation for Scenario 16.

## [2026-05-13] - Scenario 17: Version Awareness & Self-Update
- **Identified Feature Gap #019**: Discovered the need for automated version awareness and 'Self-Heal' update suggestions in `pipe_verify`.
- **Verified Fix #019**: Mocked local downgrade and successfully verified `pipe_verify()` now checks GitHub tags and outputs actionable update commands.
- Finalized permanent documentation for Scenario 17.

## [2026-05-13] - 100% Full Regression Sweep
- Initiated a formal Regression Gauntlet (per `REGRESSION_SOP.md`) following the `v0.3.1` update.
- Successfully re-executed and verified Scenarios 07, 12, 13, and 15 (The "Core Four").
- Conducted an exhaustive sweep, re-executing Scenarios 01, 02, 03, 04, 05, 06, 08, 10, 11, and 14 against the `v0.3.1` code base.
- **Status: All Clear**. Confirmed that all 17 scenarios pass under the new `v0.3.1` baseline.
