#!/usr/bin/env python3
"""
Test script for the Web Scraper Chatbot
"""

import os
from scraper import WebScraper
from chatbot import WebChatbot

def test_scraper():
    """Test the web scraper functionality"""
    print("🔍 Testing Web Scraper...")
    
    scraper = WebScraper(delay=0.5)
    
    # Test with a simple, reliable website
    test_urls = [
        "https://httpbin.org/html",  # Simple HTML test page
        "https://example.com"        # Basic example site
    ]
    
    try:
        results = scraper.scrape_multiple_urls(test_urls)
        
        print(f"✅ Scraped {len(results)} URLs")
        
        for i, result in enumerate(results, 1):
            print(f"\n--- Result {i} ---")
            print(f"URL: {result['url']}")
            print(f"Status: {result['status']}")
            print(f"Title: {result['title'][:50]}...")
            if result['status'] == 'success':
                print(f"Content preview: {result['content'][:100]}...")
            else:
                print(f"Error: {result['status']}")
        
        return results
        
    except Exception as e:
        print(f"❌ Scraper test failed: {e}")
        return []

def test_chatbot(scraped_data):
    """Test the chatbot functionality"""
    print("\n🤖 Testing Chatbot...")
    
    # Check if OpenAI API key is available
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("⚠️  No OpenAI API key found. Set OPENAI_API_KEY environment variable to test chatbot.")
        print("   You can still test the scraper functionality.")
        return
    
    try:
        chatbot = WebChatbot()
        chatbot.add_scraped_content(scraped_data)
        
        # Test questions
        test_questions = [
            "What websites were scraped?",
            "Summarize the main content from these pages"
        ]
        
        for question in test_questions:
            print(f"\n❓ Question: {question}")
            answer = chatbot.ask_question(question)
            print(f"🤖 Answer: {answer}")
            
        print("✅ Chatbot test completed")
        
    except Exception as e:
        print(f"❌ Chatbot test failed: {e}")

def test_environment():
    """Test environment setup"""
    print("🔧 Testing Environment...")
    
    # Check Python modules
    required_modules = ['requests', 'bs4', 'openai', 'streamlit']
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module} - OK")
        except ImportError:
            print(f"❌ {module} - Missing")
    
    # Check API key
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        print(f"✅ OpenAI API Key - Found (length: {len(api_key)})")
    else:
        print("⚠️  OpenAI API Key - Not found")
    
    print()

def main():
    """Run all tests"""
    print("🚀 Web Scraper Chatbot - Test Suite")
    print("=" * 50)
    
    # Test environment
    test_environment()
    
    # Test scraper
    scraped_data = test_scraper()
    
    # Test chatbot if we have scraped data
    if scraped_data:
        test_chatbot(scraped_data)
    
    print("\n" + "=" * 50)
    print("🎉 Test suite completed!")
    
    if scraped_data:
        success_count = sum(1 for item in scraped_data if item['status'] == 'success')
        print(f"📊 Scraping: {success_count}/{len(scraped_data)} URLs successful")
    
    print("\n💡 To run the full app:")
    print("   python -m streamlit run app.py")

if __name__ == "__main__":
    main()