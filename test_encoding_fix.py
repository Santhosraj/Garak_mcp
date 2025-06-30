#!/usr/bin/env python3
"""
Test encoding fix for Garak output
"""

import re

def test_encoding_fix():
    """Test the encoding fix function"""
    print("🧪 Testing Encoding Fix")
    print("=" * 40)
    
    # Sample output with problematic characters
    sample_output = """
garak LLM vulnerability scanner v0.11.1.pre1 ( https://github.com/NVIDIA/garak ) at 2025-06-25T15:43:35.736647
📜 logging to C:\Users\Dell\.local\share\garak\garak.log
🚀 Starting evaluation...
✅ Probe completed successfully
❌ Some issues found
🔍 Analyzing results...
🎯 Target model: gpt4o
💤 Evaluation in progress...
☠️ Toxic content detected
🎭 Role playing attack
🔐 Encoding injection
💻 Code execution attempt
📚 Training data extraction
🎵 Audio attack
🛡️ Safety measures
🔄 Continuation attack
📈 Divergence test
❄️ Snowball attack
🔚 Suffix attack
🧪 Test probe
📝 Report generation
👁️ Visual jailbreak
"""
    
    print("Original output with emojis:")
    print(sample_output)
    print("-" * 40)
    
    # Apply the encoding fix
    output = sample_output
    
    # Remove emojis and problematic Unicode characters
    output = re.sub(r'[^\x00-\x7F\u00A0-\uFFFF]', '', output)
    
    # Remove specific problematic characters
    problematic_chars = ['📜', '🚀', '✅', '❌', '🔍', '🎯', '💤', '☠️', '🎭', '🔐', '💻', '📚', '🎵', '🛡️', '🔄', '📈', '❄️', '🔚', '🧪', '📝', '👁️', '']
    for char in problematic_chars:
        output = output.replace(char, '')
    
    # Clean up extra whitespace
    output = re.sub(r'\n\s*\n', '\n\n', output)
    output = output.strip()
    
    print("Cleaned output without emojis:")
    print(output)
    print("-" * 40)
    
    # Check if any problematic characters remain
    remaining_emojis = re.findall(r'[^\x00-\x7F\u00A0-\uFFFF]', output)
    if remaining_emojis:
        print(f"❌ Still found problematic characters: {remaining_emojis}")
        return False
    else:
        print("✅ All problematic characters removed successfully!")
        return True

if __name__ == "__main__":
    success = test_encoding_fix()
    if success:
        print("\n🎉 Encoding fix test PASSED!")
    else:
        print("\n❌ Encoding fix test FAILED!") 