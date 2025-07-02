

import asyncio
import logging
from typing import Any, Sequence
from contextlib import AsyncExitStack

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)

from agents import MCPAgent
from azure_model import azure_model
from eval_garak import run_garak

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai-research-mcp")

# Global agent instance
research_agent = MCPAgent(name="Researcher", role="You are a helpful research assistant.")

# Create MCP server
server = Server("ai-research-agent")

@server.list_resources()
async def handle_list_resources() -> list[Resource]:
    """List available resources"""
    return [
        Resource(
            uri="agent://history",
            name="Agent Conversation History",
            description="Current conversation history with the research agent",
            mimeType="application/json",
        ),
        Resource(
            uri="agent://config",
            name="Agent Configuration",
            description="Current agent configuration and settings",
            mimeType="application/json",
        ),
    ]

@server.read_resource()
async def handle_read_resource(uri: str) -> str:
    """Read a specific resource"""
    if uri == "agent://history":
        return str(research_agent.history)
    elif uri == "agent://config":
        return f"Agent Name: {research_agent.name}\nRole: {research_agent.role}"
    else:
        raise ValueError(f"Unknown resource: {uri}")

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="ask_research_agent",
            description="Ask the research agent a question and get a response",
            inputSchema={
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "The question to ask the research agent"
                    }
                },
                "required": ["question"]
            },
        ),
        Tool(
            name="run_safety_evaluation",
            description="Run Garak safety evaluation on the model",
            inputSchema={
                "type": "object",
                "properties": {
                    "model_string": {
                        "type": "string",
                        "description": "Model string (e.g., 'azure:gpt4o')",
                        "default": "azure:gpt-4o"
                    },
                    "plugins": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of Garak plugins to run",
                        "default": ["promptinject"]
                    }
                },
                "required": []
            },
        ),
        Tool(
            name="get_agent_history",
            description="Get the current conversation history with the agent",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="reset_agent",
            description="Reset the agent's conversation history",
            inputSchema={
                "type": "object",  
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="update_agent_role",
            description="Update the agent's role/system prompt",
            inputSchema={
                "type": "object",
                "properties": {
                    "new_role": {
                        "type": "string",
                        "description": "The new role/system prompt for the agent"
                    }
                },
                "required": ["new_role"]
            },
        ),
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent | ImageContent | EmbeddedResource]:
    """Handle tool calls"""
    if arguments is None:
        arguments = {}
    
    if name == "ask_research_agent":
        question = arguments.get("question", "")
        if not question:
            return [TextContent(type="text", text="Error: No question provided")]
        
        try:
            logger.info(f"Agent received question: {question}")
            answer = research_agent.think(question, azure_model)
            logger.info(f"Agent responded: {answer[:100]}...")
            
            return [TextContent(
                type="text",
                text=f"Question: {question}\n\nAnswer: {answer}"
            )]
        except Exception as e:
            logger.error(f"Error in ask_research_agent: {e}")
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    elif name == "run_safety_evaluation":
        model_string = arguments.get("model_string", "azure:gpt4")
        plugins = arguments.get("plugins", ["promptinject"])
        
        try:
            logger.info(f"Running Garak evaluation with model: {model_string}, plugins: {plugins}")
            result = await asyncio.get_event_loop().run_in_executor(
                None, run_garak, model_string, plugins
            )
            return [TextContent(
                type="text",
                text=f"Garak evaluation completed for model {model_string} with plugins {plugins}"
            )]
        except Exception as e:
            logger.error(f"Error in run_safety_evaluation: {e}")
            return [TextContent(type="text", text=f"Error running Garak evaluation: {str(e)}")]
    
    elif name == "get_agent_history":
        history_text = "\n".join([f"{role}: {content}" for role, content in research_agent.history])
        return [TextContent(
            type="text",
            text=f"Agent History:\n{history_text}" if history_text else "No conversation history yet."
        )]
    
    elif name == "reset_agent":
        research_agent.history = []
        return [TextContent(type="text", text="Agent conversation history reset successfully.")]
    
    elif name == "update_agent_role":
        new_role = arguments.get("new_role", "")
        if not new_role:
            return [TextContent(type="text", text="Error: No new role provided")]
        
        old_role = research_agent.role
        research_agent.role = new_role
        return [TextContent(
            type="text",
            text=f"Agent role updated from:\n'{old_role}'\nto:\n'{new_role}'"
        )]
    
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    """Main function to run the MCP server"""
    # Create initialization options
    init_options = InitializationOptions(
        server_name="ai-research-agent",
        server_version="1.0.0",
        capabilities={
            "resources": {},
            "tools": {},
            "logging": {},
        }
    )
    
    logger.info("AI Research Agent MCP Server starting...")
    
    # Initialize the server with stdio transport
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream=read_stream,
            write_stream=write_stream,
            initialization_options=init_options
        )

if __name__ == "__main__":
    asyncio.run(main())