import asyncio
import sys
import json
from context_pipe.orchestrator import run_pipe
from context_pipe.config_loader import load_pipes_config

async def test_pipe(pipe_name, input_data):
    print(f"\n--- TESTING PIPE: {pipe_name} ---")
    config = load_pipes_config("pipes.json")
    pipes = config.get("pipes", [])
    target_pipe = next((p for p in pipes if p.get("name") == pipe_name), None)
    
    if not target_pipe:
        print(f"Pipe {pipe_name} not found")
        return
        
    result, trace = await run_pipe(
        pipe_config=target_pipe, 
        input_data=input_data, 
        server_registry=config.get("servers", {})
    )
    
    print("RESULT PREVIEW (first 200 chars):")
    print(result[:200] + "..." if len(result) > 200 else result)
    print("\nTRACE:")
    print(json.dumps(trace, indent=2))

async def main():
    query = "SELECT * FROM user_events LIMIT 10"
    
    # 1. Test raw bypass
    await test_pipe("raw-db-pipe", query)
    
    # 2. Test explicit distillation
    await test_pipe("sifted-db-pipe", query)

if __name__ == "__main__":
    asyncio.run(main())