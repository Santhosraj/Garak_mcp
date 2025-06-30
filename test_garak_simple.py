#!/usr/bin/env python3
"""
Test script for the Garak Simple Conversational Interface
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Set environment variables for Azure OpenAI
os.environ.setdefault("AZURE_OPENAI_ENDPOINT", "https://opeanai-eastus.openai.azure.com/")
os.environ.setdefault("AZURE_OPENAI_API_KEY", "a00d081fe4b849beb5b5c0c4ed8d837f")

def test_garak_simple_interface():
    """Test the Garak simple conversational interface"""
    try:
        print("🧪 Testing Garak Simple Conversational Interface...")
        
        # Import the interface
        from garak_working.garak_mcp_final.garak_mcp_simple_conversation import GarakMCPSimpleConversation
        
        # Create the interface
        interface = GarakMCPSimpleConversation()
        print("✅ Successfully created GarakMCPSimpleConversation instance")
        
        # Test tool listing
        tools = interface._get_available_tools()
        print(f"✅ Found {len(tools)} available tools:")
        for tool in tools:
            print(f"  • {tool['function']['name']}: {tool['function']['description']}")
        
        # Test asking the research agent
        print("\n🧪 Testing ask_research_agent tool...")
        result = interface._call_tool("ask_research_agent", {"question": "What is AI safety?"})
        print(f"✅ Research agent response: {result[:200]}...")
        
        # Test getting agent history
        print("\n🧪 Testing get_agent_history tool...")
        history = interface._call_tool("get_agent_history", {})
        print(f"✅ Agent history: {history}")
        
        # Test chat function
        print("\n🧪 Testing chat function...")
        response = interface.chat("Hello! Can you tell me about AI safety?")
        print(f"✅ Chat response: {response[:200]}...")
        
        print("\n🎉 All tests passed! The Garak Simple Conversational Interface is working correctly.")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure the Garak MCP server components are available.")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def test_tool_calling():
    """Test specific tool calling functionality"""
    try:
        print("\n🧪 Testing specific tool calling...")
        
        from garak_working.garak_mcp_final.garak_mcp_simple_conversation import GarakMCPSimpleConversation
        interface = GarakMCPSimpleConversation()
        
        # Test reset agent
        print("Testing reset_agent...")
        result = interface._call_tool("reset_agent", {})
        print(f"✅ Reset result: {result}")
        
        # Test update agent role
        print("Testing update_agent_role...")
        result = interface._call_tool("update_agent_role", {"new_role": "You are an AI safety expert."})
        print(f"✅ Update role result: {result}")
        
        # Test safety evaluation (this might take a while)
        print("Testing run_safety_evaluation...")
        result = interface._call_tool("run_safety_evaluation", {
            "model_string": "azure:gpt4",
            "plugins": ["promptinject"]
        })
        print(f"✅ Safety evaluation result: {result[:200]}...")
        
        # Test list probes
        print("Testing list_probes...")
        result = interface._call_tool("list_probes", {})
        print(f"✅ List probes result: {result[:200]}...")
        
        # Test list probes with category filter
        print("Testing list_probes with category filter...")
        result = interface._call_tool("list_probes", {"category": "promptinject"})
        print(f"✅ List probes (promptinject) result: {result[:200]}...")
        
        print("🎉 Tool calling tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Tool calling test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting Garak Simple Conversational Interface Tests...")
    print("=" * 60)
    
    # Run basic tests
    if not test_garak_simple_interface():
        print("❌ Basic tests failed!")
        return
    
    # Run tool calling tests
    if not test_tool_calling():
        print("❌ Tool calling tests failed!")
        return
    
    print("\n🎉 All tests completed successfully!")
    print("The Garak Simple Conversational Interface is ready to use.")
    print("\nTo start the interface, run:")
    print("python start_garak_simple.py")

if __name__ == "__main__":
    main() 