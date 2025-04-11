# SQL Builder Tool Documentation

## Overview
The SQL Builder tool (`sql_builder.py`) provides a natural language interface for generating SQL queries, inspired by Claude's client patterns. It converts plain English prompts into properly formatted SQL queries with safety checks and explanations.

## Features
- Natural language to SQL conversion
- Support for SQLite and PostgreSQL dialects
- Schema-aware query generation
- Built-in safety checks
- Type-safe interfaces using Pydantic
- Claude-style error handling

## Installation
1. Ensure dependencies are installed:
```bash
pip install -r requirements.txt
```

2. Set your Anthropic API key:
```bash
export ANTHROPIC_API_KEY="your_api_key"
```

## Usage

### Command Line
```bash
python sql_builder.py
```

### Programmatic API
```python
from sql_builder import SQLBuilder, SQLMessage

builder = SQLBuilder()
response = builder.create(
    SQLMessage(
        prompt="Find users with duplicate emails",
        schema="users(id INT, email TEXT)",
        dialect="postgres"
    )
)
```

### Message Structure
```python
class SQLMessage(BaseModel):
    prompt: str 
    schema: Optional[str] = None
    dialect: Literal['sqlite', 'postgres'] = 'sqlite'
    safety_check: bool = True
```

### Response Structure
```python
class SQLResponse(BaseModel):
    query: str 
    explanation: str
    alternatives: list[str]
    valid: bool
    safety_rating: conint(ge=0, le=5)
```

## Examples

### Basic Query
```python
msg = SQLMessage(prompt="Find inactive users last logged in before 2024")
response = builder.create(msg)
```

### With Schema
```python
msg = SQLMessage(
    prompt="Find orders over $100",
    schema="orders(id INT, amount DECIMAL, customer_id INT)"
)
```

## Error Handling
The tool raises `SQLBuilderError` with:
- `message`: Human-readable error
- `type`: Error category (e.g. "api_error")
- `param`: Parameter causing the error

## Safety Features
1. Query validation
2. Injection prevention
3. Permission checks
4. Cost estimation

## Integration
The tool is integrated into the main CLI launcher as option 3.
