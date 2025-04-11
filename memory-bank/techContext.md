# Tech Context

**Technologies Used:**

*   Python 3.x
*   OpenAI Python library
*   Python's built-in `input()` function for user interaction

**Development Setup:**

*   Ensure Python 3 is installed.
*   Install the OpenAI Python library: `pip install openai`
*   Set the `OPENAI_API_KEY` environment variable.

**Technical Constraints:**

*   Limited by the OpenAI API's token limits and rate limits.
*   The `code_docs.py` tool may struggle with very large codebases due to context window limitations.

**Dependencies:**

*   openai

**Tool Usage Patterns:**

*   Using `input()` to prompt the user for required information.
*   Implementing validation loops for user input.
*   Using the OpenAI Python library to interact with the OpenAI API.
*   Handling API errors and exceptions gracefully.
*   Formatting output for clear presentation in the terminal conversation.
