# Design Document

## Overview

The project cleanup and optimization will transform the current Web Scraper Chatbot from a development/testing state into a clean, production-ready application. The design focuses on removing redundancy, fixing the OpenAI response loop issue, and creating a streamlined user experience.

## Architecture

### Current Issues Analysis
1. **File Redundancy**: Multiple test files (`test_app.py`, `test_simple.py`, `test_api_key.py`) with overlapping functionality
2. **Setup Complexity**: Multiple setup guides (`setup_guide.md`, `quick_setup.md`) causing confusion
3. **Loop Issue**: The chatbot conversation history management is causing infinite loops in responses
4. **API Key Handling**: Placeholder API key in `.env` file needs proper validation

### Target Architecture
```
web-scraper-chatbot/
├── app.py              # Main Streamlit application
├── scraper.py          # Web scraping functionality
├── chatbot.py          # OpenAI integration (optimized)
├── requirements.txt    # Dependencies
├── README.md           # Comprehensive documentation
├── .env.example        # Template for environment variables
└── .env                # User's actual environment variables
```

## Components and Interfaces

### 1. File Cleanup Strategy
- **Remove**: `test_app.py`, `test_simple.py`, `test_api_key.py`, `demo.py`, `setup_api_key.py`, `set_key.bat`
- **Remove**: `setup_guide.md`, `quick_setup.md` (consolidate into README)
- **Keep**: Core functionality files (`app.py`, `scraper.py`, `chatbot.py`, `requirements.txt`)
- **Update**: `.env` file with proper placeholder and create `.env.example`

### 2. Chatbot Loop Fix
The infinite loop issue is caused by improper conversation history management in the `ask_question` method:

**Current Problem:**
```python
# In chatbot.py - this causes loops
messages.extend(self.conversation_history[-6:])  # Adding history AFTER current question
```

**Solution Design:**
- Separate system context from conversation history
- Add conversation history BEFORE the current question
- Implement proper message deduplication
- Add conversation turn tracking

### 3. Enhanced Error Handling
- Implement structured error responses
- Add API key validation with specific error messages
- Create user-friendly error display in Streamlit
- Add retry logic for transient failures

### 4. Streamlined User Experience
- Single README with clear setup instructions
- Improved API key validation flow
- Better error messages in the UI
- Simplified project structure

## Data Models

### Conversation Message Structure
```python
{
    "role": "user" | "assistant" | "system",
    "content": str,
    "timestamp": datetime,
    "turn_id": int
}
```

### Error Response Structure
```python
{
    "error_type": "api_key" | "rate_limit" | "network" | "parsing",
    "message": str,
    "user_action": str,  # What user should do
    "technical_details": str  # For debugging
}
```

## Error Handling

### API Key Validation
1. **Format Check**: Verify key starts with 'sk-' and has proper length
2. **Authentication Test**: Make a minimal API call to validate
3. **User Feedback**: Clear instructions for fixing invalid keys
4. **Fallback**: Allow manual entry in UI if environment variable fails

### OpenAI API Error Handling
1. **Rate Limiting**: Detect and inform user about quota issues
2. **Network Errors**: Retry with exponential backoff
3. **Invalid Responses**: Parse and handle malformed API responses
4. **Context Length**: Manage token limits by truncating old conversation history

### Scraping Error Handling
1. **Network Timeouts**: Graceful handling with user feedback
2. **Invalid URLs**: Validation and error messages
3. **Content Parsing**: Handle malformed HTML gracefully
4. **Rate Limiting**: Respect server limits with configurable delays

## Testing Strategy

### Manual Testing Approach
Since we're removing automated test files, we'll rely on:
1. **Interactive Testing**: Use the Streamlit app for end-to-end testing
2. **Error Scenario Testing**: Deliberately trigger error conditions
3. **API Key Testing**: Test with invalid, missing, and valid keys
4. **Scraping Testing**: Test with various website types and error conditions

### Validation Checklist
- [ ] App starts without errors
- [ ] API key validation works correctly
- [ ] Scraping functionality works with test URLs
- [ ] Chatbot responds without loops
- [ ] Error messages are clear and actionable
- [ ] Documentation is complete and accurate

## Implementation Phases

### Phase 1: File Cleanup
- Remove redundant files
- Consolidate documentation
- Update .env configuration

### Phase 2: Fix Chatbot Loop Issue
- Refactor conversation history management
- Implement proper message flow
- Add turn-based conversation tracking

### Phase 3: Enhanced Error Handling
- Improve API key validation
- Add structured error responses
- Update UI error display

### Phase 4: Documentation and Polish
- Create comprehensive README
- Add inline code comments
- Final testing and validation

## macOS Compatibility Considerations

### Environment Variables
- Use `export` command instead of `set` for environment variables
- Support both `.env` files and shell profile configuration
- Handle macOS-specific path separators and home directory references

### File System Compatibility
- Ensure all file paths use forward slashes
- Handle macOS case-sensitive file system considerations
- Support macOS-specific temporary directory locations

### Python Environment
- Compatible with macOS system Python and Homebrew Python
- Support for macOS virtual environments (venv, conda)
- Handle macOS-specific SSL certificate issues

### Documentation Updates
- Provide macOS-specific setup commands
- Include Terminal.app usage instructions
- Add macOS troubleshooting section

## Security Considerations

1. **API Key Protection**: Ensure .env file is in .gitignore
2. **Input Sanitization**: Validate URLs and user inputs
3. **Content Filtering**: Limit scraped content size to prevent abuse
4. **Error Information**: Avoid exposing sensitive details in error messages
5. **macOS Permissions**: Handle macOS security prompts and permissions gracefully