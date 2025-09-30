import streamlit as st
from scraper import WebScraper
from chatbot import WebChatbot
import os
from PyPDF2 import PdfReader

# Page config
st.set_page_config(
    page_title="Web Intelligence Assistant",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for high-contrast professional theme
st.markdown("""
<style>
    /* Main theme - Clean dark background */
    .stApp {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    
    /* Chat message styling - High contrast */
    .user-message {
        background-color: #2d3748;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 5px solid #3182ce;
        color: #ffffff;
        font-size: 16px;
        line-height: 1.6;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        border: 1px solid #4a5568;
    }
    
    .user-message strong {
        color: #63b3ed;
        font-weight: 700;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .assistant-message {
        background-color: #2a4365;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 5px solid #38a169;
        color: #ffffff;
    }
    
    .assistant-message strong {
        color: #68d391;
        font-weight: 700;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Sidebar styling - Better contrast */
    .css-1d391kg {
        background-color: #2d3748;
        border-right: 2px solid #4a5568;
    }
    
    /* Button styling - High contrast */
    .stButton > button {
        background-color: #3182ce;
        color: #ffffff;
        border-radius: 8px;
        border: 2px solid #2c5282;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #2c5282;
        border-color: #2a4365;
        transform: translateY(-1px);
    }
    
    /* Text input styling - High contrast boxes */
    .stTextInput > div > div > input {
        background-color: #2d3748 !important;
        border: 2px solid #4a5568 !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        padding: 0.75rem !important;
        font-size: 1rem !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3182ce !important;
        box-shadow: 0 0 0 3px rgba(49, 130, 206, 0.1) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #a0aec0 !important;
    }
    
    .stTextInput label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Text area styling - High contrast */
    .stTextArea > div > div > textarea {
        background-color: #2d3748 !important;
        border: 2px solid #4a5568 !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        padding: 0.75rem !important;
        font-size: 1rem !important;
        min-height: 120px !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #3182ce !important;
        box-shadow: 0 0 0 3px rgba(49, 130, 206, 0.1) !important;
    }
    
    .stTextArea > div > div > textarea::placeholder {
        color: #a0aec0 !important;
    }
    
    .stTextArea label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Selectbox styling - High contrast */
    .stSelectbox > div > div {
        background-color: #2d3748 !important;
        border: 2px solid #4a5568 !important;
        border-radius: 8px !important;
    }
    
    .stSelectbox > div > div > select {
        background-color: #2d3748 !important;
        color: #ffffff !important;
        border: none !important;
        padding: 0.75rem !important;
    }
    
    .stSelectbox label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Slider styling */
    .stSlider > div > div > div {
        color: #ffffff !important;
    }
    
    .stSlider label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Expander styling - High contrast */
    .streamlit-expanderHeader {
        background-color: #2d3748 !important;
        border: 2px solid #4a5568 !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        padding: 1rem !important;
    }
    
    .streamlit-expanderContent {
        background-color: #1a202c !important;
        border: 2px solid #4a5568 !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
        padding: 1rem !important;
    }
    
    /* Success/Error/Info message styling - High contrast */
    .stSuccess {
        background-color: #22543d !important;
        color: #c6f6d5 !important;
        border: 2px solid #38a169 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    
    .stError {
        background-color: #742a2a !important;
        color: #fed7d7 !important;
        border: 2px solid #e53e3e !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    
    .stInfo {
        background-color: #2a4365 !important;
        color: #bee3f8 !important;
        border: 2px solid #3182ce !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    
    .stWarning {
        background-color: #744210 !important;
        color: #faf089 !important;
        border: 2px solid #d69e2e !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    
    /* Header styling */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    
    /* Main header styling */
    .main-header {
        text-align: center;
        padding: 2.5rem 1rem;
        background: linear-gradient(135deg, #2b6cb0 0%, #553c9a 100%);
        border-radius: 12px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
    }
    
    .main-header h1 {
        color: white !important;
        margin-bottom: 0.5rem;
        font-size: 2.5rem;
    }
    
    .main-header p {
        color: #e2e8f0 !important;
        font-size: 1.2rem;
        margin: 0;
    }
    
    /* Content sections - High contrast boxes */
    .content-section {
        background-color: #2d3748;
        padding: 2rem;
        border-radius: 12px;
        margin: 1rem 0;
        border: 2px solid #4a5568;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    
    .ai-section {
        background-color: #2d3748;
        padding: 2rem;
        border-radius: 12px;
        margin: 1rem 0;
        border: 2px solid #4a5568;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    
    /* Custom cards for better organization */
    .success-card {
        background-color: #22543d;
        color: #c6f6d5;
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid #38a169;
        margin: 0.5rem 0;
        font-weight: 600;
    }
    
    .error-card {
        background-color: #742a2a;
        color: #fed7d7;
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid #e53e3e;
        margin: 0.5rem 0;
        font-weight: 600;
    }
    
    .info-card {
        background-color: #2a4365;
        color: #bee3f8;
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid #3182ce;
        margin: 0.5rem 0;
    }
    
    .warning-card {
        background-color: #744210;
        color: #faf089;
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid #d69e2e;
        margin: 0.5rem 0;
        font-weight: 600;
    }
    
    /* Fix all text visibility */
    .stMarkdown, .stText, p, div, span, label {
        color: #ffffff !important;
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = None
if 'scraped_data' not in st.session_state:
    st.session_state.scraped_data = []
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'api_key_valid' not in st.session_state:
    st.session_state.api_key_valid = False

# Custom CSS for professional styling
## Removed conflicting light-theme CSS to ensure dark theme readability

# Professional header
st.markdown("""
<div class="main-header">
    <h1>🔍 Web Intelligence Assistant</h1>
    <p>Extract insights from websites using advanced AI-powered analysis</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for configuration
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    st.markdown("---")
    
    # OpenAI API Key input
    st.markdown("#### 🔑 OpenAI API Configuration")
    # Try to get API key from Streamlit secrets first, then environment
    default_api_key = ""
    try:
        default_api_key = st.secrets["OPENAI_API_KEY"]
    except:
        default_api_key = os.getenv('OPENAI_API_KEY', '')
    
    api_key = st.text_input("API Key", type="password", 
                           value=default_api_key,
                           help="Get your API key from https://platform.openai.com/account/api-keys",
                           placeholder="sk-...")
    
    # Validate API key
    if api_key:
        if api_key.startswith('your_') or api_key == 'your_openai_api_key_here':
            st.markdown('<div class="error-card">❌ Please replace the placeholder with your actual OpenAI API key</div>', unsafe_allow_html=True)
            st.session_state.api_key_valid = False
        elif not api_key.startswith('sk-'):
            st.markdown('<div class="error-card">❌ OpenAI API keys should start with "sk-"</div>', unsafe_allow_html=True)
            st.session_state.api_key_valid = False
        else:
            # Try to initialize chatbot to test the key
            try:
                if st.session_state.chatbot is None or not st.session_state.api_key_valid:
                    st.session_state.chatbot = WebChatbot(api_key=api_key)
                    st.session_state.api_key_valid = True
                    st.markdown('<div class="success-card">✅ API key validated successfully!</div>', unsafe_allow_html=True)
            except ValueError as e:
                st.markdown(f'<div class="error-card">❌ {str(e)}</div>', unsafe_allow_html=True)
                st.session_state.api_key_valid = False
                st.session_state.chatbot = None
    else:
        st.markdown('<div class="warning-card">⚠️ Enter your OpenAI API key to enable AI chat features</div>', unsafe_allow_html=True)
        st.session_state.api_key_valid = False
    
    st.markdown("---")
    
    st.markdown("#### 🌐 Website Scraping")
    
    # URL input
    urls_input = st.text_area(
        "URLs to analyze:",
        placeholder ="https://www.astropatri.come",
        height=100,
        help="Enter one URL per line. The scraper will analyze these websites and extract their content."
    )

    # PDF upload
    st.markdown("#### 📄 PDF Documents")
    uploaded_pdfs = st.file_uploader(
        "Upload PDF files to analyze",
        type=["pdf"],
        accept_multiple_files=True,
        help="Uploaded PDFs will be parsed and included in the analysis and chat context."
    )

    def _parse_pdf_files(files):
        parsed_items = []
        for file in files:
            try:
                reader = PdfReader(file)
                text_chunks = []
                for page in reader.pages:
                    try:
                        text_chunks.append(page.extract_text() or "")
                    except Exception:
                        continue
                full_text = "\n".join(text_chunks)
                title = os.path.splitext(os.path.basename(file.name))[0]
                parsed_items.append({
                    'url': f"uploaded://{file.name}",
                    'title': title,
                    'content': full_text[:10000],
                    'status': 'success'
                })
            except Exception as e:
                parsed_items.append({
                    'url': f"uploaded://{getattr(file, 'name', 'unknown')}",
                    'title': 'PDF Parse Error',
                    'content': '',
                    'status': f'error: {str(e)}'
                })
        return parsed_items

    if uploaded_pdfs:
        if st.button("📥 Add Uploaded PDFs"):
            with st.spinner("Parsing uploaded PDFs..."):
                pdf_items = _parse_pdf_files(uploaded_pdfs)
                # Merge into scraped_data
                st.session_state.scraped_data = (st.session_state.scraped_data or []) + pdf_items
                # Add to chatbot if available
                if st.session_state.chatbot and st.session_state.api_key_valid:
                    st.session_state.chatbot.add_scraped_content(st.session_state.scraped_data)
                success_count = sum(1 for item in pdf_items if item['status'] == 'success')
                st.success(f"Added {success_count}/{len(pdf_items)} PDF(s) to analysis.")
    
    # Scraping options
    with st.expander("🔧 Advanced Settings", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            scrape_delay = st.slider("Request delay (seconds)", 0.5, 5.0, 1.0, 
                                   help="Time to wait between requests to be respectful to servers")
            scrape_depth = st.selectbox("Analysis depth", [1, 2, 3, 4, 5], index=3, 
                                       help="1 = Single page only, 2+ = Follow links to deeper levels")
        with col2:
            max_pages = st.slider("Maximum pages", 5, 50, 10, 
                                 help="Limit total pages to prevent excessive scraping")
            st.info("💡 Higher depth and page limits will take longer but provide more comprehensive analysis.")
    
    # Scraping buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 Scrape Websites (Single Level)"):
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
    
    with col2:
        if st.button("🕷️ Deep Scrape (Multi-Level)"):
            if not urls_input.strip():
                st.error("Please enter at least one URL!")
            else:
                urls = [url.strip() for url in urls_input.split('\n') if url.strip()]
                
                with st.spinner(f"Deep scraping websites (depth {scrape_depth})..."):
                    scraper = WebScraper(delay=scrape_delay, max_pages=max_pages)
                    scraped_data = scraper.scrape_with_depth(urls, depth=scrape_depth)
                    
                    st.session_state.scraped_data = scraped_data
                    
                    # Add content to chatbot if available
                    if st.session_state.chatbot and st.session_state.api_key_valid:
                        st.session_state.chatbot.add_scraped_content(scraped_data)
                    
                    # Show scraping results with stats
                    success_count = sum(1 for item in scraped_data if item['status'] == 'success')
                    stats = scraper.get_scraping_stats()
                    
                    st.success(f"Deep scraping completed!")
                    st.info(f"📊 **Stats:** {success_count} successful pages, "
                           f"Max depth: {stats['max_depth_configured']}, "
                           f"Total discovered: {stats['total_urls_visited']}")
                    
                    if not st.session_state.api_key_valid:
                        st.info("💡 Add your OpenAI API key to enable AI chat about this content!")
    
    # Clear data button
    if st.button("🗑️ Clear All Data"):
        st.session_state.scraped_data = []
        st.session_state.chat_history = []
        st.session_state.chatbot.clear_history()
        st.success("All data cleared!")

# Main content area
col1, col2 = st.columns([1.2, 1], gap="large")

with col1:
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown("### 📄 Content Analysis")
    
    # Show stats if data exists
    if st.session_state.scraped_data:
        total_pages = len(st.session_state.scraped_data)
        successful_pages = sum(1 for item in st.session_state.scraped_data if item['status'] == 'success')
        max_depth = max((item.get('depth', 0) for item in st.session_state.scraped_data), default=0)
        
        st.markdown(f"""
        <div class="stats-container">
            <div class="stat-item">
                <div class="stat-number">{total_pages}</div>
                <div class="stat-label">Total Pages</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{successful_pages}</div>
                <div class="stat-label">Successful</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{max_depth + 1}</div>
                <div class="stat-label">Max Levels</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    if st.session_state.scraped_data:
        for i, item in enumerate(st.session_state.scraped_data):
            # Create title with depth indicator
            depth_indicator = f" • Level {item.get('depth', 0)}" if 'depth' in item else ""
            title_display = item['title'][:60] + "..." if len(item['title']) > 60 else item['title']
            
            # Status icon
            status_icon = "✅" if item['status'] == 'success' else "❌"
            
            with st.expander(f"{status_icon} {title_display}{depth_indicator}", expanded=False):
                col_a, col_b = st.columns([2, 1])
                with col_a:
                    st.markdown(f"**🔗 URL:** `{item['url']}`")
                    if 'depth' in item:
                        st.markdown(f"**📊 Analysis Level:** {item['depth']}")
                with col_b:
                    if item['status'] == 'success':
                        st.markdown('<div class="success-card">✅ Successfully analyzed</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="error-card">❌ {item["status"]}</div>', unsafe_allow_html=True)
                
                if item['status'] == 'success':
                    st.markdown("**📝 Content Preview:**")
                    st.markdown(f'<div class="info-card">{item["content"][:400]}...</div>', unsafe_allow_html=True)
                    
                    if 'links' in item and item['links']:
                        st.markdown(f"**🔗 Discovered Links:** {len(item['links'])} additional pages found")
    else:
        st.markdown("""
        <div class="info-card">
            <h4>🚀 Ready to Analyze Websites</h4>
            <p>Enter URLs in the sidebar and choose your analysis method:</p>
            <ul>
                <li><strong>Single Level:</strong> Analyze only the specified pages</li>
                <li><strong>Deep Analysis:</strong> Follow links to discover related content</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="ai-section">', unsafe_allow_html=True)
    st.markdown("### 🤖 AI Assistant")
    
    # Chat history display
    chat_container = st.container()
    with chat_container:
        if st.session_state.chat_history:
            for message in st.session_state.chat_history:
                if message['role'] == 'user':
                    st.markdown(f"""
                    <div class="user-message">
                        <strong>👤 You:</strong>
                        <div class="chat-message-content">{message['content']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="assistant-message">
                        <strong>🤖 AI Assistant:</strong>
                        <div class="chat-message-content">{message['content']}</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="info-card">
                <h4>💡 Ask Questions About Your Content</h4>
                <p>Once you've analyzed some websites, you can ask questions like:</p>
                <ul>
                    <li>"What are the main topics covered?"</li>
                    <li>"Summarize the key findings"</li>
                    <li>"What insights can you extract?"</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    

    
    # Question input
    st.markdown("#### 💭 Ask a Question")
    question = st.text_input("Your Question", 
                           placeholder="What insights can you provide about the analyzed content?",
                           key="question_input",
                           label_visibility="collapsed")
    
    if st.button("💭 Ask Question"):
        if not st.session_state.api_key_valid:
            st.error("❌ Please enter a valid OpenAI API key first!")
        elif not st.session_state.scraped_data:
            st.error("❌ Please scrape some websites first!")
        elif not question.strip():
            st.error("❌ Please enter a question!")
        else:
            # Check if this exact question was just asked to prevent loops
            if (st.session_state.chat_history and 
                len(st.session_state.chat_history) > 0 and
                st.session_state.chat_history[-2]['content'] == question if len(st.session_state.chat_history) >= 2 else False):
                st.warning("⚠️ This question was just asked. Please try a different question to avoid loops.")
            else:
                with st.spinner("🤔 Thinking..."):
                    answer = st.session_state.chatbot.ask_question(question)
                    
                    # Add to chat history only if we got a valid response
                    if not answer.startswith("❌"):
                        st.session_state.chat_history.append({
                            'role': 'user',
                            'content': question
                        })
                        st.session_state.chat_history.append({
                            'role': 'assistant',
                            'content': answer
                        })
                    else:
                        # Show error but don't add to history
                        st.error(answer)
                
                # Rerun to update the display
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Professional footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #e2e8f0; background: #1f2937; border-radius: 10px; margin-top: 2rem; border: 1px solid #374151;">
    <h4 style="margin: 0; color: #63b3ed;">Web Intelligence Assistant</h4>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">
        Powered by OpenAI GPT • Built with Streamlit • Web Scraping with BeautifulSoup
    </p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem; opacity: 0.8;">
        Professional web content analysis and AI-powered insights
    </p>
</div>
""", unsafe_allow_html=True)