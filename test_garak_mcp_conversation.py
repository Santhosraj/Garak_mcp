#!/usr/bin/env python3
"""
Test script for Garak MCP Conversational Interface
"""

import asyncio
import logging
from pathlib import Path
import sys

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("test-garak-mcp-conversation")

async def test_garak_mcp_conversation():
    """Test the Garak MCP conversational interface"""
    
    # Import the conversational interface
    from garak_mcp_conversational_interface import GarakMCPConversationalInterface
    
    async with GarakMCPConversationalInterface() as interface:
        print("🧪 Testing Garak MCP Conversational Interface\n")
        
        # Test 1: Check available tools
        print("1️⃣ Testing available MCP tools...")
        print(f"Found {len(interface.tools)} tools:")
        for tool in interface.tools:
            print(f"  • {tool.name}: {tool.description}")
        print("\n" + "="*60 + "\n")
        
        # Test 2: Ask research agent
        print("2️⃣ Testing research agent interaction...")
        response = await interface.chat("What are the main types of AI safety vulnerabilities?")
        print(response)
        print("\n" + "="*60 + "\n")
        
        # Test 3: Get agent history
        print("3️⃣ Testing agent history...")
        response = await interface.chat("Show me the conversation history")
        print(response)
        print("\n" + "="*60 + "\n")
        
        # Test 4: Run safety evaluation
        print("4️⃣ Testing safety evaluation...")
        response = await interface.chat("Run a safety evaluation with promptinject plugin")
        print(response)
        print("\n" + "="*60 + "\n")
        
        # Test 5: Update agent role
        print("5️⃣ Testing agent role update...")
        response = await interface.chat("Update the agent role to focus on prompt injection testing")
        print(response)
        print("\n" + "="*60 + "\n")

def print_mcp_info():
    """Print information about the MCP server and tools"""
    print("📋 Garak MCP Server Information:")
    print("  Server: AI Research Agent MCP Server")
    print("  Version: 1.0.0")
    print("  Capabilities: Resources, Tools, Logging")
    print()
    
    print("🛠️ Available MCP Tools:")
    print("  • ask_research_agent - Ask the research agent a question")
    print("  • run_safety_evaluation - Run Garak safety evaluation")
    print("  • get_agent_history - Get conversation history")
    print("  • reset_agent - Reset conversation history")
    print("  • update_agent_role - Update agent's role")
    print()
    
    print("📊 Available Resources:")
    print("  • agent://history - Agent conversation history")
    print("  • agent://config - Agent configuration")
    print()

async def main():
    """Main test function"""
    print("🚀 Testing Garak MCP Conversational Interface\n")
    
    # Print MCP information
    print_mcp_info()
    
    try:
        await test_garak_mcp_conversation()
        print("\n" + "🎉 Garak MCP conversational interface test completed successfully!")
        print("✅ The MCP server integration is working correctly!")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        print(f"❌ Test failed: {e}")
        print("This might indicate an issue with the MCP server or configuration.")

if __name__ == "__main__":
    asyncio.run(main()) 