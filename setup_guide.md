# Web Scraper Chatbot - Setup Guide

## ✅ Test Results

The application has been successfully tested:

- ✅ **Web Scraper**: Working correctly, can scrape websites
- ✅ **Dependencies**: All Python packages installed
- ✅ **SSL Handling**: Fixed certificate issues
- ⚠️ **OpenAI API**: Needs valid API key for AI features

## 🚀 Quick Start

### 1. Get OpenAI API Key
1. Visit: https://platform.openai.com/account/api-keys
2. Create a new API key
3. Copy the key (starts with `sk-`)

### 2. Set API Key (Choose one method)

**Method A: Environment Variable**
```bash
set OPENAI_API_KEY=sk-your-actual-key-here
```

**Method B: Create .env file**
```
OPENAI_API_KEY=sk-your-actual-key-here
```

### 3. Run the Application
```bash
python -m streamlit run app.py
```

## 🧪 Test Commands

Run these to verify everything works:

```bash
# Test scraper functionality
python test_simple.py

# Demo complete workflow
python demo.py

# Run full app
python -m streamlit run app.py
```

## 📱 Using the App

1. **Open browser**: App runs at http://localhost:8501
2. **Enter API key**: In sidebar (if not set in environment)
3. **Add URLs**: Enter websites to scrape (one per line)
4. **Scrape**: Click "Scrape Websites" button
5. **Chat**: Ask questions about the scraped content

## 🌐 Example URLs to Test

```
http://info.cern.ch/hypertext/WWW/TheProject.html
https://www.python.org/about/
https://en.wikipedia.org/wiki/Web_scraping
```

## 🔧 Troubleshooting

**SSL Certificate Errors**: Fixed in current version
**API Key Issues**: Make sure key starts with `sk-` and is valid
**Import Errors**: Run `pip install -r requirements.txt`
**Streamlit Not Found**: Use `python -m streamlit run app.py`

## 🎯 Features

- Web scraping with BeautifulSoup
- AI-powered Q&A with OpenAI GPT
- Clean Streamlit interface
- Conversation history
- Content preview
- Respectful scraping delays