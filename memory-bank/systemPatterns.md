# System Patterns

**System Architecture:**

The project consists of two independent Python CLI tools. Each tool interacts with the OpenAI API to perform a specific task.

**Key Technical Decisions:**

*   Using the OpenAI Python library for API interaction.
*   Using Python's built-in `input()` function for interactive command-line prompts.
*   Implementing input validation loops to ensure correct user input.
*   Storing the OpenAI API key in an environment variable.

**Design Patterns in Use:**

*   Helper functions for API calls to handle errors and response parsing.
*   Functions dedicated to gathering user input via prompts.
*   Clear separation of concerns between configuration, user interaction, API interaction, and main script logic.

**Component Relationships:**

*   Each tool is a self-contained script with minimal dependencies.

**Critical Implementation Paths:**

*   API key retrieval and validation.
*   Interactive input gathering and validation.
*   Prompt construction based on user input.
*   API call execution.
*   Response parsing and formatted output display within the conversation.
