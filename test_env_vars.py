#!/usr/bin/env python3
"""
Test environment variables for Garak
"""

import os
import subprocess

def test_environment_variables():
    """Test that environment variables are set correctly"""
    print("🧪 Testing Environment Variables for Garak")
    print("=" * 50)
    
    # Set environment variables
    env = os.environ.copy()
    env.update({
        "AZURE_API_KEY": "",
        "AZURE_ENDPOINT": "",
        "AZURE_MODEL_NAME": "gpt4o",
        "AZURE_API_VERSION": "2024-06-01"
    })
    
    print("Environment variables set:")
    for key, value in env.items():
        if key.startswith("AZURE_"):
            if "KEY" in key:
                print(f"  {key}: {value[:8]}...")
            else:
                print(f"  {key}: {value}")
    
    # Test with a simple Garak command
    print("\nTesting Garak command...")
    try:
        result = subprocess.run(
            ["garak", "--list_probes"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            env=env
        )
        
        if result.returncode == 0:
            print("✅ Garak command executed successfully!")
            print(f"Output length: {len(result.stdout)} characters")
            return True
        else:
            print(f"❌ Garak command failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error running Garak: {e}")
        return False

if __name__ == "__main__":
    test_environment_variables() 
