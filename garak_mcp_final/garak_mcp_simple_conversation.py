
import asyncio
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("garak-mcp-simple-conversation")

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://opeanai-eastus.openai.azure.com/")
MODEL = "gpt4o"

# Set Azure API key for Garak components
os.environ["AZURE_API_KEY"] = AZURE_OPENAI_API_KEY
os.environ["AZURE_ENDPOINT"] = AZURE_OPENAI_ENDPOINT

# Configure OpenAI client
openai.api_key = AZURE_OPENAI_API_KEY
openai.api_base = AZURE_OPENAI_ENDPOINT
openai.api_type = "azure"
openai.api_version = "2024-07-01-preview"

class GarakMCPSimpleConversation:
    """Simple conversational interface for Garak MCP server using direct imports"""
    
    def __init__(self):
        self.openai_client = openai.AzureOpenAI(
            api_key=AZURE_OPENAI_API_KEY,
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_version="2024-07-01-preview"
        )
        
        # Import Garak MCP server components
        try:
            # Add the garak/mcp_app directory to Python path
            mcp_app_dir = Path(__file__).parent / "garak" / "mcp_app"
            sys.path.insert(0, str(mcp_app_dir))
            
            from garak_mcp.agents import MCPAgent
            from garak_mcp.azure_model import azure_model
            from garak_mcp.eval_garak import run_garak
            
            # Initialize the research agent
            self.research_agent = MCPAgent(name="Researcher", role="You are a helpful research assistant.")
            self.azure_model = azure_model
            self.run_garak = run_garak
            
            logger.info("Successfully imported Garak MCP server components")
            
        except ImportError as e:
            logger.error(f"Failed to import Garak MCP components: {e}")
            raise
    
    def _get_available_tools(self) -> List[Dict[str, Any]]:
        """Get available tools in OpenAI function format"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "ask_research_agent",
                    "description": "Ask the research agent a question and get a response",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "question": {
                                "type": "string",
                                "description": "The question to ask the research agent"
                            }
                        },
                        "required": ["question"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "run_safety_evaluation",
                    "description": "Run Garak safety evaluation on the model",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "model_string": {
                                "type": "string",
                                "description": "Model string (e.g., 'azure:gpt4')",
                                "default": "azure:gpt4"
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
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_probes",
                    "description": "List all available Garak probes for safety testing",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "category": {
                                "type": "string",
                                "description": "Optional category filter (e.g., 'promptinject', 'dan', 'encoding')",
                                "default": ""
                            }
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_agent_history",
                    "description": "Get the current conversation history with the agent",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "reset_agent",
                    "description": "Reset the agent's conversation history",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_agent_role",
                    "description": "Update the agent's role/system prompt",
                    "parameters": {
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
            }
        ]
    
    def _call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Call a tool function directly"""
        try:
            if tool_name == "ask_research_agent":
                question = arguments.get("question", "")
                if not question:
                    return "Error: No question provided"
                
                logger.info(f"Agent received question: {question}")
                answer = self.research_agent.think(question, self.azure_model)
                logger.info(f"Agent responded: {answer[:100]}...")
                
                return f"Question: {question}\n\nAnswer: {answer}"
            
            elif tool_name == "run_safety_evaluation":
                model_string = arguments.get("model_string", "azure:gpt4")
                plugins = arguments.get("plugins", ["promptinject"])
                
                logger.info(f"Running Garak evaluation with model: {model_string}, plugins: {plugins}")
                result = self.run_garak(model_string, plugins)
                return f"Garak evaluation completed for model {model_string} with plugins {plugins}. Result: {result}"
            
            elif tool_name == "list_probes":
                category = arguments.get("category", "")
                
                try:
                    from garak_mcp.eval_garak import list_probes_by_category
                    
                    probes = list_probes_by_category(category)
                    
                    if category:
                        return f"Available Garak probes in category '{category}':\n" + "\n".join(probes)
                    else:
                        return f"All available Garak probes:\n" + "\n".join(probes)
                        
                except Exception as e:
                    logger.error(f"Error listing probes: {e}")
                    return f"Error listing probes: {str(e)}"
            
            elif tool_name == "get_agent_history":
                history_text = "\n".join([f"{role}: {content}" for role, content in self.research_agent.history])
                return f"Agent History:\n{history_text}" if history_text else "No conversation history yet."
            
            elif tool_name == "reset_agent":
                self.research_agent.history = []
                return "Agent conversation history reset successfully."
            
            elif tool_name == "update_agent_role":
                new_role = arguments.get("new_role", "")
                if not new_role:
                    return "Error: No new role provided"
                
                old_role = self.research_agent.role
                self.research_agent.role = new_role
                return f"Agent role updated from:\n'{old_role}'\nto:\n'{new_role}'"
            
            else:
                return f"Unknown tool: {tool_name}"
                
        except Exception as e:
            logger.error(f"Error calling tool {tool_name}: {e}")
            return f"Error calling tool {tool_name}: {str(e)}"
    
    def chat(self, user_message: str, conversation_history: List[Dict[str, str]] = None) -> str:
        """Main chat function that handles conversation with tool calling"""
        if conversation_history is None:
            conversation_history = []
        
        # Get available tools
        tools = self._get_available_tools()
        
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
                - list_probes: List available Garak probes
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
                    
                    # Call the tool directly
                    tool_result = self._call_tool(tool_name, tool_args)
                    
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
    
    def interactive_chat(self):
        """Start an interactive chat session"""
        print("🤖 Welcome to the Garak MCP Simple Conversational Interface!")
        print("I can help you interact with the AI research agent and run safety evaluations.")
        print("Type 'quit' or 'exit' to end the conversation.")
        print("Type 'tools' to see available tools.")
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
                    print("\n🛠️ Available Tools:")
                    tools = self._get_available_tools()
                    for tool in tools:
                        print(f"  • {tool['function']['name']}: {tool['function']['description']}")
                    continue
                
                print("\n🤖 Assistant: ", end="", flush=True)
                
                # Get response from the model
                response = self.chat(user_input, conversation_history)
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

def main():
    """Main entry point"""
    try:
        print("🚀 Starting Garak MCP Simple Conversational Interface...")
        
        # Create the conversational interface
        interface = GarakMCPSimpleConversation()
        
        # Start interactive chat
        interface.interactive_chat()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure the Garak MCP server components are available.")
    except Exception as e:
        print(f"❌ Error starting interface: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 