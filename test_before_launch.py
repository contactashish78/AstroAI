#!/usr/bin/env python3
"""
Pre-launch test script for Web Intelligence Assistant
Run this before launching the app to verify everything works correctly
"""

import os
import sys
from dotenv import load_dotenv
from scraper import WebScraper
from chatbot import WebChatbot

def test_environment():
    """Test environment setup and dependencies"""
    print("🔧 Testing Environment Setup...")
    
    # Check Python modules
    required_modules = ['streamlit', 'requests', 'bs4', 'openai', 'dotenv']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"  ✅ {module} - OK")
        except ImportError:
            print(f"  ❌ {module} - Missing")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n❌ Missing modules: {', '.join(missing_modules)}")
        print("Run: pip3 install -r requirements.txt")
        return False
    
    return True

def test_api_key():
    """Test OpenAI API key configuration"""
    print("\n🔑 Testing OpenAI API Key...")
    
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY', '')
    
    if not api_key:
        print("  ❌ No API key found in environment")
        return False
    
    if api_key.startswith('your_') or api_key == 'open_ai_key':
        print("  ❌ Placeholder API key detected")
        return False
    
    if not api_key.startswith('sk-'):
        print("  ❌ Invalid API key format (should start with 'sk-')")
        return False
    
    print(f"  ✅ API key format valid (length: {len(api_key)})")
    
    # Test API key with actual request
    try:
        chatbot = WebChatbot()
        print("  ✅ API key authentication successful")
        return True
    except Exception as e:
        print(f"  ❌ API key authentication failed: {e}")
        return False

def test_scraper():
    """Test web scraper functionality"""
    print("\n🕷️ Testing Web Scraper...")
    
    try:
        scraper = WebScraper(delay=0.5, max_pages=3)
        
        # Test single URL scraping
        print("  Testing single URL scraping...")
        result = scraper.scrape_url('http://info.cern.ch/hypertext/WWW/TheProject.html')
        
        if result['status'] == 'success':
            print(f"  ✅ Single URL scraping successful: {result['title']}")
        else:
            print(f"  ❌ Single URL scraping failed: {result['status']}")
            return False
        
        # Test multi-level scraping
        print("  Testing multi-level scraping...")
        results = scraper.scrape_with_depth(['http://info.cern.ch/hypertext/WWW/TheProject.html'], depth=2)
        
        if len(results) > 1:
            print(f"  ✅ Multi-level scraping successful: {len(results)} pages scraped")
            
            # Show depth distribution
            depth_counts = {}
            for r in results:
                depth = r.get('depth', 0)
                depth_counts[depth] = depth_counts.get(depth, 0) + 1
            
            for depth, count in sorted(depth_counts.items()):
                print(f"    Level {depth}: {count} pages")
        else:
            print("  ⚠️ Multi-level scraping only found 1 page")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Scraper test failed: {e}")
        return False

def test_chatbot_conversation():
    """Test chatbot conversation flow and loop prevention"""
    print("\n🤖 Testing Chatbot Conversation Flow...")
    
    try:
        # Create test data
        test_data = [{
            'url': 'https://test.com',
            'title': 'Test Page About Python Programming',
            'content': 'Python is a high-level programming language created by Guido van Rossum. It was first released in 1991. Python is known for its simple syntax and readability. It is widely used for web development, data science, artificial intelligence, and automation.',
            'status': 'success'
        }]
        
        chatbot = WebChatbot()
        chatbot.add_scraped_content(test_data)
        
        # Test conversation flow
        print("  Testing conversation flow...")
        test_result = chatbot.test_conversation_flow()
        
        if test_result:
            print("  ✅ Conversation flow test passed - no loops detected")
        else:
            print("  ❌ Conversation flow test failed - potential loops detected")
            return False
        
        # Test specific questions
        print("  Testing specific questions...")
        questions = [
            "What programming language is mentioned?",
            "Who created Python?",
            "When was Python first released?"
        ]
        
        for i, question in enumerate(questions, 1):
            print(f"    Q{i}: {question}")
            answer = chatbot.ask_question(question)
            
            if answer.startswith("❌"):
                print(f"    A{i}: ERROR - {answer}")
                return False
            else:
                print(f"    A{i}: {answer[:60]}...")
        
        print(f"  ✅ All {len(questions)} questions answered successfully")
        print(f"  ✅ Conversation history length: {len(chatbot.conversation_history)}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Chatbot test failed: {e}")
        return False

def test_streamlit_compatibility():
    """Test Streamlit compatibility"""
    print("\n📱 Testing Streamlit Compatibility...")
    
    try:
        import streamlit as st
        print("  ✅ Streamlit import successful")
        
        # Check if app.py exists and is readable
        if os.path.exists('app.py'):
            print("  ✅ app.py file found")
            
            # Basic syntax check
            with open('app.py', 'r') as f:
                content = f.read()
                if 'st.set_page_config' in content:
                    print("  ✅ Streamlit configuration found")
                else:
                    print("  ⚠️ No Streamlit configuration found")
        else:
            print("  ❌ app.py file not found")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Streamlit compatibility test failed: {e}")
        return False

def run_all_tests():
    """Run all tests and provide summary"""
    print("🚀 Web Intelligence Assistant - Pre-Launch Test Suite")
    print("=" * 60)
    
    tests = [
        ("Environment Setup", test_environment),
        ("OpenAI API Key", test_api_key),
        ("Web Scraper", test_scraper),
        ("Chatbot Conversation", test_chatbot_conversation),
        ("Streamlit Compatibility", test_streamlit_compatibility)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    passed = 0
    total = len(tests)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Ready to launch the app.")
        print("Run: python3 -m streamlit run app.py")
        return True
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Please fix issues before launching.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)