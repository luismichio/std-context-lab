/**
 * Context-Pipe Native pi.dev Extension
 * "No MCP" - Tools are registered natively.
 */
import { ExtensionAPI, isToolCallEventType } from "@earendil-works/pi-coding-agent";
import { Type } from "@sinclair/typebox";
import { spawnSync } from "child_process";
import { readFileSync, statSync } from "fs";
import { basename } from "path";

export default function (pi: ExtensionAPI) {
  const pythonExe = "C:/Users/luism/Workbench/GitHub/std-context-lab/.venv/Scripts/python.exe";
  const mcpPipePath = "C:/Users/luism/AppData/Local/Programs/Python/Python313/Scripts/mcp-pipe.EXE";

  const callCli = (args: string[], input?: string) => {
    const maxBuffer = 50 * 1024 * 1024;
    
    // Try mcp-pipe binary first (fast path)
    if (mcpPipePath) {
      const result = spawnSync(mcpPipePath, args, { input, encoding: "utf-8", maxBuffer });
      if (result.status === 0) return result.stdout;
    }
    
    // Fallback to python module
    const pythonArgs = ["-m", "context_pipe.cli", ...args];
    const result2 = spawnSync(pythonExe, pythonArgs, { input, encoding: "utf-8", maxBuffer });
    if (result2.status === 0) return result2.stdout;
    
    const errorMsg = result2.stderr || "CLI call failed";
    console.error("[Context-Pipe] CLI call failed:", errorMsg);
    throw new Error(errorMsg);
  };

  // 1. Register Native Tools
  pi.registerTool({
    name: "pipe_read_file",
    label: "Pipe Read File",
    description: "Read a file through the optimal context pipe (Standard Practice).",
    parameters: Type.Object({
      path: Type.String({ description: "Absolute or relative path to the file." }),
      pipe_name: Type.Optional(Type.String({ description: "Explicit pipe name." })),
    }),
    async execute(_toolCallId, params) {
      const text = readFileSync(params.path, "utf-8");
      const sifted = callCli(["run", params.pipe_name || "standard-distill"], text);
      return { content: [{ type: "text", text: sifted }] };
    }
  });

  pi.registerTool({
    name: "pipe_run",
    label: "Pipe Run",
    description: "Process text through a named context pipe.",
    parameters: Type.Object({
      pipe_name: Type.String({ description: "Name of the pipe to run." }),
      input_text: Type.String({ description: "Raw text to process." }),
    }),
    async execute(_toolCallId, params) {
      const sifted = callCli(["run", params.pipe_name], params.input_text);
      return { content: [{ type: "text", text: sifted }] };
    }
  });

  pi.registerTool({
    name: "get_pipe_stats",
    label: "Get Pipe Stats",
    description: "View the Context-Pipe Balance Sheet (ROI).",
    parameters: Type.Object({}),
    async execute(_toolCallId, _params) {
      const stats = callCli(["stats"]);
      return { content: [{ type: "text", text: stats }] };
    }
  });

  pi.registerTool({
    name: "list_pipes",
    label: "List Pipes",
    description: "Lists all available context pipes and their descriptions.",
    parameters: Type.Object({}),
    async execute(_toolCallId, _params) {
      const list = callCli(["list"]);
      return { content: [{ type: "text", text: list }] };
    }
  });

  pi.registerTool({
    name: "pipe_analyze_file",
    label: "Pipe Analyze File",
    description: "Analyze a file through the context pipe with semantic analysis.",
    parameters: Type.Object({
      path: Type.String({ description: "Absolute or relative path to the file." }),
      pipe_name: Type.Optional(Type.String({ description: "Explicit pipe name (default: semantic-refinery)." })),
    }),
    async execute(_toolCallId, params) {
      const size = statSync(params.path).size;
      const recommendation = size > 10000 ? "semantic-refinery" : "standard-distill";
      const resultText = `File: ${basename(params.path)}\nSize: ${size} bytes\nRecommendation: Use pipe_read_file with pipe_name='${recommendation}'.`;
      return { content: [{ type: "text", text: resultText }] };
    }
  });

  pi.registerTool({
    name: "pipe_run_dynamic",
    label: "Pipe Run Dynamic",
    description: "Run an ad-hoc processing graph composed from shadow tools.",
    parameters: Type.Object({
      nodes_json: Type.String({ description: "JSON array of node definitions." }),
      input_text: Type.String({ description: "Raw input text to process." }),
    }),
    async execute(_toolCallId, params) {
      const sifted = callCli(["run-dynamic", params.nodes_json], params.input_text);
      return { content: [{ type: "text", text: sifted }] };
    }
  });

  // 2. Intercept Native 'read' Tool
  pi.on("tool_call", async (event, ctx) => {
    if (isToolCallEventType("read", event)) {
      const filePath = event.input.path;
      try {
        const stats = statSync(filePath);
        if (stats.size > 51200) {
          return {
            block: true,
            reason: `File is ${(stats.size / 1024).toFixed(1)}KB. Use pipe_read_file("${filePath}") instead.`
          };
        }
      } catch (e) {}
    }
  });

  // 3. Auto-Pipe Large Tool Results
  pi.on("tool_result", async (event, ctx) => {
    const text = event.content?.[0]?.text;
    if (typeof text === "string" && text.length > 5000) {
      if (text.includes("--- [Context-Pipe Audit] ---")) return;
      try {
        ctx.ui.setStatus("context-pipe", "Sifting output...");
        const sifted = callCli(["run", "standard-distill"], text);
        return { content: [{ type: "text", text: sifted }] };
      } catch (e) {
        console.error("[Context-Pipe] Auto-sift failed");
      } finally {
        ctx.ui.setStatus("context-pipe", "");
      }
    }
  });

  // 4. Register Commands
  pi.registerCommand("pipe-stats", {
    description: "View Context-Pipe Balance Sheet",
    handler: async (_args, _ctx) => {
      const stats = callCli(["stats"]);
      console.log(stats);
    }
  });
}
