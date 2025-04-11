#!/usr/bin/env python3
from sql_builder import SQLBuilder, SQLMessage, save_to_file
import openai
import json
from pathlib import Path
from enum import Enum, auto

class ConversationState(Enum):
    INITIAL = auto()
    REFINING = auto()
    VALIDATING = auto()
    COMPLETE = auto()

def main():
    builder = SQLBuilder()
    history_file = Path(".sql_history.json")
    state = ConversationState.INITIAL
    current_query = None
    
    print("Interactive SQL Builder")
    print("Describe your query in plain English. We'll work together to refine it.")
    print("Commands: quit, save, edit, test, done")

    while True:
        prompt = input("\nDescribe your query: ")
        
        if prompt.lower() == 'quit':
            break
            
        if prompt.lower() == 'save':
            filename = input("Filename (default: sql_output.md): ") or "sql_output.md"
            save_to_file(current_query, filename)
            print(f"Saved to {filename}")
            continue
            
        if prompt.lower() == 'edit':
            print(f"Current query:\n```sql\n{current_query.query}\n```")
            new_prompt = input("Enter your corrections: ")
            prompt = f"Revise this query: {current_query.query}\nChanges needed: {new_prompt}"
            
        if prompt.lower() == 'test':
            print("Test mode - would execute:")
            print(f"```sql\n{current_query.query}\n```")
            continue
            
        if prompt.lower() == 'done':
            print("Final query:")
            print(f"```sql\n{current_query.query}\n```")
            break

        # Use OpenAI API for natural conversation
        conversation = [
            {"role": "system", "content": "You are an SQL expert helping users build queries through conversation."},
            {"role": "user", "content": prompt}
        ]
        
        # Get AI response using new OpenAI API (v1.0+)
        client = openai.OpenAI()
        ai_response = client.chat.completions.create(
            model="gpt-4",
            messages=conversation,
            temperature=0.7
        )
        
        # Process response
        ai_text = ai_response.choices[0].message.content
        print(f"\nAI Assistant: {ai_text}")
        
        # Get refined prompt from user
        refined_prompt = input("\nYour response: ")
        
        message = SQLMessage(prompt=refined_prompt)
        response = builder.create(message)
        current_query = response
        
        print(f"\nDraft Query:\n```sql\n{response.query}\n```")
        print(f"\nExplanation:\n{response.explanation}")
        
        if response.alternatives:
            print("\nOptions:")
            for i, alt in enumerate(response.alternatives, 1):
                print(f"{i}. {alt}")
                
        print("\nWhat would you like to do?")
        print("1. Save this query")
        print("2. Make changes")
        print("3. Test with sample data")
        print("4. Finalize and exit")

if __name__ == "__main__":
    main()
