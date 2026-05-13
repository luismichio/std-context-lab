import json
import sys
import os

def generate_mermaid(config_path):
    if not os.path.exists(config_path):
        return f"Error: {config_path} not found"

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception as e:
        return f"Error parsing JSON: {str(e)}"

    pipes = config.get("pipes", [])
    if not pipes:
        return "No pipes found in config."

    lines = ["graph LR"]
    
    for pipe in pipes:
        pipe_name = pipe.get("name", "unknown")
        nodes = pipe.get("nodes", [])
        
        # Start node
        prev_node_id = f"start_{pipe_name}"
        lines.append(f"  {prev_node_id}([Input])")
        
        for i, node in enumerate(nodes):
            cmd = node.get("cmd", "")
            node_type = node.get("type", "binary")
            
            if node_type == "mcp":
                label = f"mcp:{node.get('server')}/{node.get('tool')}"
            else:
                label = os.path.basename(cmd) if cmd else "unknown"
            
            node_id = f"node_{pipe_name}_{i}"
            lines.append(f"  {node_id}[{label}]")
            lines.append(f"  {prev_node_id} --> {node_id}")
            prev_node_id = node_id
        
        # End node
        end_node_id = f"end_{pipe_name}"
        lines.append(f"  {end_node_id}([LLM Context])")
        lines.append(f"  {prev_node_id} --> {end_node_id}")

    return "\n".join(lines)

if __name__ == "__main__":
    # If run as a node, we might want to read from stdin, 
    # but for visualization, we read the config file.
    path = sys.argv[1] if len(sys.argv) > 1 else "pipes.json"
    print(generate_mermaid(path))
