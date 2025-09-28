#!/usr/bin/env python3
"""
Simple deployment test to verify app can start
"""

import sys
import os

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import streamlit as st
        print("✅ streamlit")
    except ImportError as e:
        print(f"❌ streamlit: {e}")
        return False
    
    try:
        import requests
        print("✅ requests")
    except ImportError as e:
        print(f"❌ requests: {e}")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("✅ beautifulsoup4")
    except ImportError as e:
        print(f"❌ beautifulsoup4: {e}")
        return False
    
    try:
        import openai
        print("✅ openai")
    except ImportError as e:
        print(f"❌ openai: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv")
    except ImportError as e:
        print(f"❌ python-dotenv: {e}")
        return False
    
    return True

def test_app_modules():
    """Test that our app modules can be imported"""
    print("\nTesting app modules...")
    
    try:
        from scraper import WebScraper
        print("✅ scraper.py")
    except ImportError as e:
        print(f"❌ scraper.py: {e}")
        return False
    
    try:
        from chatbot import WebChatbot
        print("✅ chatbot.py")
    except ImportError as e:
        print(f"❌ chatbot.py: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic functionality without API calls"""
    print("\nTesting basic functionality...")
    
    try:
        from scraper import WebScraper
        scraper = WebScraper(delay=0.1, max_pages=1)
        print("✅ WebScraper initialization")
    except Exception as e:
        print(f"❌ WebScraper initialization: {e}")
        return False
    
    # Test without API key (should handle gracefully)
    try:
        from chatbot import WebChatbot
        # This should fail gracefully without API key
        print("✅ WebChatbot module loadable")
    except Exception as e:
        print(f"❌ WebChatbot module: {e}")
        return False
    
    return True

def main():
    print("🚀 Deployment Test Suite")
    print("=" * 30)
    
    tests = [
        ("Import Test", test_imports),
        ("App Modules Test", test_app_modules),
        ("Basic Functionality Test", test_basic_functionality)
    ]
    
    all_passed = True
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        if not test_func():
            all_passed = False
    
    print("\n" + "=" * 30)
    if all_passed:
        print("✅ All deployment tests passed!")
        print("App is ready for deployment.")
        return 0
    else:
        print("❌ Some tests failed.")
        print("Fix issues before deploying.")
        return 1

if __name__ == "__main__":
    sys.exit(main())