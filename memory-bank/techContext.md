# Technical Context

## Technologies Used
- Python 3.10+ for CLI tools development.
- OpenAI API for AI-powered features.
- Git and GitHub for version control and repository hosting.
- BFG Repo-Cleaner for git history rewriting and secret removal.
- Homebrew for package management on macOS.
- Markdown for documentation generation.
- Java for sample source code in documentation generator.

## Development Setup
- Python dependencies managed via `requirements.txt`.
- OpenAI API key managed via environment variable or prompt input.
- GitHub CLI (`gh`) used for repository management.
- Code formatted according to PEP 8 style guide.
- Interactive CLI launcher (`cli_tools_launcher.py`) as main user interface.

## Technical Constraints
- Secrets must never be committed to git.
- Repository must maintain clean history for security.
- Tools designed for modularity and extensibility.
- CLI tools require internet access for OpenAI API calls.

## Dependencies
- `openai` Python package for API integration.
- Standard Python libraries for CLI interaction and file handling.

## Tool Usage Patterns
- Unified launcher provides menu-driven access to all tools.
- Each tool has interactive prompts for user input.
- Outputs are either printed to console or saved to files.
- Error handling and input validation are basic but functional.
