# Garak Model Context Protocol
A conversational interface that connects Azure OpenAI with Garak, a comprehensive AI safety testing framework, allowing the AI model to help with AI safety assessments and evaluations.

## Features

- 🤖 Conversational AI powered by Azure OpenAI GPT-4
- 🛡️ AI safety testing and evaluation capabilities
- 💬 Interactive chat interface
- 🔍 Prompt injection detection and prevention
- 📊 Model behavior analysis
- 🚨 Security testing methodologies
- 🎯 Red teaming approaches
- 🔗 MCP (Model Context Protocol) server integration

## Three Interface Types

### 1. **Regular Conversational Interface** (`garak_conversational_interface.py`)
- Direct Azure OpenAI integration
- AI safety knowledge and guidance
- No MCP server required
- Faster startup and simpler setup

### 2. **MCP Conversational Interface** (`garak_mcp_conversational_interface.py`)
- Connects to Garak MCP server via stdio transport
- Full MCP tool integration
- Research agent interaction
- Safety evaluation execution
- Agent management capabilities

### 3. **MCP Simple Interface** (`garak_mcp_simple_conversation.py`) ⭐ **Recommended**
- Direct module import (no MCP client library)
- Same functionality as MCP interface
- More reliable on Windows
- Faster startup
- No MCP client dependency issues
- **Best choice for most users**

## AI Safety Capabilities

The interface specializes in AI safety and security, including:

### 🛡️ **Safety Testing**
- Prompt injection vulnerability testing
- Model behavior analysis
- Security assessment methodologies
- Risk evaluation frameworks

### 🔍 **Detection & Prevention**
- Prompt injection attack detection
- Safety vulnerability identification
- Prevention strategy recommendations
- Best practice guidance

### 📊 **Analysis & Reporting**
- Model response analysis
- Safety metric evaluation
- Comprehensive testing reports
- Actionable recommendations

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   ```bash
   # Set your Azure OpenAI credentials
   export AZURE_OPENAI_API_KEY="your_azure_api_key_here"
   export AZURE_OPENAI_ENDPOINT="your_azure_endpoint_here"
   ```

3. **Run the conversational interface:**

   **For Regular Interface:**
   ```bash
   python start_garak_conversation.py
   ```

   **For MCP Interface (requires MCP client library):**
   ```bash
   python start_garak_mcp_conversation.py
   ```

   **For MCP Simple Interface (recommended):**
   ```bash
   python start_garak_simple.py
   ```

## Usage

Once started, you can interact with the AI using natural language. The AI specializes in AI safety and security topics.

### Regular Interface Examples

**User:** "What are the main types of prompt injection attacks?"
- AI will explain different prompt injection techniques and their risks

**User:** "How do I test an AI model for safety vulnerabilities?"
- AI will provide comprehensive testing methodologies and approaches

### MCP Interface Examples

**User:** "Ask the research agent about AI safety vulnerabilities"
- AI will use the MCP server to ask the research agent

**User:** "Run a safety evaluation with promptinject plugin"
- AI will execute a Garak safety evaluation through the MCP server

**User:** "Show me the conversation history"
- AI will retrieve the agent's conversation history

**User:** "Update the agent role to focus on prompt injection testing"
- AI will update the research agent's role

### Special Commands

**Regular Interface:**
- **`garak`** - Run a Garak evaluation
- **`plugins`** - See available Garak plugins
- **`quit`** or **`exit`** - End the conversation

**MCP Interface:**
- **`tools`** - See available MCP tools
- **`quit`** or **`exit`** - End the conversation

## MCP Server Tools

The MCP interface provides access to these tools:

- **`ask_research_agent`** - Ask the research agent a question
- **`run_safety_evaluation`** - Run Garak safety evaluation
- **`get_agent_history`** - Get conversation history
- **`reset_agent`** - Reset conversation history
- **`update_agent_role`** - Update agent's role

