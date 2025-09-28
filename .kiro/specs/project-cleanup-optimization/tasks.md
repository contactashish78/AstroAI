# Implementation Plan

- [ ] 1. Clean up redundant files and consolidate project structure
  - Remove duplicate test files: `test_app.py`, `test_simple.py`, `test_api_key.py`, `demo.py`
  - Remove redundant setup files: `setup_api_key.py`, `set_key.bat`, `setup_guide.md`, `quick_setup.md`
  - Create `.env.example` template file with proper placeholder
  - Update `.env` file with proper placeholder format
  - _Requirements: 1.1, 1.2, 1.3, 1.4_

- [ ] 2. Fix the OpenAI chatbot infinite loop issue
  - Refactor the `ask_question` method in `chatbot.py` to properly manage conversation history
  - Implement proper message ordering to prevent conversation loops
  - Add turn-based conversation tracking to avoid duplicate messages
  - Test the fix with sample conversations to ensure single responses
  - _Requirements: 2.1, 2.2, 2.3_

- [ ] 3. Enhance API key validation and error handling
  - Improve API key validation logic in `chatbot.py` with specific error types
  - Add structured error response handling for different OpenAI API errors
  - Update Streamlit UI in `app.py` to display user-friendly error messages
  - Implement proper error handling for rate limits, authentication, and network issues
  - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [ ] 4. Optimize Streamlit session state management
  - Review and optimize session state handling in `app.py`
  - Ensure proper state initialization and cleanup
  - Fix any state-related issues that could cause UI problems
  - Add proper error state management for better user experience
  - _Requirements: 5.4, 4.4_

- [ ] 5. Create comprehensive documentation
  - Write a complete README.md file with setup instructions, usage guide, and troubleshooting
  - Add inline code comments to improve code maintainability
  - Include example URLs and usage scenarios in documentation
  - Document the API key setup process clearly
  - _Requirements: 4.1, 4.2, 4.3_

- [ ] 6. Add input validation and sanitization
  - Implement URL validation in the scraper module
  - Add content size limits and sanitization in `scraper.py`
  - Validate user inputs in the Streamlit interface
  - Add proper error handling for malformed inputs
  - _Requirements: 5.2, 5.4_

- [ ] 7. Implement macOS compatibility features
  - Update all file path handling to use forward slashes and os.path.join()
  - Modify environment variable setup instructions for macOS (export vs set)
  - Add macOS-specific SSL certificate handling in scraper.py
  - Update any Windows-specific code to be cross-platform compatible
  - _Requirements: 6.1, 6.2, 6.3, 6.4_

- [ ] 8. Update documentation for macOS users
  - Add macOS-specific setup instructions using Terminal commands
  - Include macOS troubleshooting section in README
  - Provide examples using macOS file paths and commands
  - Add instructions for macOS Python virtual environment setup
  - _Requirements: 6.5, 4.1, 4.2_

- [ ] 9. Final testing and validation
  - Test the complete application workflow from setup to usage on macOS
  - Verify that all error scenarios are handled properly
  - Ensure the chatbot no longer loops and provides single responses
  - Validate that the cleaned-up project structure works correctly on macOS
  - Test environment variable setup using macOS Terminal commands
  - _Requirements: 1.4, 2.1, 3.4, 4.4, 6.6_