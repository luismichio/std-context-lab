import os
import subprocess
import time
import json
import concurrent.futures

def run_python_pipe(input_text):
    cmd = [
        "../../.venv/Scripts/python.exe", "-m", "context_pipe.orchestrator",
        "run", "stress-test", "--config", "pipes.json"
    ]
    start = time.time()
    result = subprocess.run(cmd, input=input_text, text=True, capture_output=True, env=os.environ)
    duration = time.time() - start
    if result.returncode != 0:
        print(f"Python Error: {result.stderr}")
    return duration

def run_rust_pipe(input_text):
    cmd = [
        "../../.venv/Scripts/cpipe.exe", "run", "stress-test", "--config", "pipes.json"
    ]
    start = time.time()
    result = subprocess.run(cmd, input=input_text, text=True, capture_output=True, env=os.environ)
    duration = time.time() - start
    if result.returncode != 0:
        print(f"Rust Error: {result.stderr}")
    return duration

def main():
    # 1. Startup Tax Benchmark (Sequential)
    print("\n--- Test 1: Startup Tax Benchmark (10 iterations) ---")
    input_text = "Sample input text for benchmarking context-pipe performance."
    
    py_times = [run_python_pipe(input_text) for _ in range(10)]
    rs_times = [run_rust_pipe(input_text) for _ in range(10)]
    
    py_avg = sum(py_times) / 10
    rs_avg = sum(rs_times) / 10
    
    print(f"Python Avg: {py_avg:.4f}s")
    print(f"Rust Avg:   {rs_avg:.4f}s")
    if rs_avg > 0:
        print(f"Improvement: {(py_avg/rs_avg):.1f}x faster")

    # 2. High Concurrency Test
    print("\n--- Test 2: High Concurrency (20 parallel instances) ---")
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        start = time.time()
        futures = [executor.submit(run_rust_pipe, input_text) for _ in range(20)]
        concurrent.futures.wait(futures)
        total_time = time.time() - start
    print(f"Processed 20 parallel pipes in {total_time:.4f}s")

    # 3. Protocol Violation (Non-UTF8)
    print("\n--- Test 3: Protocol Violation (Binary Data) ---")
    cmd = [
        "../../.venv/Scripts/cpipe.exe", "run", "stress-test", "--config", "pipes.json"
    ]
    binary_input = b"Illegal bytes: \xff\xfe\xfd\n"
    # cpipe should handle this or fail gracefully
    result = subprocess.run(cmd, input=binary_input, capture_output=True, env=os.environ)
    print(f"Exit Code: {result.returncode}")
    print(f"Stderr Peek: {result.stderr.decode('utf-8', 'ignore')[:100]}")

if __name__ == "__main__":
    # Ensure target_repos is in PYTHONPATH for Python orchestrator
    os.environ["PYTHONPATH"] = os.path.abspath("../../target_repos/context-pipe")
    main()
