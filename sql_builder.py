

#!/usr/bin/env python3
from pydantic import BaseModel, conint, Field
from typing import Optional, Literal
from openai import OpenAI
import os

class SQLMessage(BaseModel):
    prompt: str 
    db_schema: Optional[str] = Field(None, alias="schema")
    dialect: Literal['sqlite', 'postgres'] = 'sqlite'
    safety_check: bool = True

class SQLResponse(BaseModel):
    query: str 
    explanation: str
    alternatives: list[str]
    valid: bool
    safety_rating: conint(ge=0, le=5)

class SQLBuilderError(Exception):
    def __init__(self, message, type, param):
        super().__init__(message)
        self.type = type
        self.param = param

class SQLBuilder:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    def create(self, message: SQLMessage, conversation_history: list[dict] = None) -> SQLResponse:
        try:
            messages = []
            if conversation_history:
                messages.extend(conversation_history)
            messages.append({
                "role": "user",
                "content": self._build_prompt(message)
            })
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages
            )
            return self._parse_response(response.choices[0].message.content)
        except Exception as e:
            raise SQLBuilderError(str(e), "api_error", None)

    def _build_prompt(self, message: SQLMessage) -> str:
        base = f"""Convert this natural language request to {message.dialect} SQL:

Request: {message.prompt}

Format your response EXACTLY as follows:
---SQL---
[SQL query here]
---EXPLANATION---
[Detailed explanation]
---ALTERNATIVES---
[Alternative approaches, one per line]

Guidelines:
1. Generate production-ready SQL with proper comments
2. Use the schema if provided
3. Include safety checks if requested
4. Handle edge cases
5. Return ONLY the formatted response - no additional commentary
6. The response MUST include all three sections (SQL, EXPLANATION, ALTERNATIVES)
7. If no alternatives exist, include "None" in ALTERNATIVES section

Example response format:
---SQL---
SELECT * FROM users;
---EXPLANATION---
This query selects all columns from the users table
---ALTERNATIVES---
None"""

        if message.db_schema:
            base += f"\n\nDatabase Schema:\n{message.db_schema}"
        if message.safety_check:
            base += "\n\nSafety Requirements:\n- Parameterize inputs\n- Validate data types\n- Handle NULL values\n- Prevent SQL injection"
        return base

    def _parse_response(self, text: str) -> SQLResponse:
        """Parse the AI response into structured SQL components with enhanced validation."""
        try:
            if not text.strip():
                raise ValueError("Empty response from AI")
            
            # Validate required sections exist
            required_sections = ["---SQL---", "---EXPLANATION---", "---ALTERNATIVES---"]
            for section in required_sections:
                if section not in text:
                    raise ValueError(f"Missing required section: {section}")
            
            # Extract and validate SQL query
            query = text.split("---SQL---")[1].split("---EXPLANATION---")[0].strip()
            if not query or not query.startswith(("SELECT", "INSERT", "UPDATE", "DELETE", "WITH")):
                raise ValueError("Invalid SQL query - must start with valid SQL keyword")
            
            # Extract explanation
            explanation = text.split("---EXPLANATION---")[1].split("---ALTERNATIVES---")[0].strip()
            if not explanation:
                raise ValueError("Explanation cannot be empty")
            
            # Extract alternatives
            alternatives = [
                alt.strip() for alt in text.split("---ALTERNATIVES---")[1].strip().split("\n") 
                if alt.strip() and alt.strip().lower() != "none"
            ]
            
            # Basic SQL syntax validation
            if ";" not in query:
                query += ";"
            
            return SQLResponse(
                query=query,
                explanation=explanation,
                alternatives=alternatives,
                valid=True,
                safety_rating=self._calculate_safety_rating(query)
            )
        except Exception as e:
            return SQLResponse(
                query="SELECT 1;",  # Safe default query
                explanation=f"Error: {str(e)}",
                alternatives=[],
                valid=False,
                safety_rating=1
            )

    def _calculate_safety_rating(self, query: str) -> int:
        """Calculate safety rating (1-5) based on query characteristics."""
        rating = 4  # Base rating
        
        # Deduct points for potential risks
        if any(keyword in query.upper() for keyword in ["DROP", "TRUNCATE", "ALTER"]):
            rating -= 2
        if "WHERE" not in query.upper() and query.upper().startswith(("UPDATE", "DELETE")):
            rating -= 1
        if any(op in query for op in ["*=", "/=", "%="]):  # Math operations
            rating -= 1
            
        return max(1, min(5, rating))  # Clamp between 1-5

def save_to_file(response: SQLResponse, filename: str = "sql_output.md"):
    """Save SQL response to a markdown file"""
    with open(filename, "w") as f:
        f.write(f"# SQL Query\n```sql\n{response.query}\n```\n\n")
        f.write(f"## Explanation\n{response.explanation}\n\n")
        if response.alternatives:
            f.write("## Alternative Approaches\n")
            for alt in response.alternatives:
                f.write(f"- {alt}\n")
        f.write(f"\nSafety Rating: {response.safety_rating}/5")

if __name__ == "__main__":
    builder = SQLBuilder()
    test_msg = SQLMessage(prompt="Find users with duplicate emails")
    response = builder.create(test_msg)
    print(response)
    save_to_file(response)
