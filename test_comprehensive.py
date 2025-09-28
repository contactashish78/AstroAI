#!/usr/bin/env python3
"""
Comprehensive Test Suite for Web Intelligence Assistant
"""

import os
import sys
from scraper import WebScraper
from chatbot import WebChatbot
import time

class WebIntelligenceTestSuite:
    def __init__(self):
        self.test_websites = {
            'simple': [
                'http://info.cern.ch/hypertext/WWW/TheProject.html',
                'https://example.com'
            ],
            'medium': [
                'https://www.python.org/about/',
                'https://docs.python.org/3/'
            ],
            'complex': [
                'https://en.wikipedia.org/wiki/Web_scraping',
                'https://github.com/python/cpython'
            ]
        }
        
        self.test_results = {
            'scraper_tests': [],
            'chatbot_tests': [],
            'integration_tests': []
        }
    
    def run_all_tests(self):
        """Run the complete test suite"""
        print("🚀 Web Intelligence Assistant - Comprehensive Test Suite")
        print("=" * 60)
        
        # Test environment
        self.test_environment()
        
        # Test scraper with different depths
        self.test_scraper_depths()
        
        # Test chatbot functionality
        self.test_chatbot_features()
        
        # Test integration
        self.test_integration()
        
        # Generate report
        self.generate_report()
    
    def test_environment(self):
        """Test environment setup"""
        print("\n🔧 Testing Environment Setup...")
        
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
        if api_key and api_key.startswith('sk-'):
            print(f"✅ OpenAI API Key - Found (length: {len(api_key)})")
        else:
            print("⚠️  OpenAI API Key - Not found or invalid")
    
    def test_scraper_depths(self):
        """Test scraper with different depth levels"""
        print("\n🕷️ Testing Scraper Depth Functionality...")
        
        test_url = 'http://info.cern.ch/hypertext/WWW/TheProject.html'
        
        for depth in [1, 2, 3, 4]:
            print(f"\n--- Testing Depth {depth} ---")
            try:
                scraper = WebScraper(delay=0.5, max_pages=10)
                results = scraper.scrape_with_depth([test_url], depth=depth)
                
                success_count = sum(1 for r in results if r['status'] == 'success')
                max_depth_found = max([r.get('depth', 0) for r in results])
                
                print(f"✅ Depth {depth}: {success_count} successful pages, max depth reached: {max_depth_found}")
                
                self.test_results['scraper_tests'].append({
                    'depth': depth,
                    'success_count': success_count,
                    'max_depth_reached': max_depth_found,
                    'status': 'passed'
                })
                
            except Exception as e:
                print(f"❌ Depth {depth} failed: {e}")
                self.test_results['scraper_tests'].append({
                    'depth': depth,
                    'status': 'failed',
                    'error': str(e)
                })
    
    def test_chatbot_features(self):
        """Test chatbot functionality"""
        print("\n🤖 Testing Chatbot Features...")
        
        # Check if API key is available
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or not api_key.startswith('sk-'):
            print("⚠️  Skipping chatbot tests - no valid API key")
            return
        
        try:
            chatbot = WebChatbot()
            
            # Test 1: Conversation flow test
            print("Testing conversation flow...")
            flow_test = chatbot.test_conversation_flow()
            if flow_test:
                print("✅ Conversation flow test - PASSED")
                self.test_results['chatbot_tests'].append({
                    'test': 'conversation_flow',
                    'status': 'passed'
                })
            else:
                print("❌ Conversation flow test - FAILED")
                self.test_results['chatbot_tests'].append({
                    'test': 'conversation_flow',
                    'status': 'failed'
                })
            
            # Test 2: Multiple questions without loops
            print("Testing multiple questions...")
            test_content = [{
                'url': 'https://test.com',
                'title': 'Test Page About Python',
                'content': 'Python is a programming language created by Guido van Rossum in 1991. It is used for web development, data science, and artificial intelligence.',
                'status': 'success'
            }]
            
            chatbot.add_scraped_content(test_content)
            chatbot.clear_history()
            
            questions = [
                "What programming language is mentioned?",
                "Who created this language?",
                "What year was it created?",
                "What is it used for?"
            ]
            
            answers = []
            for q in questions:
                answer = chatbot.ask_question(q)
                answers.append(answer)
                time.sleep(0.5)  # Small delay
            
            # Check for loops (answers shouldn't repeat questions)
            loop_detected = any(q.lower() in a.lower() for q, a in zip(questions, answers))
            
            if not loop_detected and len(set(answers)) == len(answers):
                print("✅ Multiple questions test - PASSED")
                self.test_results['chatbot_tests'].append({
                    'test': 'multiple_questions',
                    'status': 'passed'
                })
            else:
                print("❌ Multiple questions test - FAILED (loop detected)")
                self.test_results['chatbot_tests'].append({
                    'test': 'multiple_questions',
                    'status': 'failed',
                    'reason': 'loop_detected'
                })
                
        except Exception as e:
            print(f"❌ Chatbot tests failed: {e}")
            self.test_results['chatbot_tests'].append({
                'test': 'general',
                'status': 'failed',
                'error': str(e)
            })
    
    def test_integration(self):
        """Test full integration workflow"""
        print("\n🔗 Testing Integration Workflow...")
        
        try:
            # Step 1: Scrape with depth
            scraper = WebScraper(delay=0.5, max_pages=5)
            scraped_data = scraper.scrape_with_depth(['http://info.cern.ch/hypertext/WWW/TheProject.html'], depth=2)
            
            success_count = sum(1 for item in scraped_data if item['status'] == 'success')
            print(f"✅ Scraping: {success_count} pages scraped successfully")
            
            # Step 2: Initialize chatbot with scraped data
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key and api_key.startswith('sk-'):
                chatbot = WebChatbot()
                chatbot.add_scraped_content(scraped_data)
                
                # Step 3: Ask questions about scraped content
                test_questions = [
                    "What websites were analyzed?",
                    "What is the main topic?",
                    "Who created the World Wide Web?"
                ]
                
                for i, question in enumerate(test_questions, 1):
                    answer = chatbot.ask_question(question)
                    if not answer.startswith("❌"):
                        print(f"✅ Q{i}: Got valid response")
                    else:
                        print(f"❌ Q{i}: Error response")
                
                self.test_results['integration_tests'].append({
                    'test': 'full_workflow',
                    'status': 'passed',
                    'pages_scraped': success_count
                })
            else:
                print("⚠️  Skipping chatbot integration - no valid API key")
                self.test_results['integration_tests'].append({
                    'test': 'full_workflow',
                    'status': 'skipped',
                    'reason': 'no_api_key'
                })
                
        except Exception as e:
            print(f"❌ Integration test failed: {e}")
            self.test_results['integration_tests'].append({
                'test': 'full_workflow',
                'status': 'failed',
                'error': str(e)
            })
    
    def test_custom_website(self, url: str, depth: int = 3):
        """Test with a custom website provided by user"""
        print(f"\n🌐 Testing Custom Website: {url}")
        print(f"Depth: {depth}")
        
        try:
            scraper = WebScraper(delay=1.0, max_pages=15)
            results = scraper.scrape_with_depth([url], depth=depth)
            
            print(f"\n📊 Results for {url}:")
            print(f"Total pages processed: {len(results)}")
            
            success_count = 0
            for i, result in enumerate(results, 1):
                status_icon = "✅" if result['status'] == 'success' else "❌"
                depth_info = f"Level {result.get('depth', 0)}"
                print(f"{i}. {status_icon} {depth_info}: {result['title'][:50]}...")
                
                if result['status'] == 'success':
                    success_count += 1
                    if 'links' in result and result['links']:
                        print(f"   Found {len(result['links'])} links")
            
            stats = scraper.get_scraping_stats()
            print(f"\n📈 Statistics:")
            print(f"Success rate: {success_count}/{len(results)} ({success_count/len(results)*100:.1f}%)")
            print(f"Max depth configured: {stats['max_depth_configured']}")
            print(f"Total URLs discovered: {stats['total_urls_visited']}")
            
            return results
            
        except Exception as e:
            print(f"❌ Custom website test failed: {e}")
            return []
    
    def generate_report(self):
        """Generate test report"""
        print("\n" + "=" * 60)
        print("📋 TEST REPORT")
        print("=" * 60)
        
        # Scraper tests
        scraper_passed = sum(1 for t in self.test_results['scraper_tests'] if t['status'] == 'passed')
        scraper_total = len(self.test_results['scraper_tests'])
        print(f"🕷️  Scraper Tests: {scraper_passed}/{scraper_total} passed")
        
        # Chatbot tests
        chatbot_passed = sum(1 for t in self.test_results['chatbot_tests'] if t['status'] == 'passed')
        chatbot_total = len(self.test_results['chatbot_tests'])
        print(f"🤖 Chatbot Tests: {chatbot_passed}/{chatbot_total} passed")
        
        # Integration tests
        integration_passed = sum(1 for t in self.test_results['integration_tests'] if t['status'] == 'passed')
        integration_total = len(self.test_results['integration_tests'])
        print(f"🔗 Integration Tests: {integration_passed}/{integration_total} passed")
        
        total_passed = scraper_passed + chatbot_passed + integration_passed
        total_tests = scraper_total + chatbot_total + integration_total
        
        print(f"\n🎯 Overall: {total_passed}/{total_tests} tests passed ({total_passed/total_tests*100:.1f}%)")
        
        if total_passed == total_tests:
            print("🎉 All tests passed! System is ready for use.")
        else:
            print("⚠️  Some tests failed. Check the details above.")

def main():
    """Main function to run tests"""
    test_suite = WebIntelligenceTestSuite()
    
    if len(sys.argv) > 1:
        # Custom website testing
        url = sys.argv[1]
        depth = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        test_suite.test_custom_website(url, depth)
    else:
        # Run full test suite
        test_suite.run_all_tests()

if __name__ == "__main__":
    main()