#!/usr/bin/env python3
"""
Startup script for the Garak MCP Simple Conversational Interface
"""

import os
import sys
import asyncio
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Set environment variables for Azure OpenAI
os.environ.setdefault("AZURE_OPENAI_ENDPOINT", "https://opeanai-eastus.openai.azure.com/")
os.environ.setdefault("AZURE_OPENAI_API_KEY", "a00d081fe4b849beb5b5c0c4ed8d837f")
os.environ.setdefault("AZURE_OPENAI_MODEL", "gpt4o")
os.environ.setdefault("AZURE_API_KEY", "a00d081fe4b849beb5b5c0c4ed8d837f")
os.environ.setdefault("AZURE_ENDPOINT", "https://opeanai-eastus.openai.azure.com/")
os.environ.setdefault("AZURE_MODEL_NAME", "gpt-4o")

async def main():
    """Main entry point"""
    try:
        print("🚀 Starting Garak MCP Simple Conversational Interface...")
        
        # Check if Garak modules exist
        garak_path = Path(__file__).parent / "garak" / "mcp_app"
        if not garak_path.exists():
            print(f"❌ Garak modules not found at: {garak_path}")
            print("Please ensure the Garak MCP server is properly set up.")
            return
        
        from garak_working.garak_mcp_final.garak_mcp_simple_conversation import GarakMCPSimpleConversationalInterface
        
        async with GarakMCPSimpleConversationalInterface() as interface:
            await interface.interactive_chat()
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install required dependencies:")
        print("pip install openai asyncio")
    except Exception as e:
        print(f"❌ Error starting interface: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main()) 