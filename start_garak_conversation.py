#!/usr/bin/env python3
"""
Startup script for the Garak Conversational Interface
"""

import os
import sys
import asyncio
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Set environment variables for Azure OpenAI

os.environ.setdefault("AZURE_API_KEY", "")
os.environ.setdefault("AZURE_ENDPOINT", "")
os.environ.setdefault("AZURE_MODEL_NAME", "gpt-4o")

async def main():
    """Main entry point"""
    try:
        print("🚀 Starting Garak Conversational Interface...")
        
        from garak_conversational_interface import GarakConversationalInterface
        
        async with GarakConversationalInterface() as interface:
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
