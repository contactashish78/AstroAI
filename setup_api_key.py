#!/usr/bin/env python3
"""
Helper script to set up OpenAI API key
"""

import os

def setup_api_key():
    """Interactive API key setup"""
    print("🔑 OpenAI API Key Setup")
    print("=" * 30)
    
    print("\n📋 Instructions:")
    print("1. Go to: https://platform.openai.com/account/api-keys")
    print("2. Click 'Create new secret key'")
    print("3. Copy the key (it starts with 'sk-')")
    print("4. Paste it below")
    
    while True:
        api_key = input("\n🔑 Enter your OpenAI API key: ").strip()
        
        if not api_key:
            print("❌ No key entered. Please try again.")
            continue
        
        if not api_key.startswith('sk-'):
            print("❌ Invalid key format. OpenAI keys start with 'sk-'")
            continue
        
        if len(api_key) < 20:
            print("❌ Key seems too short. Please check and try again.")
            continue
        
        break
    
    # Create .env file
    env_content = f"OPENAI_API_KEY={api_key}\n"
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("✅ API key saved to .env file!")
        
        # Also set environment variable for current session
        os.environ['OPENAI_API_KEY'] = api_key
        print("✅ Environment variable set for current session!")
        
        print("\n🎉 Setup complete! You can now:")
        print("   • Run: python test_api_key.py (to test)")
        print("   • Run: python -m streamlit run app.py (to start the app)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error saving .env file: {e}")
        print(f"💡 Manually set: set OPENAI_API_KEY={api_key}")
        return False

if __name__ == "__main__":
    setup_api_key()