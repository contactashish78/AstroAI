import openai
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()

class WebChatbot:
    def __init__(self, api_key: str = None):
        # Get API key from parameter, environment, or .env file
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Please provide it via parameter or set OPENAI_API_KEY environment variable.")
        
        if self.api_key.startswith('your_') or self.api_key == 'your_openai_api_key_here':
            raise ValueError("Please replace the placeholder API key with your actual OpenAI API key.")
        
        try:
            self.client = openai.OpenAI(api_key=self.api_key)
            # Test the API key with a simple request
            self._test_api_key()
        except Exception as e:
            raise ValueError(f"Failed to initialize OpenAI client: {str(e)}")
        
        self.scraped_content = []
        self.conversation_history = []
    
    def _test_api_key(self):
        """Test if the API key is valid"""
        try:
            # Make a minimal request to test the key
            self.client.models.list()
        except openai.AuthenticationError:
            raise ValueError("Invalid OpenAI API key. Please check your key at https://platform.openai.com/account/api-keys")
        except Exception as e:
            # Other errors are okay for now, we just want to test authentication
            pass
    
    def add_scraped_content(self, content: List[Dict[str, str]]):
        """Add scraped content to the chatbot's knowledge base"""
        self.scraped_content = content
    
    def _prepare_context(self) -> str:
        """Prepare context from scraped content"""
        if not self.scraped_content:
            return "No website content available."
        
        context = "Based on the following website content:\n\n"
        for item in self.scraped_content:
            if item['status'] == 'success':
                context += f"Title: {item['title']}\n"
                context += f"URL: {item['url']}\n"
                context += f"Content: {item['content'][:2000]}...\n\n"
        
        return context
    
    def ask_question(self, question: str) -> str:
        """Ask a question about the scraped content"""
        try:
            context = self._prepare_context()
            
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant that answers questions based on website content provided to you. Use only the information from the websites to answer questions. If the information is not available in the provided content, say so clearly."
                },
                {
                    "role": "user",
                    "content": f"{context}\n\nQuestion: {question}"
                }
            ]
            
            # Add conversation history (avoid duplicating the current question)
            messages.extend(self.conversation_history[-6:])  # Keep last 6 messages
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            answer = response.choices[0].message.content
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": question})
            self.conversation_history.append({"role": "assistant", "content": answer})
            
            return answer
            
        except openai.AuthenticationError:
            return "❌ Authentication Error: Invalid OpenAI API key. Please check your key at https://platform.openai.com/account/api-keys"
        except openai.RateLimitError:
            return "❌ Rate Limit Error: You've exceeded your API quota. Please check your OpenAI billing."
        except openai.APIError as e:
            return f"❌ OpenAI API Error: {str(e)}"
        except Exception as e:
            return f"❌ Unexpected Error: {str(e)}"
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []