#!/usr/bin/env python3
"""
List all available Garak probes and their purposes
"""

import os
import subprocess
import json
import sys
from pathlib import Path

# Add the garak directory to Python path
garak_path = Path(__file__).parent / "garak"
sys.path.insert(0, str(garak_path))

def set_azure_credentials():
    """Set Azure credentials from the MCP config"""
    os.environ["AZURE_API_KEY"] = "a00d081fe4b849beb5b5c0c4ed8d837f"
    os.environ["AZURE_ENDPOINT"] = "https://opeanai-eastus.openai.azure.com/"
    os.environ["AZURE_MODEL_NAME"] = "gpt-4o"
    os.environ["AZURE_API_VERSION"] = "2024-06-01"

def get_garak_probes():
    """Get list of Garak probes using the garak command"""
    try:
        result = subprocess.run(
            ["garak", "--list_probes"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error running garak: {e.stderr}"
    except FileNotFoundError:
        return "Error: garak command not found. Please install Garak first."

def analyze_probes_with_ai(probes_output):
    """Use Azure OpenAI to analyze and categorize the probes"""
    try:
        from mcp_app.garak_mcp.azure_model import azure_model
        
        prompt = f"""
Based on the following Garak probe list, provide a comprehensive analysis of all available probes and their purposes:

{probes_output}

Please organize the probes by category and explain what each category is designed to test. Include:
1. Main categories of attacks
2. Specific probe purposes
3. What vulnerabilities they target
4. Any notable patterns or themes

Format your response clearly with categories and explanations.
"""
        
        response = azure_model(prompt)
        return response
    except ImportError as e:
        return f"Error importing Azure model: {str(e)}"
    except Exception as e:
        return f"Error analyzing probes with AI: {str(e)}"

def main():
    """Main function to list and analyze Garak probes"""
    print("🔍 Analyzing Garak Probes...")
    print("=" * 60)
    
    # Set Azure credentials
    set_azure_credentials()
    
    # Get raw probe list
    print("1. Getting probe list from Garak...")
    probes_output = get_garak_probes()
    
    if "Error" in probes_output:
        print(f"❌ {probes_output}")
        return
    
    print("✅ Probe list retrieved successfully")
    
    # Analyze with AI
    print("\n2. Analyzing probes with AI...")
    analysis = analyze_probes_with_ai(probes_output)
    
    print("\n" + "=" * 60)
    print("📊 GARAK PROBES ANALYSIS")
    print("=" * 60)
    print(analysis)
    
    # Save to file
    with open("garak_probes_analysis.txt", "w") as f:
        f.write("GARAK PROBES ANALYSIS\n")
        f.write("=" * 60 + "\n")
        f.write(analysis)
    
    print(f"\n💾 Analysis saved to: garak_probes_analysis.txt")

if __name__ == "__main__":
    main() 