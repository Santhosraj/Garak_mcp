import asyncio
import json
import logging
import os
from typing import Any, Dict, List, Optional
import openai
from pathlib import Path
import sys

current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("garak-mcp-simple-conversation")

# Azure OpenAI Configuration
API_KEY = "a00d081fe4b849beb5b5c0c4ed8d837f"
AZURE_ENDPOINT = "https://opeanai-eastus.openai.azure.com/"
MODEL = "gpt4o"  
AZURE_MODEL_NAME = "gpt-4o"


# Set environment variables for Garak
os.environ["AZURE_API_KEY"] = API_KEY
os.environ["AZURE_ENDPOINT"] = AZURE_ENDPOINT
os.environ["AZURE_MODEL_NAME"] = AZURE_MODEL_NAME
os.environ["AZURE_API_VERSION"] = "2024-06-01"

class GarakMCPSimpleConversationalInterface:
    """Simple conversational interface using direct Garak MCP server integration"""
    
    def __init__(self):
        self.tools = []
        self.openai_client = openai.AzureOpenAI(
            azure_endpoint=AZURE_ENDPOINT,
            api_key=API_KEY,
            api_version="2024-06-01"
        )
        
    async def __aenter__(self):
        """Async context manager entry"""
        # Get available tools from the MCP server
        self.tools = await self._get_tools()
        logger.info(f"Connected to Garak MCP server with {len(self.tools)} tools available")
        
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        pass
    
    async def _get_tools(self) -> List[Dict[str, Any]]:
        """Get tools from the Garak MCP server"""
        # Define the tools based on the Garak MCP server implementation
        tool_definitions = [
     
            {
                "name": "run_safety_evaluation",
                "description": "Run Garak safety evaluation on the model",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "model_string": {
                            "type": "string",
                            "description": "Model string (e.g., 'azure:gpt4')",
                            "default": "azure:gpt4o"
                        },
                        "plugins": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of Garak plugins to run",
                            "default": ["promptinject"]
                        }
                    },
                    "required": []
                }
            },
            {
                "name": "get_agent_history",
                "description": "Get the current conversation history with the agent",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "reset_agent",
                "description": "Reset the agent's conversation history",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "update_agent_role",
                "description": "Update the agent's role/system prompt",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "new_role": {
                            "type": "string",
                            "description": "The new role/system prompt for the agent"
                        }
                    },
                    "required": ["new_role"]
                }
            }
        ]
        
        tools = []
        for tool_def in tool_definitions:
            openai_tool = {
                "type": "function",
                "function": tool_def
            }
            tools.append(openai_tool)
        
        return tools
    
    async def _call_mcp_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Call a tool on the Garak MCP server"""
        try:
            # Import the necessary modules from the Garak MCP server
            sys.path.insert(0, str(Path(__file__).parent / "garak" / "mcp_app"))
            
            from agents.agents import MCPAgent
            from models.azure_model import azure_model
            from evaluate.eval_garak import run_garak
            
            # Create a global agent instance (similar to the MCP server)
            if not hasattr(self, '_agent'):
                self._agent = MCPAgent(name="Researcher", role="You are a helpful research assistant.")
            
            # Map tool names to functions
            if tool_name == "ask_research_agent":
                question = arguments.get("question", "")
                if not question:
                    return "Error: No question provided"
                
                answer = self._agent.think(question, azure_model)
                return f"Question: {question}\n\nAnswer: {answer}"
            
            elif tool_name == "run_safety_evaluation":
                model_string = arguments.get("model_string", "azure:gpt4o")
                plugins = arguments.get("plugins", ["promptinject"])
                
                # Parse user request to determine appropriate probes
                user_request = arguments.get("user_request", "")
                if user_request:
                    # Extract probe types from user request
                    request_lower = user_request.lower()
                    detected_probes = []
                    
                    # Map common request patterns to probes
                    if any(word in request_lower for word in ["jailbreak", "dan", "do anything", "stan", "dude"]):
                        detected_probes.append("dan")
                    if any(word in request_lower for word in ["prompt", "injection", "hijack"]):
                        detected_probes.append("promptinject")
                    if any(word in request_lower for word in ["encoding", "base64", "hex", "morse"]):
                        detected_probes.append("encoding")
                    if any(word in request_lower for word in ["social", "grandma", "manipulation"]):
                        detected_probes.append("grandma")
                    if any(word in request_lower for word in ["toxic", "toxicity", "rtp"]):
                        detected_probes.append("realtoxicityprompts")
                    if any(word in request_lower for word in ["leak", "extraction", "training data"]):
                        detected_probes.append("leakreplay")
                    if any(word in request_lower for word in ["code", "sql", "exploitation"]):
                        detected_probes.append("exploitation")
                    if any(word in request_lower for word in ["malware", "virus", "payload"]):
                        detected_probes.append("malwaregen")
                    if any(word in request_lower for word in ["comprehensive", "full", "all"]):
                        detected_probes = ["dan", "promptinject", "encoding", "grandma", "realtoxicityprompts"]
                    
                    # Use detected probes if found, otherwise use provided plugins
                    if detected_probes:
                        plugins = detected_probes
                
                # Run the evaluation (environment variables are set in run_garak function)
                result = run_garak(model_string=model_string, plugins=plugins)
                return f"Garak evaluation completed for model {model_string} with plugins {plugins}\n\nResult: {result}"
            
            elif tool_name == "get_agent_history":
                history_text = "\n".join([f"{role}: {content}" for role, content in self._agent.history])
                return f"Agent History:\n{history_text}" if history_text else "No conversation history yet."
            
            elif tool_name == "reset_agent":
                self._agent.history = []
                return "Agent conversation history reset successfully."
            
            elif tool_name == "update_agent_role":
                new_role = arguments.get("new_role", "")
                if not new_role:
                    return "Error: No new role provided"
                
                old_role = self._agent.role
                self._agent.role = new_role
                return f"Agent role updated from:\n'{old_role}'\nto:\n'{new_role}'"
            
            else:
                return f"Unknown tool: {tool_name}"
                
        except Exception as e:
            logger.error(f"Error calling tool {tool_name}: {e}")
            return f"Error calling tool {tool_name}: {str(e)}"
    
    async def chat(self, user_message: str, conversation_history: List[Dict[str, str]] = None) -> str:
        """Main chat function that handles conversation with tool calling"""
        if conversation_history is None:
            conversation_history = []
        
        # Format tools for OpenAI
        tools = self.tools
        
        # Prepare messages
        messages = [
            {
                "role": "system",
                "content": """You are a helpful assistant that can interact with a Garak MCP server for AI research and safety evaluation. 
                You can:
                
                - Ask the research agent questions about AI safety and research
                - Run Garak safety evaluations on AI models
                - Manage the agent's conversation history
                - Update the agent's role and configuration
                
                Available tools:
                - ask_research_agent: Ask the research agent a question
                - run_safety_evaluation: Run Garak safety evaluation
                - get_agent_history: Get conversation history
                - reset_agent: Reset conversation history
                - update_agent_role: Update agent's role
                
                When a user asks a question:
                1. Use ask_research_agent to get a response from the research agent
                2. If they want to run safety evaluations, use run_safety_evaluation
                3. If they want to see history, use get_agent_history
                4. If they want to reset or update the agent, use the appropriate tools
                
                Always be conversational and helpful. If you need to call a tool, do so and then explain the results to the user.
                Focus on AI safety, research, and evaluation topics."""
            }
        ]
        
        # Add conversation history
        messages.extend(conversation_history)
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        try:
            # First, try to get a response without tool calling
            response = self.openai_client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=tools,
                tool_choice="auto",
                temperature=0.7,
                max_tokens=1000
            )
            
            assistant_message = response.choices[0].message
            messages.append(assistant_message)
            
            # Check if tool calling is needed
            if assistant_message.tool_calls:
                # Handle tool calls
                for tool_call in assistant_message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)
                    
                    # Call the MCP tool
                    tool_result = await self._call_mcp_tool(tool_name, tool_args)
                    
                    # Add tool result to messages
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_result
                    })
                
                # Get final response from OpenAI
                final_response = self.openai_client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1000
                )
                
                return final_response.choices[0].message.content
            else:
                return assistant_message.content
                
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return f"Sorry, I encountered an error: {str(e)}"
    
    async def interactive_chat(self):
        """Start an interactive chat session"""
        print("🤖 Welcome to the Garak MCP Simple Conversational Interface!")
        print("I can help you interact with the AI research agent and run safety evaluations.")
        print("Type 'quit' or 'exit' to end the conversation.")
        print("Type 'tools' to see available MCP tools.")
        print("-" * 50)
        
        conversation_history = []
        
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n🤖 Goodbye! Stay safe with AI!")
                    break
                
                if not user_input:
                    continue
                
                if user_input.lower() == 'tools':
                    print("\n🛠️ Available MCP Tools:")
                    for tool in self.tools:
                        print(f"  • {tool['function']['name']}: {tool['function']['description']}")
                    continue
                
                print("\n🤖 Assistant: ", end="", flush=True)
                
                # Get response from the model
                response = await self.chat(user_input, conversation_history)
                print(response)
                
                # Update conversation history
                conversation_history.append({"role": "user", "content": user_input})
                conversation_history.append({"role": "assistant", "content": response})
                
                # Keep conversation history manageable (last 10 exchanges)
                if len(conversation_history) > 20:
                    conversation_history = conversation_history[-20:]
                    
            except KeyboardInterrupt:
                print("\n\n🤖 Goodbye! Stay safe with AI!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")

async def main():
    """Main entry point"""
    print("🚀 Starting Garak MCP Simple Conversational Interface...")
    
    async with GarakMCPSimpleConversationalInterface() as interface:
        await interface.interactive_chat()

if __name__ == "__main__":
    asyncio.run(main()) 