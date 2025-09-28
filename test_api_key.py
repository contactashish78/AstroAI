#!/usr/bin/env python3
"""
Test OpenAI API key functionality
"""

import os
from chatbot import WebChatbot

def test_api_key():
    """Test OpenAI API key setup and functionality"""
    print("🔑 OpenAI API Key Tester")
    print("=" * 40)
    
    # Method 1: Check environment variable
    env_key = os.getenv('OPENAI_API_KEY')
    print(f"Environment variable: {'✅ Found' if env_key else '❌ Not found'}")
    
    if env_key:
        print(f"Key format: {'✅ Valid' if env_key.startswith('sk-') else '❌ Invalid (should start with sk-)'}")
        print(f"Key length: {len(env_key)} characters")
        
        if env_key.startswith('your_') or env_key == 'your_openai_api_key_here':
            print("❌ This is a placeholder key, not a real one!")
            return False
    
    # Method 2: Test manual input
    if not env_key or not env_key.startswith('sk-'):
        print("\n💡 Enter your API key manually:")
        manual_key = input("OpenAI API Key (starts with sk-): ").strip()
        
        if not manual_key:
            print("❌ No key provided")
            return False
        
        if not manual_key.startswith('sk-'):
            print("❌ Invalid key format (should start with sk-)")
            return False
        
        test_key = manual_key
    else:
        test_key = env_key
    
    # Method 3: Test the key with chatbot
    print(f"\n🧪 Testing API key...")
    
    try:
        chatbot = WebChatbot(api_key=test_key)
        print("✅ API key is valid!")
        
        # Test with sample content
        sample_data = [{
            'url': 'https://example.com',
            'title': 'Test Page',
            'content': 'This is a test page about Python programming and web development.',
            'status': 'success'
        }]
        
        chatbot.add_scraped_content(sample_data)
        
        print("\n🤖 Testing AI response...")
        answer = chatbot.ask_question("What is this page about?")
        
        if answer.startswith('❌'):
            print(f"❌ API Error: {answer}")
            return False
        else:
            print(f"✅ AI Response: {answer}")
            return True
            
    except ValueError as e:
        print(f"❌ Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def show_setup_instructions():
    """Show setup instructions"""
    print("\n" + "=" * 40)
    print("📋 Setup Instructions")
    print("=" * 40)
    
    print("\n1️⃣ Get OpenAI API Key:")
    print("   • Visit: https://platform.openai.com/account/api-keys")
    print("   • Click 'Create new secret key'")
    print("   • Copy the key (starts with 'sk-')")
    
    print("\n2️⃣ Set Environment Variable:")
    print("   Windows: set OPENAI_API_KEY=sk-your-key-here")
    print("   Or create .env file with: OPENAI_API_KEY=sk-your-key-here")
    
    print("\n3️⃣ Run the app:")
    print("   python -m streamlit run app.py")

def main():
    """Main function"""
    success = test_api_key()
    
    if success:
        print("\n🎉 All tests passed! Your setup is ready.")
        print("💡 Run: python -m streamlit run app.py")
    else:
        show_setup_instructions()

if __name__ == "__main__":
    main()