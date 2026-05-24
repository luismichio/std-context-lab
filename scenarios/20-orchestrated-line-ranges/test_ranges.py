import os
import sys
import json
import asyncio

# Add context-pipe to path
sys.path.insert(0, os.path.abspath("../../target_repos/context-pipe"))
from context_pipe.server import pipe_read_file

# Authorize current directory for testing
os.environ["PIPE_AUTHORIZED_ROOT"] = os.getcwd()
# Explicitly point to the local pipes.json
os.environ["PIPE_CONFIG_PATH"] = os.path.abspath("pipes.json")

async def test_range(name, start, end):
    print(f"\n--- Test: {name} ({start} to {end}) ---")
    try:
        result = await pipe_read_file(path="numbered_lines.txt", start_line=start, end_line=end)
        
        # Strip audit header if present
        content_lines = result.split("\n")
        lines = [l for l in content_lines if "Line " in l]
        
        print(f"Result count: {len(lines)} lines")
        if lines:
            print(f"First line: {lines[0]}")
            print(f"Last line: {lines[-1]}")
        else:
            print("Full result (first 2 lines):")
            print("\n".join(content_lines[:2]))
    except Exception as e:
        print(f"Caught error: {e}")

async def main():
    # 1. Happy Path (11 lines)
    await test_range("Happy Path", 500, 510)

    # 2. Out of Bounds (High)
    await test_range("Out of Bounds High", 2000, 2050)

    # 3. Inverted Bounds
    await test_range("Inverted Bounds", 50, 10)

    # 4. Partial EOF
    await test_range("Partial EOF", 995, 1010)

if __name__ == "__main__":
    asyncio.run(main())
