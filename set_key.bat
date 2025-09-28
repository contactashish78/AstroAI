@echo off
echo 🔑 OpenAI API Key Setup
echo ========================
echo.
echo 📋 Instructions:
echo 1. Go to: https://platform.openai.com/account/api-keys
echo 2. Click "Create new secret key"
echo 3. Copy the key (starts with sk-)
echo 4. Paste it below
echo.
set /p api_key="Enter your OpenAI API key: "

if "%api_key%"=="" (
    echo ❌ No key entered!
    pause
    exit /b 1
)

echo.
echo Setting environment variable...
set OPENAI_API_KEY=%api_key%

echo ✅ API key set for this session!
echo.
echo 🧪 Testing the key...
python test_api_key.py

echo.
echo 🚀 Ready to run the app!
echo Run: python -m streamlit run app.py
pause