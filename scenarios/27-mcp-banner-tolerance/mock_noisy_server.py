#!/usr/bin/env python3
"""
Mock noisy MCP server for Scenario 27 — MCP Banner Tolerance.

Emits N banner lines to stdout before JSON-RPC begins, then responds
to a single MCP `initialize` + `tools/call` echo sequence.

Usage:
  python mock_noisy_server.py --banners 3   # emits 3 banner lines
  python mock_noisy_server.py --banners 51  # exceeds 50-line safety limit
"""
import sys
import json
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--banners", type=int, default=3)
    args = parser.parse_args()

    # Emit N non-JSON banner lines to stdout BEFORE JSON-RPC
    for i in range(args.banners):
        sys.stdout.write(f"Mock MCP Server v1.0 — banner line {i + 1}\n")
        sys.stdout.flush()

    # Minimal JSON-RPC MCP server loop
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue

        method = req.get("method", "")
        req_id = req.get("id")

        # Notifications have no id — ignore them, send no response
        if req_id is None:
            continue

        if method == "initialize":
            resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {"name": "mock-noisy-server", "version": "1.0.0"},
                    "capabilities": {"tools": {}}
                }
            }
        elif method == "tools/list":
            resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "tools": [
                        {
                            "name": "echo",
                            "description": "Echoes the input text.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {"text": {"type": "string"}},
                                "required": ["text"]
                            }
                        }
                    ]
                }
            }
        elif method == "tools/call":
            text = req.get("params", {}).get("arguments", {}).get("text", "")
            resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": f"[ECHO] {text}"}],
                    "isError": False
                }
            }
        else:
            resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"}
            }

        sys.stdout.write(json.dumps(resp) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
