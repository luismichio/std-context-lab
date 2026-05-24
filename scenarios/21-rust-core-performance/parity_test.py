import os
import subprocess
import sys

def run_parity_test(name, cmd, cwd):
    print(f"\n========================================")
    print(f"--- Parity Test: {name} ---")
    print(f"Directory: {cwd}")
    print(f"Command: {cmd}")
    print(f"----------------------------------------")
    
    cpipe_path = os.path.abspath("../../.venv/Scripts/cpipe.exe")
    
    # We no longer need to "adapt" as much if cpipe is protocol-compliant.
    # However, for PowerShell reliability, we still use absolute path and & operator.
    new_cmd = cmd
    if new_cmd.startswith("mcp-pipe"):
        new_cmd = f'& "{cpipe_path}" {new_cmd[8:]}'
    elif " mcp-pipe " in new_cmd:
        new_cmd = new_cmd.replace(" mcp-pipe ", f' & "{cpipe_path}" ')
    elif "| mcp-pipe" in new_cmd:
        new_cmd = new_cmd.replace("| mcp-pipe", f'| & "{cpipe_path}"')
    elif " mcp-pipe" in new_cmd:
         new_cmd = new_cmd.replace(" mcp-pipe", f' & "{cpipe_path}"')

    try:
        result = subprocess.run(["powershell", "-Command", new_cmd], capture_output=True, text=True, cwd=cwd)
        print(f"Exit Code: {result.returncode}")
        
        if result.stdout:
            print(f"Stdout (peek): {result.stdout[:200].strip()}...")
        if result.stderr:
            print(f"Stderr (peek): {result.stderr[:200].strip()}...")
            
        if result.returncode == 0:
            print(f"[PASS]: Parity maintained.")
            return True
        else:
            print(f"[FAIL]: Parity broken.")
            return False
            
    except Exception as e:
        print(f"[ERROR] executing test: {e}")
        return False

def main():
    if sys.platform == "win32":
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print("Starting Context-Pipe GAUNTLET v2 (Rust Core v0.4.4)")
    
    tests = [
        {"name": "01: Protocol Basics", "cwd": "../01-protocol-basics", "cmd": "Get-Content sample.log | mcp-pipe run basics-pipe"},
        {"name": "02: Shadow Discovery", "cwd": "../02-shadow-discovery", "cmd": "mcp-pipe list --config pipes.json"},
        {"name": "04: Core Pre-Filters", "cwd": "../04-core-prefilters", "cmd": "mcp-pipe run noisy-filter --config pipes.json --input_file noisy_app.log"},
        {"name": "06: A2A Handoff", "cwd": "../06-a2a-handoff", "cmd": "mcp-pipe handoff --from Researcher --to Reviewer --output 'findings'"},
        {"name": "17: Version Awareness", "cwd": "../17-version-awareness", "cmd": "mcp-pipe verify"},
        {"name": "18: Dynamic Sifting", "cwd": "../18-autonomous-dynamic-sifting", "cmd": "mcp-pipe run-dynamic '[{\"cmd\": \"grep\", \"args\": [\"needle\"]}, {\"cmd\": \"semantic-sift-cli\", \"args\": [\"semantic\"]}]' --input_file needle_in_haystack.log --allow_shell"},
        {"name": "20: Line Ranges", "cwd": "../20-orchestrated-line-ranges", "cmd": "mcp-pipe run standard-distill --input_file numbered_lines.txt --start_line 500 --end_line 510"}
    ]
    
    results = []
    for test in tests:
        res = run_parity_test(test["name"], test["cmd"], test["cwd"])
        results.append(res)
        
    print(f"\n========================================")
    print(f"GAUNTLET v2 COMPLETE.")
    print(f"Total Scenarios Tested: {len(results)}")
    print(f"Passed: {results.count(True)}")
    print(f"Failed: {results.count(False)}")
    print(f"Success Rate: {(results.count(True)/len(results)*100):.1f}%")
    print(f"========================================")

if __name__ == "__main__":
    main()
