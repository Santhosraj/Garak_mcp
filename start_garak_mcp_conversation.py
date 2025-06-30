#!/usr/bin/env python3
"""
Startup script for the Garak MCP Conversational Interface
"""

import os
import sys
import asyncio
from pathlib import Path

# Add the garak/mcp_app directory to Python path
current_dir = Path(__file__).parent
mcp_app_dir = current_dir / "garak" / "mcp_app"
sys.path.insert(0, str(mcp_app_dir))

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
        print("🚀 Starting Garak MCP Conversational Interface...")
        
        # Check if MCP server exists
        server_script = current_dir / "garak" / "mcp_app" / "garak_mcp" / "main.py"
        if not server_script.exists():
            print(f"❌ MCP server not found at: {server_script}")
            print("Please ensure the Garak MCP server is properly set up.")
            return
        
        from garak_mcp_conversational_interface import GarakMCPConversationalInterface
        
        async with GarakMCPConversationalInterface() as interface:
            await interface.interactive_chat()
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install required dependencies:")
        print("pip install openai mcp asyncio")
    except Exception as e:
        print(f"❌ Error starting interface: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main()) 