import streamlit as st
from scraper import WebScraper
from chatbot import WebChatbot
import os

# Page config
st.set_page_config(
    page_title="Web Scraper Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = None
if 'scraped_data' not in st.session_state:
    st.session_state.scraped_data = []
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'api_key_valid' not in st.session_state:
    st.session_state.api_key_valid = False

st.title("🤖 Web Scraper Chatbot")
st.markdown("Scrape websites and ask questions about their content using AI!")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    
    # OpenAI API Key input
    api_key = st.text_input("OpenAI API Key", type="password", 
                           value=os.getenv('OPENAI_API_KEY', ''),
                           help="Get your API key from https://platform.openai.com/account/api-keys")
    
    # Validate API key
    if api_key:
        if api_key.startswith('your_') or api_key == 'your_openai_api_key_here':
            st.error("❌ Please replace the placeholder with your actual OpenAI API key")
            st.session_state.api_key_valid = False
        elif not api_key.startswith('sk-'):
            st.error("❌ OpenAI API keys should start with 'sk-'")
            st.session_state.api_key_valid = False
        else:
            # Try to initialize chatbot to test the key
            try:
                if st.session_state.chatbot is None or not st.session_state.api_key_valid:
                    st.session_state.chatbot = WebChatbot(api_key=api_key)
                    st.session_state.api_key_valid = True
                    st.success("✅ API key validated successfully!")
            except ValueError as e:
                st.error(f"❌ {str(e)}")
                st.session_state.api_key_valid = False
                st.session_state.chatbot = None
    else:
        st.warning("⚠️ Enter your OpenAI API key to enable AI chat features")
        st.session_state.api_key_valid = False
    
    st.header("Website Scraping")
    
    # URL input
    urls_input = st.text_area(
        "Enter URLs (one per line):",
        placeholder="https://example.com\nhttps://another-site.com"
    )
    
    scrape_delay = st.slider("Delay between requests (seconds)", 0.5, 5.0, 1.0)
    
    if st.button("🔍 Scrape Websites"):
        if not urls_input.strip():
            st.error("Please enter at least one URL!")
        else:
            urls = [url.strip() for url in urls_input.split('\n') if url.strip()]
            
            with st.spinner("Scraping websites..."):
                scraper = WebScraper(delay=scrape_delay)
                scraped_data = scraper.scrape_multiple_urls(urls)
                
                st.session_state.scraped_data = scraped_data
                
                # Add content to chatbot if available
                if st.session_state.chatbot and st.session_state.api_key_valid:
                    st.session_state.chatbot.add_scraped_content(scraped_data)
                
                # Show scraping results
                success_count = sum(1 for item in scraped_data if item['status'] == 'success')
                st.success(f"Successfully scraped {success_count}/{len(scraped_data)} websites!")
                
                if not st.session_state.api_key_valid:
                    st.info("💡 Add your OpenAI API key to enable AI chat about this content!")
    
    # Clear data button
    if st.button("🗑️ Clear All Data"):
        st.session_state.scraped_data = []
        st.session_state.chat_history = []
        st.session_state.chatbot.clear_history()
        st.success("All data cleared!")

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📄 Scraped Content")
    
    if st.session_state.scraped_data:
        for i, item in enumerate(st.session_state.scraped_data):
            with st.expander(f"📝 {item['title'][:50]}..." if len(item['title']) > 50 else f"📝 {item['title']}"):
                st.write(f"**URL:** {item['url']}")
                st.write(f"**Status:** {item['status']}")
                if item['status'] == 'success':
                    st.write(f"**Content Preview:** {item['content'][:300]}...")
                else:
                    st.error(f"Failed to scrape: {item['status']}")
    else:
        st.info("No content scraped yet. Enter URLs in the sidebar and click 'Scrape Websites'.")

with col2:
    st.header("💬 Chat with AI")
    
    # Chat history display
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.write(f"**You:** {message['content']}")
            else:
                st.write(f"**AI:** {message['content']}")
    
    # Question input
    question = st.text_input("Ask a question about the scraped content:", 
                           placeholder="What is the main topic of these websites?")
    
    if st.button("💭 Ask Question") or question:
        if not st.session_state.api_key_valid:
            st.error("❌ Please enter a valid OpenAI API key first!")
        elif not st.session_state.scraped_data:
            st.error("❌ Please scrape some websites first!")
        elif not question.strip():
            st.error("❌ Please enter a question!")
        else:
            with st.spinner("🤔 Thinking..."):
                answer = st.session_state.chatbot.ask_question(question)
                
                # Add to chat history
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': question
                })
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': answer
                })
                
                st.rerun()

# Footer
st.markdown("---")
st.markdown("Built with Streamlit, OpenAI, and BeautifulSoup 🚀")