# CLI Tools for AI Automation

[Updated Documentation Structure]

## Project Structure
```
cli_tools/
├── .clinerules          # Development guidelines
├── cli_tools_launcher.py # Main entry point
├── meet_title.py        # Meeting title generator
├── code_docs.py         # Code documentation tool
├── sql_builder.py       # SQL query builder
├── requirements.txt     # Dependencies
├── README.md            # Project documentation
└── memory-bank/         # Project knowledge base
    ├── projectbrief.md
    ├── productContext.md
    ├── systemPatterns.md
    ├── techContext.md
    ├── progress.md
    └── activeContext.md
```

This project provides two command-line tools built with Python to automate specific AI-powered tasks: generating alliterative meeting titles and creating Markdown documentation from Java source code.

## Tools

1.  **Alliterative Meeting Title Generator (`meet_title.py`)**: Generates creative, alliterative meeting titles based on a topic and a starting letter.
2.  **Code-to-Markdown Documentation Generator (`code_docs.py`)**: Creates technical documentation in Markdown format from Java source code provided in a ZIP file.
3.  **SQL Query Builder (`sql_builder.py`)**: Converts natural language to SQL queries with safety checks. [See detailed documentation](sql_builder_docs.md).

## Setup

1.  **Clone the repository (if applicable):**
    ```bash
    git clone <repository_url>
    cd cli_tools
    ```

2.  **Install Dependencies:**
    Ensure you have Python 3 installed. Then, install the required library:
    ```bash
    pip install -r requirements.txt
    ```
    *(This will install the `openai` library).*

3.  **OpenAI API Key:**
    These tools require an OpenAI API key to function. You can:
    - Set it as an environment variable before running:
      ```bash
      export OPENAI_API_KEY="your_openai_api_key"
      ```
      *(On Windows, use `set OPENAI_API_KEY=your_openai_api_key` in Command Prompt or `$env:OPENAI_API_KEY="your_openai_api_key"` in PowerShell)*
    - Or enter it when prompted by the launcher
    - Get an API key from [OpenAI](https://platform.openai.com/account/api-keys)

## Usage

### Unified Launcher (`cli_tools_launcher.py`)

This menu-driven interface provides access to all tools:

```bash
python cli_tools_launcher.py
```

**Main Menu:**
1. Generate Alliterative Meeting Titles
2. Create Markdown Documentation from Java Code
3. Build SQL Queries
4. Exit

### Tool Details

#### 1. Alliterative Meeting Title Generator
- Guides you through creating meeting titles where each word starts with the same letter
- Interactive workflow:
  1. Enter meeting topic
  2. Choose starting letter
  3. Select number of words (3 or 4)

#### 2. Code-to-Markdown Documentation Generator
- Creates technical documentation from Java source code
- Interactive workflow:
  1. Provide path to ZIP file containing Java code
  2. Specify documentation version
  3. Choose output destination

**Example Output:**
```markdown
Data Version: 1.2
# Com/Example/Events

## UserCreatedEvent
| Property | Type   | Description          |
|----------|--------|----------------------|
| userId   | String | Unique user identifier|
```

**Output (saved to `event_docs.md`):**

```markdown
Data Version: 1.2

# Com/Example/Events

## UserCreatedEvent

Represents an event triggered when a new user is created.

| Property Name | Data Type | Description (from JavaDoc) | Annotations |
|---------------|-----------|----------------------------|-------------|
| userId        | String    | The unique identifier for the user. | @NotNull, @JsonProperty("userId") |
| email         | String    | The email address of the new user. | @NotNull |

## OrderPlacedEvent

Represents an event when an order is successfully placed.

| Property Name | Data Type | Description (from JavaDoc) | Annotations |
|---------------|-----------|----------------------------|-------------|
| orderId       | String    | The unique ID for the order. | @NotNull |
| customerId    | String    | ID of the customer placing the order. | @NotNull |
| totalAmount   | BigDecimal| The total amount of the order. | N/A |
```
*(Note: The exact output depends on the content of your Java files and the AI model's response).*

## Contributing

Contributions are welcome! Please follow standard fork-and-pull-request workflows.

## License

MIT License