## Configuration

The Azure OpenAI configuration is set in the code:
- **Endpoint:** `https://opeanai-eastus.openai.azure.com/`
- **API Key:** `a00d081fe4b849beb5b5c0c4ed8d837f`
- **Model:** `gpt4o` (Latest GPT-4 model)
- **API Version:** `2024-07-01-preview` (Latest API version)

To change these settings, modify the constants in the interface files.

## Architecture

### Regular Interface:
```
User Input → Azure OpenAI → AI Safety Analysis → Response
```

### MCP Interface:
```
User Input → Azure OpenAI → Tool Selection → Garak MCP Server → Tool Execution → Response
```

### MCP Simple Interface:
```
User Input → Azure OpenAI → Tool Selection → Direct Module Calls → Response
```

## Testing

Use the provided test scripts to verify functionality:

```bash
# Test the regular conversational interface
python test_garak_conversation.py

# Test the MCP conversational interface
python test_garak_mcp_conversation.py

# Test the MCP simple interface (recommended)
python test_garak_simple.py

# Run the regular interactive interface
python start_garak_conversation.py

# Run the MCP interactive interface
python start_garak_mcp_conversation.py

# Run the MCP simple interactive interface (recommended)
python start_garak_simple.py
```

## Files

### Regular Interface:
- `garak_conversational_interface.py` - Main conversational interface
- `start_garak_conversation.py` - Startup script
- `test_garak_conversation.py` - Test script

### MCP Interface:
- `garak/mcp_app/garak_mcp_conversational_interface.py` - MCP conversational interface
- `start_garak_mcp_conversation.py` - MCP startup script
- `test_garak_mcp_conversation.py` - MCP test script

### MCP Simple Interface (Recommended):
- `garak_mcp_simple_conversation.py` - Simple MCP conversational interface
- `start_garak_simple.py` - Simple MCP startup script
- `test_garak_simple.py` - Simple MCP test script

### Shared:
- `requirements.txt` - Python dependencies
- `README.md` - This file

## Which Interface Should You Use?

### 🟢 **Use MCP Simple Interface** (Recommended)
- ✅ Most reliable on Windows
- ✅ No MCP client library dependency issues
- ✅ Faster startup
- ✅ Same functionality as full MCP interface
- ✅ Direct module imports

### 🟡 **Use Regular Interface**
- ✅ Simple setup
- ✅ No MCP server required
- ✅ Good for basic AI safety discussions
- ❌ No tool calling capabilities

### 🔴 **Use MCP Interface** (Advanced)
- ✅ Full MCP protocol support
- ✅ Standard MCP client library
- ❌ Complex setup on Windows
- ❌ MCP client library compatibility issues
- ❌ Slower startup

## Example Use Cases

1. **AI Safety Assessment:** "Evaluate the safety of this AI model"
2. **Prompt Injection Testing:** "Test for prompt injection vulnerabilities"
3. **Security Analysis:** "Analyze this model's security posture"
4. **Red Teaming:** "Help me red team this AI system"
5. **Best Practices:** "What are the best practices for AI safety?"
6. **Risk Assessment:** "Assess the risks of this AI application"

## Troubleshooting

- **Import errors:** Make sure all dependencies are installed with `pip install -r requirements.txt`
- **API errors:** Verify your Azure OpenAI credentials and endpoint
- **MCP server errors:** Ensure the Garak MCP server is properly set up
- **Model errors:** Check that the GPT-4 model is available in your Azure deployment

## AI Safety Focus

This interface is specifically designed for AI safety professionals, researchers, and developers who need to:

- **Test AI models** for safety vulnerabilities
- **Understand attack vectors** and prevention strategies
- **Implement safety measures** in AI systems
- **Conduct security assessments** of AI applications
- **Stay informed** about the latest AI safety developments

The AI assistant is trained to provide thorough, analytical responses focused on AI safety and security best practices. 
