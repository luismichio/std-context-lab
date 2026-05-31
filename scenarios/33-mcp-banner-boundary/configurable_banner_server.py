"""configurable_banner_server.py — minimal MCP server that emits N banner lines.
Usage: python configurable_banner_server.py <n_banners>
"""
import sys
import json

n_banners = int(sys.argv[1]) if len(sys.argv) > 1 else 3

# Emit banner lines before JSON-RPC
for i in range(n_banners):
    sys.stdout.write(f"Banner line {i+1} of {n_banners}\r\n")
    sys.stdout.flush()

# Minimal MCP server loop
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        msg = json.loads(line)
    except json.JSONDecodeError:
        continue

    msg_id = msg.get("id")
    method = msg.get("method", "")

    if method == "initialize":
        resp = {
            "jsonrpc": "2.0", "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "banner-test-server", "version": "1.0"}
            }
        }
    elif method == "tools/list":
        resp = {
            "jsonrpc": "2.0", "id": msg_id,
            "result": {"tools": [{"name": "echo", "description": "Echo input",
                "inputSchema": {"type": "object", "properties":
                    {"text": {"type": "string"}}, "required": ["text"]}}]}
        }
    elif method == "tools/call":
        text = msg.get("params", {}).get("arguments", {}).get("text", "")
        resp = {
            "jsonrpc": "2.0", "id": msg_id,
            "result": {"content": [{"type": "text", "text": f"[ECHO] {text}"}]}
        }
    elif method == "notifications/initialized":
        continue
    else:
        resp = {"jsonrpc": "2.0", "id": msg_id, "result": {}}

    sys.stdout.write(json.dumps(resp) + "\n")
    sys.stdout.flush()
