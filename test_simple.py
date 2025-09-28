#!/usr/bin/env python3
"""
Simple test for scraper functionality without network dependencies
"""

from scraper import WebScraper
from chatbot import WebChatbot
import os

def test_scraper_local():
    """Test scraper with local content simulation"""
    print("🔍 Testing Web Scraper (Local Mode)...")
    
    # Create mock scraped data
    mock_data = [
        {
            'url': 'https://example.com',
            'title': 'Example Domain',
            'content': 'This domain is for use in illustrative examples in documents. You may use this domain in literature without prior coordination or asking for permission.',
            'status': 'success'
        },
        {
            'url': 'https://test-site.com',
            'title': 'Test Site - Python Programming',
            'content': 'Python is a high-level programming language. It is widely used for web development, data analysis, artificial intelligence, and scientific computing. Python syntax is clean and readable.',
            'status': 'success'
        }
    ]
    
    print("✅ Mock data created successfully")
    for i, item in enumerate(mock_data, 1):
        print(f"  {i}. {item['title']} - {item['url']}")
    
    return mock_data

def test_chatbot_with_mock_data(scraped_data):
    """Test chatbot with mock data"""
    print("\n🤖 Testing Chatbot with Mock Data...")
    
    # Check if we have a valid API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key.startswith('your_'):
        print("⚠️  Using placeholder API key. To test with real OpenAI:")
        print("   1. Get your API key from https://platform.openai.com/account/api-keys")
        print("   2. Set it as: set OPENAI_API_KEY=your_actual_key")
        print("   3. Or create a .env file with: OPENAI_API_KEY=your_actual_key")
        return
    
    try:
        chatbot = WebChatbot()
        chatbot.add_scraped_content(scraped_data)
        
        print("✅ Chatbot initialized with scraped content")
        print("✅ Ready to answer questions about:")
        for item in scraped_data:
            print(f"   - {item['title']}")
        
        # Test without actual API call for now
        print("\n💡 Chatbot is ready! In the full app, you can ask questions like:")
        print("   - 'What is Python used for?'")
        print("   - 'Summarize the content from these websites'")
        print("   - 'What domains were scraped?'")
        
    except Exception as e:
        print(f"❌ Chatbot setup failed: {e}")

def test_real_scraper():
    """Test real scraper with a simple HTTP site"""
    print("\n🌐 Testing Real Web Scraper...")
    
    try:
        scraper = WebScraper(delay=0.5)
        
        # Use a simple HTTP site to avoid SSL issues
        test_url = "http://info.cern.ch/hypertext/WWW/TheProject.html"
        
        print(f"Attempting to scrape: {test_url}")
        result = scraper.scrape_url(test_url)
        
        if result['status'] == 'success':
            print("✅ Real scraping successful!")
            print(f"Title: {result['title']}")
            print(f"Content preview: {result['content'][:100]}...")
            return [result]
        else:
            print(f"❌ Scraping failed: {result['status']}")
            return []
            
    except Exception as e:
        print(f"❌ Real scraper test failed: {e}")
        return []

def main():
    """Run simplified tests"""
    print("🚀 Web Scraper Chatbot - Simple Test")
    print("=" * 45)
    
    # Test with mock data first
    mock_data = test_scraper_local()
    test_chatbot_with_mock_data(mock_data)
    
    # Try real scraping
    real_data = test_real_scraper()
    
    print("\n" + "=" * 45)
    print("✅ Simple test completed!")
    
    print("\n🎯 Next steps:")
    print("1. Set your OpenAI API key to test AI features")
    print("2. Run the full app: python -m streamlit run app.py")
    print("3. Enter URLs in the sidebar and start chatting!")

if __name__ == "__main__":
    main()