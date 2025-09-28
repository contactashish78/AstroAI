# Web Scraper Chatbot

A Python application that scrapes websites and uses OpenAI's GPT to answer questions about the scraped content.

## Features

- 🔍 Web scraping with BeautifulSoup
- 🤖 AI-powered question answering with OpenAI
- 💬 Interactive chat interface with Streamlit
- 📄 Content preview and management
- ⚙️ Configurable scraping delays
- 🗂️ Session-based conversation history

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key to the `.env` file:
     ```
     OPENAI_API_KEY=your_actual_api_key_here
     ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## Usage

1. **Enter your OpenAI API key** in the sidebar (or set it in the `.env` file)

2. **Add URLs to scrape** in the sidebar text area (one per line)

3. **Click "Scrape Websites"** to extract content from the URLs

4. **Ask questions** about the scraped content in the chat interface

5. **View scraped content** in the left panel to see what data is available

## Components

- `scraper.py` - Web scraping functionality using requests and BeautifulSoup
- `chatbot.py` - OpenAI integration for question answering
- `app.py` - Streamlit web interface
- `requirements.txt` - Python dependencies

## Configuration

- **Scraping delay**: Adjust the delay between requests to be respectful to websites
- **Content limit**: Each scraped page is limited to 10,000 characters
- **Chat history**: Keeps the last 6 messages for context

## Notes

- The scraper includes a respectful delay between requests
- Content is cleaned and limited to prevent token overflow
- The chatbot only answers based on scraped content
- Session data is cleared when you refresh the page

## Requirements

- Python 3.7+
- OpenAI API key
- Internet connection for scraping and API calls