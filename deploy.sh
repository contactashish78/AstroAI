#!/bin/bash

echo "🚀 Web Intelligence Assistant - Deployment Script"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if git is initialized
if [ ! -d ".git" ]; then
    print_status "Initializing Git repository..."
    git init
    git branch -M main
fi

# Run tests first
print_status "Running comprehensive tests..."
python3 test_comprehensive.py

if [ $? -eq 0 ]; then
    print_success "All tests passed!"
else
    print_error "Tests failed. Please fix issues before deploying."
    exit 1
fi

# Check if API key is set
if [ -f ".env" ]; then
    if grep -q "sk-" .env; then
        print_success "API key found in .env file"
    else
        print_warning "API key not found or invalid in .env file"
    fi
else
    print_warning "No .env file found. Make sure to set OPENAI_API_KEY in your deployment platform."
fi

# Add all files
print_status "Adding files to git..."
git add .

# Commit changes
commit_message="Deploy: $(date '+%Y-%m-%d %H:%M:%S')"
print_status "Committing changes: $commit_message"
git commit -m "$commit_message"

# Check if remote origin exists
if git remote get-url origin > /dev/null 2>&1; then
    print_status "Pushing to GitHub..."
    git push origin main
    
    if [ $? -eq 0 ]; then
        print_success "Successfully pushed to GitHub!"
    else
        print_error "Failed to push to GitHub. Check your remote repository."
        exit 1
    fi
else
    print_warning "No remote origin set. Please add your GitHub repository:"
    echo "git remote add origin https://github.com/YOUR_USERNAME/web-intelligence-assistant.git"
    echo "git push -u origin main"
fi

echo ""
echo "🎉 Deployment preparation complete!"
echo ""
echo "Next steps:"
echo "1. Go to https://share.streamlit.io"
echo "2. Sign in with GitHub"
echo "3. Click 'New app'"
echo "4. Select your repository"
echo "5. Set main file: app.py"
echo "6. Add your OpenAI API key in Secrets"
echo ""
echo "Your app will be available at:"
echo "https://YOUR_USERNAME-web-intelligence-assistant-app-main.streamlit.app"
echo ""
print_success "Ready for deployment! 🚀"