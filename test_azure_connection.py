#!/usr/bin/env python3
"""
Test Azure OpenAI connection with correct deployment name
"""

import os
import openai

def test_azure_connection():
    """Test Azure OpenAI connection"""
    print("🧪 Testing Azure OpenAI Connection")
    print("=" * 40)
    
    # Set credentials
    api_key = "a00d081fe4b849beb5b5c0c4ed8d837f"
    endpoint = "https://opeanai-eastus.openai.azure.com/"
    deployment_name = "gpt4o"  # Correct deployment name
    api_version = "2024-06-01"
    
    print(f"🔑 API Key: {api_key[:8]}...")
    print(f"🌐 Endpoint: {endpoint}")
    print(f"🤖 Deployment: {deployment_name}")
    print(f"📅 API Version: {api_version}")
    print()
    
    try:
        # Create client
        client = openai.AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version=api_version
        )
        
        print("✅ Azure OpenAI client created successfully")
        
        # Test simple request
        print("📤 Sending test request...")
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "user", "content": "Hello! Please respond with 'Connection successful!'"}
            ],
            max_tokens=50,
            temperature=0.7
        )
        
        result = response.choices[0].message.content
        print(f"📥 Response: {result}")
        
        if "Connection successful" in result:
            print("🎉 Azure OpenAI connection test PASSED!")
            return True
        else:
            print("⚠️  Response received but not as expected")
            return False
            
    except Exception as e:
        print(f"❌ Azure OpenAI connection test FAILED: {e}")
        return False

def main():
    """Main function"""
    success = test_azure_connection()
    
    if success:
        print("\n✅ You can now run the Garak MCP interfaces!")
        print("Try: python garak/mcp_app/garak_mcp_simple_conversation.py")
    else:
        print("\n❌ Please check your Azure configuration")

if __name__ == "__main__":
    main() 