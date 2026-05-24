import json
import sys
import os

# Add context-pipe to path
sys.path.insert(0, os.path.abspath("../../target_repos/context-pipe"))
from context_pipe.wrapper import wrap_payload

def test_hook(name, tool_name, path, expected_decision):
    print(f"\n--- Test: {name} ---")
    # Real Gemini CLI payload format (uses 'tool', 'args')
    payload = {
        "tool": tool_name,
        "args": {"path": path} if path else {}
    }
    
    # Mock config
    config = {"rules": [{"trigger": "size:>1024", "pipe": "standard-distill"}]}
    
    # Mock environment for platform detection
    os.environ["GEMINI_SESSION_ID"] = "true"
    
    result_json = wrap_payload(json.dumps(payload), config)
    result = json.loads(result_json)
    print(f"Path: {path}")
    print(f"Expected: {expected_decision}, Actual: {result.get('decision')}")
    if result.get('decision') == 'deny':
        print(f"Reason: {result.get('reason')}")
    return result_json

# 1. Massive File
test_hook("Massive File", "read_file", "massive_50mb.log", "deny")

# 2. Boundary Condition (Exactly at threshold - 1KB)
test_hook("Threshold Limit", "read_file", "threshold_limit.log", "allow")

# 3. Exemption (Small config)
test_hook("Small Config", "read_file", "small_config.json", "allow")

# 4. Invalid Payload (Unknown tool)
test_hook("Invalid Tool", "unknown_tool", "massive_50mb.log", "allow")
