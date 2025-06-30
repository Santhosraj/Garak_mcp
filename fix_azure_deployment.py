#!/usr/bin/env python3
"""
Fix Azure deployment configuration for Garak MCP
"""

import os
import requests
import json
from typing import List, Optional

def set_azure_credentials():
    """Set Azure credentials"""
    os.environ["AZURE_API_KEY"] = "a00d081fe4b849beb5b5c0c4ed8d837f"
    os.environ["AZURE_ENDPOINT"] = "https://opeanai-eastus.openai.azure.com/"
    os.environ["AZURE_API_VERSION"] = "2024-06-01"

def test_deployment_name(endpoint: str, api_key: str, deployment_name: str, api_version: str = "2024-06-01") -> bool:
    """Test if a deployment name exists"""
    url = f"{endpoint}openai/deployments/{deployment_name}/chat/completions?api-version={api_version}"
    
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }
    
    data = {
        "messages": [{"role": "user", "content": "Hello"}],
        "max_tokens": 10
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            return True
        elif response.status_code == 404:
            return False
        else:
            print(f"  Status {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"  Error: {e}")
        return False

def find_correct_deployment() -> Optional[str]:
    """Find the correct deployment name"""
    set_azure_credentials()
    
    endpoint = os.environ["AZURE_ENDPOINT"]
    api_key = os.environ["AZURE_API_KEY"]
    
    # Common deployment names to try
    deployment_names = [
        "gpt-4o",
        "gpt4o", 
        "gpt-4",
        "gpt4",
        "gpt-35-turbo",
        "gpt35turbo",
        "gpt-35-turbo-16k",
        "gpt-4-turbo",
        "gpt4turbo"
    ]
    
    print("🔍 Testing Azure deployment names...")
    print("=" * 50)
    
    working_deployments = []
    
    for deployment in deployment_names:
        print(f"Testing: {deployment}")
        if test_deployment_name(endpoint, api_key, deployment):
            print(f"  ✅ {deployment} - WORKING")
            working_deployments.append(deployment)
        else:
            print(f"  ❌ {deployment} - Not found")
    
    if working_deployments:
        print(f"\n🎉 Found {len(working_deployments)} working deployment(s):")
        for dep in working_deployments:
            print(f"  - {dep}")
        return working_deployments[0]  # Return the first working one
    else:
        print("\n❌ No working deployments found!")
        print("\nTo fix this:")
        print("1. Go to your Azure OpenAI resource in the Azure Portal")
        print("2. Under 'Deployments', create a new deployment")
        print("3. Choose GPT-4o or GPT-4 model")
        print("4. Give it a deployment name (e.g., 'gpt-4o' or 'gpt4o')")
        print("5. Use that exact name in your configuration")
        return None

def update_config_files(correct_deployment: str):
    """Update configuration files with the correct deployment name"""
    print(f"\n🔧 Updating configuration files with deployment: {correct_deployment}")
    print("=" * 50)
    
    # Files to update
    files_to_update = [
        "garak/mcp_app/garak_mcp/azure_model.py",
        "garak/mcp_app/garak_mcp_simple_conversation.py",
        "garak_conversational_interface.py",
        "garak_mcp_conversational_interface.py"
    ]
    
    for file_path in files_to_update:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace common deployment name patterns
                updated_content = content.replace(
                    'os.getenv("AZURE_MODEL_NAME", "gpt-4o")',
                    f'os.getenv("AZURE_MODEL_NAME", "{correct_deployment}")'
                )
                updated_content = updated_content.replace(
                    'os.getenv("AZURE_MODEL_NAME", "gpt4o")',
                    f'os.getenv("AZURE_MODEL_NAME", "{correct_deployment}")'
                )
                updated_content = updated_content.replace(
                    'model = "gpt-4o"',
                    f'model = "{correct_deployment}"'
                )
                updated_content = updated_content.replace(
                    'model = "gpt4o"',
                    f'model = "{correct_deployment}"'
                )
                
                if content != updated_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    print(f"✅ Updated: {file_path}")
                else:
                    print(f"⏭️  No changes needed: {file_path}")
                    
            except Exception as e:
                print(f"❌ Error updating {file_path}: {e}")
        else:
            print(f"⏭️  File not found: {file_path}")

def create_env_file(correct_deployment: str):
    """Create a .env file with the correct configuration"""
    env_content = f"""# Azure OpenAI Configuration
AZURE_API_KEY=a00d081fe4b849beb5b5c0c4ed8d837f
AZURE_ENDPOINT=https://opeanai-eastus.openai.azure.com/
AZURE_MODEL_NAME={correct_deployment}
AZURE_API_VERSION=2024-06-01

# Garak Configuration
GARAK_PATH=garak
GARAK_OUTPUT_DIR=garak_results
"""
    
    try:
        with open(".env", 'w') as f:
            f.write(env_content)
        print(f"✅ Created .env file with deployment: {correct_deployment}")
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")

def main():
    """Main function"""
    print("🚀 Azure Deployment Configuration Fixer")
    print("=" * 60)
    
    # Find correct deployment
    correct_deployment = find_correct_deployment()
    
    if correct_deployment:
        print(f"\n🎯 Using deployment: {correct_deployment}")
        
        # Update configuration files
        update_config_files(correct_deployment)
        
        # Create .env file
        create_env_file(correct_deployment)
        
        print(f"\n✅ Configuration updated successfully!")
        print(f"📝 Deployment name: {correct_deployment}")
        print(f"🔑 API Key: {os.environ['AZURE_API_KEY'][:8]}...")
        print(f"🌐 Endpoint: {os.environ['AZURE_ENDPOINT']}")
        
        print(f"\n🚀 You can now run your Garak MCP interfaces!")
        print("Try: python garak/mcp_app/garak_mcp_simple_conversation.py")
        
    else:
        print("\n❌ Please create a deployment in Azure OpenAI first!")
        print("Then run this script again.")

if __name__ == "__main__":
    main() 