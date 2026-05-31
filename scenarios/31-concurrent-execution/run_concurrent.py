"""run_concurrent.py — spawns N parallel mcp-pipe invocations and waits for all.
Usage: python run_concurrent.py <n_workers> <pipe_name> <config>
"""
import sys
import subprocess
import time
from pathlib import Path

n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
pipe_name = sys.argv[2] if len(sys.argv) > 2 else "concurrent-sift"
config = sys.argv[3] if len(sys.argv) > 3 else "pipes.json"

mcp_pipe = "C:/Users/luism/Workbench/GitHub/std-context-lab/.venv/Scripts/mcp-pipe.exe"
input_text = b"Concurrent test payload: ERROR log line repeated. " * 20

procs = []
start = time.time()
for i in range(n):
    p = subprocess.Popen(
        [mcp_pipe, "run", pipe_name, "--config", config],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    p.stdin.write(input_text)
    p.stdin.close()
    procs.append((i, p))

results = []
for i, p in procs:
    stdout, stderr = p.communicate()
    results.append((i, p.returncode, len(stdout), stderr.decode("utf-8", errors="replace")))

elapsed = time.time() - start
print(f"Ran {n} concurrent pipes in {elapsed:.2f}s")
for i, rc, out_len, err in results:
    status = "OK" if rc == 0 else f"FAIL(rc={rc})"
    print(f"  Worker {i}: {status} — {out_len} bytes stdout")
    if err.strip():
        print(f"    stderr: {err.strip()[:100]}")
