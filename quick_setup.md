# 🚀 Quick API Key Setup Guide

## Step 1: Get Your OpenAI API Key

1. **Visit OpenAI Platform:**
   - Go to: https://platform.openai.com/account/api-keys
   - Sign in to your OpenAI account (create one if needed)

2. **Create API Key:**
   - Click "Create new secret key"
   - Give it a name (like "Web Scraper Bot")
   - Copy the key (it starts with `sk-` and is about 51 characters long)
   - **Important:** Save it somewhere safe - you won't see it again!

## Step 2: Set the API Key (Choose ONE method)

### Method A: Environment Variable (Recommended)
Open Command Prompt and run:
```bash
set OPENAI_API_KEY=sk-your-actual-key-here
```

### Method B: Create .env File
Create a file named `.env` in your project folder with:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

### Method C: Enter in App
You can also enter it directly in the Streamlit app sidebar when it runs.

## Step 3: Test Your Setup

Run this to test if your key works:
```bash
python test_api_key.py
```

## Step 4: Start the App

```bash
python -m streamlit run app.py
```

## 🔍 Troubleshooting

**"Invalid API key"** → Make sure it starts with `sk-` and is copied correctly
**"Rate limit"** → You've used up your free credits, check OpenAI billing
**"Not found"** → Set the environment variable or create .env file

## 💡 Example

If your API key is `sk-abc123def456ghi789`, then run:
```bash
set OPENAI_API_KEY=sk-abc123def456ghi789
python -m streamlit run app.py
```

That's it! 🎉