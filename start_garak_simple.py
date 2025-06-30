#!/usr/bin/env python3
"""
Startup script for the Garak Simple Conversational Interface
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Set environment variables for Azure OpenAI

os.environ.setdefault("AZURE_API_KEY", "")
os.environ.setdefault("AZURE_ENDPOINT", "")
os.environ.setdefault("AZURE_MODEL_NAME", "gpt-4o")

def main():
    """Main entry point"""
    try:
        print("🚀 Starting Garak Simple Conversational Interface...")
        
        # Check if Garak MCP components exist
        mcp_app_dir = current_dir / "garak" / "mcp_app"
        if not mcp_app_dir.exists():
            print(f"❌ Garak MCP app directory not found at: {mcp_app_dir}")
            print("Please ensure the Garak MCP server is properly set up.")
            return
        
        from garak_working.garak_mcp_final.garak_mcp_simple_conversation import GarakMCPSimpleConversation
        
        # Create the conversational interface
        interface = GarakMCPSimpleConversation()
        
        # Start interactive chat
        interface.interactive_chat()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install required dependencies:")
        print("pip install openai python-dotenv")
    except Exception as e:
        print(f"❌ Error starting interface: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 
