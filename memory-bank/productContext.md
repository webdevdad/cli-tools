# Product Context

## Purpose
The CLI Tools project aims to provide a suite of AI-powered command-line utilities that automate common tasks related to meetings, code documentation, and SQL query building. These tools enhance productivity by leveraging natural language processing and generation capabilities of the OpenAI API.

## Problems It Solves
- Generates creative, alliterative meeting titles to make meetings more engaging.
- Converts Java source code into well-structured Markdown documentation, saving manual effort.
- Builds SQL queries interactively from natural language descriptions, reducing the need for deep SQL expertise.

## How It Should Work
- Users interact with a unified CLI launcher that presents a menu of available tools.
- Each tool guides users through an interactive prompt sequence to gather necessary inputs.
- Tools communicate with the OpenAI API to process inputs and generate outputs.
- Outputs are presented in the console or saved to files as specified by the user.
- The system handles API key management securely via environment variables or prompt input.

## User Experience Goals
- Simple, intuitive command-line interface accessible to users with basic technical skills.
- Clear prompts and validation to minimize user errors.
- Fast and accurate AI-powered responses.
- Secure handling of sensitive information.
- Comprehensive documentation and examples to facilitate adoption.
