#!/usr/bin/env python3
"""
Demo script showing the complete workflow
"""

from scraper import WebScraper
from chatbot import WebChatbot
import os

def demo_workflow():
    """Demonstrate the complete scraper + chatbot workflow"""
    print("🚀 Web Scraper Chatbot - Demo Workflow")
    print("=" * 50)
    
    # Step 1: Initialize scraper
    print("1️⃣ Initializing web scraper...")
    scraper = WebScraper(delay=1.0)
    
    # Step 2: Scrape some websites
    print("2️⃣ Scraping websites...")
    urls = [
        "http://info.cern.ch/hypertext/WWW/TheProject.html",  # First website
        "https://www.python.org/about/"  # Python about page
    ]
    
    scraped_data = []
    for url in urls:
        print(f"   Scraping: {url}")
        result = scraper.scrape_url(url)
        scraped_data.append(result)
        
        if result['status'] == 'success':
            print(f"   ✅ Success: {result['title']}")
        else:
            print(f"   ❌ Failed: {result['status']}")
    
    # Step 3: Initialize chatbot
    print("\n3️⃣ Setting up AI chatbot...")
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key.startswith('your_'):
        print("   ⚠️  No valid OpenAI API key found")
        print("   📝 Showing scraped content instead:")
        
        for i, item in enumerate(scraped_data, 1):
            if item['status'] == 'success':
                print(f"\n   📄 Website {i}: {item['title']}")
                print(f"   🔗 URL: {item['url']}")
                print(f"   📝 Content: {item['content'][:200]}...")
        
        print("\n   💡 To enable AI chat:")
        print("      1. Get API key: https://platform.openai.com/account/api-keys")
        print("      2. Set environment variable: OPENAI_API_KEY=your_key")
        print("      3. Run this demo again")
        return
    
    # Initialize chatbot with scraped content
    chatbot = WebChatbot()
    chatbot.add_scraped_content(scraped_data)
    print("   ✅ Chatbot ready with scraped content")
    
    # Step 4: Demo questions
    print("\n4️⃣ Asking AI questions about scraped content...")
    
    demo_questions = [
        "What websites were scraped?",
        "What is the main topic of these pages?",
        "Tell me about the World Wide Web project"
    ]
    
    for i, question in enumerate(demo_questions, 1):
        print(f"\n   ❓ Question {i}: {question}")
        try:
            answer = chatbot.ask_question(question)
            print(f"   🤖 Answer: {answer}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Demo completed!")
    print("\n🎯 Ready to use the full Streamlit app:")
    print("   python -m streamlit run app.py")

if __name__ == "__main__":
    demo_workflow()