#!/usr/bin/env python3
"""
Test script for Garak Conversational Interface
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
logger = logging.getLogger("test-garak-conversation")

async def test_garak_conversation():
    """Test the Garak conversational interface"""
    
    # Import the conversational interface
    from garak_conversational_interface import GarakConversationalInterface
    
    async with GarakConversationalInterface() as interface:
        print("🧪 Testing Garak Conversational Interface\n")
        
        # Test 1: Basic conversation
        print("1️⃣ Testing basic conversation...")
        response = await interface.chat("Hello! Can you tell me about AI safety testing?")
        print(response)
        print("\n" + "="*60 + "\n")
        
        # Test 2: AI safety question
        print("2️⃣ Testing AI safety knowledge...")
        response = await interface.chat("What are the main types of prompt injection attacks?")
        print(response)
        print("\n" + "="*60 + "\n")
        
        # Test 3: Garak plugins
        print("3️⃣ Testing Garak plugins info...")
        response = await interface.get_available_plugins()
        print(response)
        print("\n" + "="*60 + "\n")
        
        # Test 4: Complex AI safety question
        print("4️⃣ Testing complex AI safety reasoning...")
        response = await interface.chat(
            "How would you approach testing an AI model for safety vulnerabilities? " +
            "What are the key areas to focus on?"
        )
        print(response)
        print("\n" + "="*60 + "\n")

def print_model_info():
    """Print information about the current model configuration"""
    from garak_conversational_interface import AZURE_ENDPOINT, MODEL, API_VERSION
    
    print("📋 Current Model Configuration:")
    print(f"  Endpoint: {AZURE_ENDPOINT}")
    print(f"  Model: {MODEL}")
    print(f"  API Version: {API_VERSION}")
    print()
    
    print("✅ Garak Features:")
    print("  • AI safety testing and evaluation")
    print("  • Prompt injection detection")
    print("  • Model behavior analysis")
    print("  • Security testing methodologies")
    print("  • Red teaming approaches")
    print()

async def main():
    """Main test function"""
    print("🚀 Testing Garak Conversational Interface\n")
    
    # Print model information
    print_model_info()
    
    try:
        await test_garak_conversation()
        print("\n" + "🎉 Garak conversational interface test completed successfully!")
        print("✅ The latest GPT-4 model is working correctly with Garak!")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        print(f"❌ Test failed: {e}")
        print("This might indicate an issue with the model configuration or Garak setup.")

if __name__ == "__main__":
    asyncio.run(main()) 