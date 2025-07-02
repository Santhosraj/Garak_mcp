# Garak MCP Server

A Model Context Protocol (MCP) server that integrates [Garak](https://github.com/NVIDIA/garak) LLM vulnerability scanning capabilities with conversational AI agents powered by Azure OpenAI.

## Overview

This MCP server provides tools for:
- **AI Research Assistant**: A conversational agent that can answer questions and provide research assistance
- **Garak Safety Evaluation**: Run comprehensive LLM vulnerability assessments using Garak's probe framework
- **Azure OpenAI Integration**: Seamless integration with Azure OpenAI models for text generation
- **Conversation Management**: Track, manage, and export conversation histories

## Features

### 🤖 AI Research Agent
- **Conversational Interface**: Natural language interaction with an AI research assistant
- **Safety Checks**: Built-in content filtering to prevent harmful responses
- **Context Awareness**: Maintains conversation history for contextual responses
- **Role Customization**: Update agent roles and specializations dynamically

### 🔍 Garak Safety Evaluation
- **Comprehensive Testing**: Run multiple Garak probes to assess LLM vulnerabilities
- **Plugin Support**: Test against various attack vectors (prompt injection, jailbreaks, etc.)
- **Parallel Processing**: Configurable parallel execution for faster evaluation
- **Detailed Reporting**: Generate comprehensive evaluation reports

### ☁️ Azure OpenAI Integration
- **Model Flexibility**: Support for various Azure OpenAI models (GPT-4, GPT-3.5, etc.)
- **Rate Limiting**: Built-in request throttling to respect API limits
- **Error Handling**: Robust error handling and retry mechanisms
- **Configuration Management**: Environment-based configuration

## Installation

### Prerequisites

1. **Python 3.10+**
2. **Azure OpenAI Account** with API access
3. **Garak Installation** (optional, for safety evaluation features)

### Setup

1. **Clone the repository**:
   ```bash
   cd garak_working/garak/mcp_app/garak_mcp
   ```

2. **Install dependencies**:
   ```bash
   pip install mcp requests
   ```

3. **Install Garak** (for safety evaluation):
   ```bash
   pip install garak
   ```

4. **Configure Azure OpenAI**:
   Set the following environment variables:
   ```bash
   export AZURE_ENDPOINT="https://your-endpoint.openai.azure.com/"
   export AZURE_API_KEY="your-api-key"
   export AZURE_MODEL_NAME="gpt4o"  # or your preferred model
   ```

## Usage

### Starting the MCP Server

```bash
python server.py
```

The server will start and listen for MCP client connections.

### Available Tools

#### 1. `ask_research_agent`
Ask the AI research assistant a question.

**Parameters:**
- `question` (string, required): The question to ask the agent

**Example:**
```json
{
  "name": "ask_research_agent",
  "arguments": {
    "question": "What are the latest developments in AI safety?"
  }
}
```

#### 2. `run_safety_evaluation`
Run Garak safety evaluation on a model.

**Parameters:**
- `model_string` (string, optional): Model identifier (default: "azure:gpt4o")
- `plugins` (array, optional): List of Garak plugins to run (default: ["promptinject"])

**Example:**
```json
{
  "name": "run_safety_evaluation",
  "arguments": {
    "model_string": "azure:gpt4o",
    "plugins": ["promptinject", "dan", "encoding"]
  }
}
```

#### 3. `get_agent_history`
Retrieve the current conversation history.

**Example:**
```json
{
  "name": "get_agent_history",
  "arguments": {}
}
```

#### 4. `reset_agent`
Clear the agent's conversation history.

**Example:**
```json
{
  "name": "reset_agent",
  "arguments": {}
}
```

#### 5. `update_agent_role`
Update the agent's role/system prompt.

**Parameters:**
- `new_role` (string, required): The new role description

**Example:**
```json
{
  "name": "update_agent_role",
  "arguments": {
    "new_role": "You are an expert cybersecurity analyst specializing in threat detection."
  }
}
```

### Available Resources

#### `agent://history`
Current conversation history with the research agent.

#### `agent://config`
Current agent configuration and settings.

## Architecture

### Core Components

1. **`server.py`**: MCP server implementation with tool and resource handlers
2. **`agents.py`**: AI agent classes with conversation management and safety features
3. **`azure_model.py`**: Azure OpenAI client with configuration and error handling
4. **`eval_garak.py`**: Garak evaluation wrapper with enhanced reporting

### Agent Classes

#### `MCPAgent`
Base agent class with:
- Conversation history management
- Safety content filtering
- Role-based prompting
- Error handling and logging

#### `SpecializedAgent`
Extended agent with domain-specific capabilities:
- Specialization context
- Enhanced prompting for specific domains
- Custom keyword handling

### Azure OpenAI Client

The `AzureOpenAIClient` class provides:
- **Configuration Management**: Environment-based settings
- **Rate Limiting**: Request throttling to respect API limits
- **Error Handling**: Comprehensive error handling and retry logic
- **Token Usage Tracking**: Monitor API usage and costs

### Garak Evaluator

The `GarakEvaluator` class offers:
- **Plugin Management**: Support for various Garak probes
- **Parallel Execution**: Configurable parallel processing
- **Report Generation**: Detailed evaluation reports
- **History Tracking**: Maintain evaluation history

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AZURE_ENDPOINT` | Azure OpenAI endpoint URL | Required |
| `AZURE_API_KEY` | Azure OpenAI API key | Required |
| `AZURE_MODEL_NAME` | Model name to use | `gpt4o` |
| `AZURE_API_VERSION` | API version | `2024-06-01` |

### Garak Configuration

Garak evaluation can be configured with:
- **Model Type**: Azure, OpenAI, HuggingFace, etc.
- **Plugins**: List of probes to run
- **Parallel Settings**: Number of parallel attempts and requests
- **Output Directory**: Where to save evaluation reports

## Examples

### Basic Research Query
```python
# Ask the research agent a question
response = await client.call_tool("ask_research_agent", {
    "question": "Explain the concept of prompt injection attacks"
})
```

### Safety Evaluation
```python
# Run comprehensive safety evaluation
result = await client.call_tool("run_safety_evaluation", {
    "model_string": "azure:gpt4o",
    "plugins": ["promptinject", "dan", "encoding", "misleading"]
})
```

### Agent Management
```python
# Update agent role
await client.call_tool("update_agent_role", {
    "new_role": "You are an expert in machine learning and AI ethics."
})

# Get conversation history
history = await client.call_tool("get_agent_history", {})
```

## Error Handling

The server includes comprehensive error handling:

- **API Errors**: Graceful handling of Azure OpenAI API errors
- **Network Issues**: Connection error recovery
- **Invalid Inputs**: Input validation and helpful error messages
- **Garak Failures**: Fallback handling for evaluation failures

## Logging

The server uses Python's logging module with:
- **INFO Level**: General operation logs
- **ERROR Level**: Error conditions and failures
- **DEBUG Level**: Detailed debugging information

Logs include:
- API request/response details
- Agent conversation tracking
- Garak evaluation progress
- Error conditions and stack traces

## Security Considerations

- **API Key Protection**: Never expose API keys in logs or responses
- **Content Filtering**: Built-in safety checks for harmful content
- **Rate Limiting**: Prevents API abuse and excessive costs
- **Input Validation**: Validates all user inputs before processing

## Troubleshooting

### Common Issues

1. **Azure API Key Error**
   - Ensure `AZURE_API_KEY` is set correctly
   - Verify the API key has proper permissions

2. **Garak Not Found**
   - Install Garak: `pip install garak`
   - Verify Garak installation: `python -c "import garak"`

3. **Rate Limit Errors**
   - The client includes automatic rate limiting
   - Wait between requests if you encounter rate limits

4. **Model Not Found**
   - Verify the model name in `AZURE_MODEL_NAME`
   - Check if the model is available in your Azure deployment

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is part of the Garak ecosystem and follows the same licensing terms.

## Support

- **Documentation**: [Garak Documentation](https://docs.garak.ai/)
- **Discord**: [Garak Discord Community](https://discord.gg/uVch4puUCs)
- **GitHub**: [Garak Repository](https://github.com/NVIDIA/garak)
- **Website**: [garak.ai](https://garak.ai/)

## Related Projects

- [Garak](https://github.com/NVIDIA/garak): LLM vulnerability scanner
- [MCP](https://modelcontextprotocol.io/): Model Context Protocol
- [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service): Azure OpenAI Service 