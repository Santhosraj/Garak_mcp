#!/usr/bin/env python3
"""
Test script for Garak MCP Simple Conversational Interface
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
logger = logging.getLogger("test-garak-mcp-simple")

async def test_garak_mcp_simple():
    """Test the Garak MCP simple conversational interface"""
    
    # Import the conversational interface
    from garak_working.garak_mcp_final.garak_mcp_simple_conversation import GarakMCPSimpleConversationalInterface
    
    async with GarakMCPSimpleConversationalInterface() as interface:
        print("🧪 Testing Garak MCP Simple Conversational Interface\n")
        
        # Test 1: Check available tools
        print("1️⃣ Testing available MCP tools...")
        print(f"Found {len(interface.tools)} tools:")
        for tool in interface.tools:
            print(f"  • {tool['function']['name']}: {tool['function']['description']}")
        print("\n" + "="*60 + "\n")
        
        # Test 2: Ask research agent
        print("2️⃣ Testing research agent interaction...")
        response = await interface.chat("Ask the research agent: What are the main types of AI safety vulnerabilities?")
        print(response)
        print("\n" + "="*60 + "\n")
        
        # Test 3: Get agent history
        print("3️⃣ Testing agent history...")
        response = await interface.chat("Show me the conversation history")
        print(response)
        print("\n" + "="*60 + "\n")
        
        # Test 4: Update agent role
        print("4️⃣ Testing agent role update...")
        response = await interface.chat("Update the agent role to focus on prompt injection testing")
        print(response)
        print("\n" + "="*60 + "\n")
        
        # Test 5: Ask another question with updated role
        print("5️⃣ Testing with updated role...")
        response = await interface.chat("Ask the research agent: How can I test for prompt injection vulnerabilities?")
        print(response)
        print("\n" + "="*60 + "\n")

def print_simple_mcp_info():
    """Print information about the simple MCP interface"""
    print("📋 Garak MCP Simple Interface Information:")
    print("  Type: Direct module import (no MCP client library)")
    print("  Approach: Similar to Apify simple conversation")
    print("  Dependencies: Minimal (no MCP client required)")
    print()
    
    print("🛠️ Available Tools:")
    print("  • ask_research_agent - Ask the research agent a question")
    print("  • run_safety_evaluation - Run Garak safety evaluation")
    print("  • get_agent_history - Get conversation history")
    print("  • reset_agent - Reset conversation history")
    print("  • update_agent_role - Update agent's role")
    print()
    
    print("✅ Advantages:")
    print("  • No MCP client library dependency")
    print("  • Faster startup")
    print("  • More reliable on Windows")
    print("  • Direct access to Garak modules")
    print()

async def main():
    """Main test function"""
    print("🚀 Testing Garak MCP Simple Conversational Interface\n")
    
    # Print simple MCP information
    print_simple_mcp_info()
    
    try:
        await test_garak_mcp_simple()
        print("\n" + "🎉 Garak MCP simple conversational interface test completed successfully!")
        print("✅ The simple MCP interface is working correctly!")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        print(f"❌ Test failed: {e}")
        print("This might indicate an issue with the Garak modules or configuration.")

if __name__ == "__main__":
    asyncio.run(main()) 