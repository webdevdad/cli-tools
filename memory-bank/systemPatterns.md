# System Patterns

## Architecture
- Modular CLI tool design with a unified launcher interface.
- Each tool encapsulated as a separate Python module/script.
- Interactive command-line prompts guide user input and workflow.
- AI integration via OpenAI API for natural language processing and generation.

## Key Technical Decisions
- Use of environment variables and .env file for secret management.
- GitHub repository hygiene enforced with BFG Repo-Cleaner for secret removal.
- Adoption of PEP 8 style guide for consistent Python code formatting.
- Use of Homebrew for managing external dependencies on macOS.
- Markdown as the primary output format for documentation generation.

## Design Patterns
- Command pattern implemented via menu-driven CLI launcher.
- Separation of concerns: each tool handles a distinct AI-powered task.
- Input validation and error handling embedded in interactive prompts.
- Use of external AI service abstracted behind Python API calls.

## Component Relationships
- `cli_tools_launcher.py` serves as the entry point and dispatcher.
- `meet_title.py` handles alliterative meeting title generation.
- `code_docs.py` processes Java source code ZIP files into Markdown docs.
- `sql_builder.py` provides an interactive SQL query builder with AI assistance.
- Memory bank files document project context, progress, and technical details.

## Critical Implementation Paths
- User launches CLI launcher.
- User selects desired tool.
- Tool prompts for necessary inputs.
- Tool calls OpenAI API with constructed prompts.
- Tool processes API response and outputs results.
- User can save or view output as needed.
