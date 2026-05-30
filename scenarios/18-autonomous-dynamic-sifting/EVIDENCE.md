# Evidence: Scenario 18 (Autonomous Dynamic Sifting)

**Verified On:** 2026-05-24
**Baseline:** `context-pipe v0.4.3` | `semantic-sift v0.3.2`

## Verification Command
```powershell
mcp-pipe run-dynamic '[{"cmd": "grep", "args": ["needle"]}, {"cmd": "semantic-sift-cli", "args": ["semantic"]}]' --input_file needle_in_haystack.log --allow_shell
```

## Captured Evidence (Raw)
*   **Log File**: [run_autonomous_dynamic_sifting.log](run_autonomous_dynamic_sifting.log)
*   **Claim Proven**: Proved the "Dynamic Sifting" capability, allowing agents to assemble JIT processing graphs on-the-fly.

## Gap Tests Added 2026-05-30 (Phase 11 features via run-dynamic)

### Test — Dynamic validator (type:"validator" + branches)
```bash
echo "input" | mcp-pipe run-dynamic '[{"id":"val","type":"validator","cmd":"<python>","args":["-c","import sys; sys.exit(0)"],"branches":{"0":"sift"}},{"id":"sift","cmd":"<semantic-sift-cli>","args":["semantic","--rate","0.5"]}]'
```
**stdout:** `--- [Semantic-Sift Audit] ---`
✅ Validator exits 0 → routed to sift branch.

### Test — Dynamic condition (`condition: "size:>5000"`)
```bash
echo "SHORT" | mcp-pipe run-dynamic '[{"cmd":"<semantic-sift-cli>","args":["logs"],"condition":"size:>5000"},{"cmd":"<semantic-sift-cli>","args":["logs"]}]'
```
**stdout:** One sift audit header (first node skipped, second ran)
✅ Condition gate works in dynamic context.

### Test — Dynamic id+next jump
```bash
echo "input" | mcp-pipe run-dynamic '[{"id":"A","cmd":"<python>","args":["-c","import sys; sys.stdout.write('[A]'+sys.stdin.read())"],"next":"C"},{"id":"B","cmd":"<python>","args":["-c","import sys; sys.stdout.write('[B]'+sys.stdin.read())"]},{"id":"C","cmd":"<python>","args":["-c","import sys; sys.stdout.write('[C]'+sys.stdin.read())"]}]'
```
**stdout:** `[C][A]input`
✅ Node B skipped. `next` jump works in dynamic context.
