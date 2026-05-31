# REPORT_042

## Title
pi.dev Extension: 1KB `read` Threshold Inconsistent with Python 50KB; Small Files Bypass Gate

## Metadata
- **Date**: 2026-05-31
- **Scenario**: 19 — BeforeTool Gating, 36 — pi.dev Enforcement Gap
- **Status**: 🔴 Re-opened — false fix in v0.5.6
- **Severity**: Low (threshold too low, not a security gap)

## Description

The pi.dev extension (`context-pipe.ts`) sets a 1KB threshold for blocking native `read` calls. Files under 1KB pass through unrestricted. The Python-side BeforeTool hook in `wrapper.py` uses 50KB. These thresholds are inconsistent.

The 1KB threshold is overly strict — it forces `pipe_read_file` for tiny files (config snippets, README excerpts, 48‑byte test files) where the pipe audit header adds more overhead than the content saves. The Python 50KB threshold was chosen because pipes are not cost-effective below that size.

## Affected Code

**File**: `.pi/extensions/context-pipe.ts`
**Line**: ~124–130

```typescript
// 2. Intercept Native 'read' Tool
pi.on("tool_call", async (event, ctx) => {
  if (isToolCallEventType("read", event)) {
    const filePath = event.input.path;
    try {
      const stats = statSync(filePath);
      if (stats.size > 1024) {                    // <-- 1KB threshold
        return {
          block: true,
          reason: `File is ${(stats.size / 1024).toFixed(1)}KB. Use pipe_read_file("${filePath}") instead.`
        };
      }
    } catch (e) {}
  }
});
```

**Reference**: Python/BEFORE_TOOL at `target_repos/context-pipe/context_pipe/wrapper.py` line ~85:

```python
if size > 51200:  # 50KB limit
    block_msg = f"[BLOCKED by Context-Pipe] File size ({size/1024:.1f}KB) exceeds 50KB safety limit for native read. Use pipe_read_file instead."
```

## Impact

- **Low**. The 1KB threshold doesn't miss actual threats — small files are cheap to read. But it generates false-positive blocks on files that would be better served by allowing the native read.
- Inconsistent behavior between pi.dev and Gemini CLI for same file sizes (1KB–50KB range).

## Recommendation

Change the threshold in `context-pipe.ts` from 1024 to 51200 to match the Python-side 50KB limit.

```typescript
if (stats.size > 51200) {
```

## False Fix — v0.5.6 Claimed but Not Applied

The v0.5.6 upstream changelog states:

> Changed the native `read` tool interception threshold in the pi.dev extension (`context-pipe.ts`) from 1KB (`1024` bytes) to 50KB (`51200` bytes) to resolve consistency issues with the Python BeforeTool hook and eliminate false-positive blocks on small files (REPORT_042).

**This is a false fix.** The `51200` value does not appear anywhere in the extension template. The fix was not applied to `context_pipe/onboarding.py` — the file that generates `.pi/extensions/context-pipe.ts`. After running `lab_update.py` on v0.5.6 and regenerating via onboarding, the extension still has:

```typescript
// context_pipe/onboarding.py line 1328 — unchanged
if (stats.size > 1024) {
```

**Evidence:**
```bash
$ grep -n "51200\|1024" target_repos/context-pipe/context_pipe/onboarding.py
1328:        if (stats.size > 1024) {   # <-- still 1KB, NOT 51200
```

```bash
$ grep -n "51200\|1024" .pi/extensions/context-pipe.ts
122:        if (stats.size > 1024) {   # <-- regenerated from unchanged template
```

The fix must be applied to `context_pipe/onboarding.py` line 1328, not claimed in the changelog alone.

## Evidence

File sizes of recently blocked or warned-on files:

| File | Size | Verdict with 1KB | Verdict with 50KB |
|---|---|---|---|
| `tiny_test.txt` | 48 B | ❌ Pass (wrong) | ✅ Pass (correct) |
| `EVIDENCE.md` (S27) | 1.9 KB | ❌ Blocked (false positive) | ✅ Allow (correct) |
| `50mb-server.log` (S12) | 50.6 MB | ✅ Blocked | ✅ Blocked |
