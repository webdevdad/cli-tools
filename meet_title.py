import os
import sys
from openai import OpenAI, OpenAIError

# --- Configuration ---
# Try to get the API key from environment variables
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = "gpt-3.5-turbo" # Or "gpt-4", "gpt-4o" etc.

# --- Helper Function for API Call ---
def get_ai_suggestion(prompt_text):
    """Sends a prompt to the OpenAI API and returns the text response."""
    if not API_KEY:
        print("Error: OPENAI_API_KEY environment variable not set.")
        sys.exit(1) # Exit script if key is missing

    try:
        client = OpenAI(api_key=API_KEY)
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful assistant skilled in creating concise, alliterative meeting titles."},
                {"role": "user", "content": prompt_text}
            ],
            max_tokens=50, # Keep response short
            temperature=0.7 # Allow for some creativity
        )
        # Ensure response structure is as expected
        if response.choices and len(response.choices) > 0:
             # Handle potential variations in API response structure
            choice = response.choices[0]
            if hasattr(choice, 'message') and hasattr(choice.message, 'content'):
                return choice.message.content.strip()
            else:
                # Fallback or alternative parsing if structure differs
                 print("Warning: Unexpected API response structure. Trying fallback.")
                 # Attempt alternative access if needed, or return a default/error
                 # For example, if the structure might be simpler:
                 # return response.choices[0].text.strip() # Example for older models/structures
                 return "Error: Could not parse AI response."

        else:
            return "Error: No response choices received from API."

    except OpenAIError as e:
        print(f"Error calling OpenAI API: {e}")
        sys.exit(1) # Exit script on API error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


# --- Functions for User Input ---
def get_meeting_topic():
    """Prompts user for the meeting topic and validates it."""
    while True:
        topic = input("Enter the meeting topic: ").strip()
        if topic:
            return topic
        else:
            print("Error: Meeting topic cannot be empty. Please try again.")

def get_starting_letter():
    """Prompts user for the starting letter and validates it."""
    while True:
        letter = input("Enter the starting letter for the title words: ").strip()
        if len(letter) == 1 and letter.isalpha():
            return letter.upper()
        else:
            print("Error: Please enter a single alphabetic character.")

def get_word_count():
    """Prompts user for the number of words (3 or 4) and validates it."""
    while True:
        count_str = input("Enter the number of words in the title (3 or 4, default 4): ").strip()
        if not count_str: # Handle empty input for default
            return 4
        try:
            count = int(count_str)
            if count in [3, 4]:
                return count
            else:
                print("Error: Please enter 3 or 4.")
        except ValueError:
            print("Error: Invalid input. Please enter a number (3 or 4).")


# --- Main Script Logic ---
if __name__ == "__main__":
    print("--- Alliterative Meeting Title Generator ---")

    # Get inputs from user
    meeting_topic = get_meeting_topic()
    start_letter = get_starting_letter()
    num_words = get_word_count()

    # Construct the prompt for the AI
    prompt = (
        f"Generate exactly {num_words} potential meeting titles about '{meeting_topic}'. "
        f"STRICTLY follow these rules:\n"
        f"1. Every word must start with '{start_letter}'\n"
        f"2. Each title must have exactly {num_words} words\n"
        f"3. List each title on a new line with no additional text\n"
        f"4. Use proper grammar and professional tone"
    )

    print(f"\nRequesting {num_words}-word titles starting with '{start_letter}' for topic: '{meeting_topic}'...")
    print("-" * 30)

    # Call the API helper function
    suggestion = get_ai_suggestion(prompt)

    # Display the result
    print("Suggested Titles:")
    print(suggestion)
    print("-" * 30)
    print("Exiting.")
