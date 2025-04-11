import os
import sys
import zipfile
from openai import OpenAI, OpenAIError

# --- Configuration ---
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = "gpt-4o" # Use a more powerful model for code understanding
# MODEL_NAME = "gpt-4-turbo" # Another good option
# MODEL_NAME = "gpt-3.5-turbo" # Cheaper, but may struggle with complex code/instructions

# --- Helper Function for API Call (Can reuse or adapt from meet_title.py) ---
def get_ai_suggestion(prompt_text, max_response_tokens=3000): # Allow more tokens for docs
    """Sends a prompt to the OpenAI API and returns the text response."""
    if not API_KEY:
        print("Error: OPENAI_API_KEY environment variable not set.")
        sys.exit(1)

    try:
        client = OpenAI(api_key=API_KEY)
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are an expert technical writer specializing in generating Markdown documentation from Java source code, strictly following formatting instructions."},
                {"role": "user", "content": prompt_text}
            ],
            max_tokens=max_response_tokens,
            temperature=0.1 # Low temperature for factual, consistent output
        )
        # Ensure response structure is as expected (same logic as meet_title)
        if response.choices and len(response.choices) > 0:
             choice = response.choices[0]
             if hasattr(choice, 'message') and hasattr(choice.message, 'content'):
                return choice.message.content.strip()
             else:
                 print("Warning: Unexpected API response structure.")
                 return "Error: Could not parse AI response."
        else:
            return "Error: No response choices received from API."
    except OpenAIError as e:
        # Handle potential context length errors specifically
        if "context_length_exceeded" in str(e):
             print(f"Error: The provided source code likely exceeds the model's ({MODEL_NAME}) context window limit.")
             print("Try reducing the number of files in the ZIP or using a model with a larger context window.")
        else:
            print(f"Error calling OpenAI API: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

# --- Function to Read Java Files from ZIP ---
def extract_java_code_from_zip(zip_path):
    """Extracts content of .java files from a ZIP archive."""
    code_content = {} # Dictionary: { "path/in/zip/MyClass.java": "code string" }
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            for filename in z.namelist():
                # Process only files ending in .java and ignore common build/test directories
                if filename.endswith(".java") and not any(part in filename.lower() for part in ['/test/', '/build/', '/target/', '/.git/', '/.settings/']):
                    # Clean up potential directory structures if needed, but keep path for context
                    # cleaned_path = '/'.join(filename.split('/')[1:]) # Example: remove top-level dir if zip contains one

                    # Skip empty files
                    if z.getinfo(filename).file_size == 0:
                         print(f"Skipping empty file: {filename}")
                         continue

                    try:
                        with z.open(filename) as f:
                            # Decode safely, replacing errors
                            code_content[filename] = f.read().decode('utf-8', errors='replace')
                    except Exception as read_err:
                         print(f"Warning: Could not read or decode file '{filename}': {read_err}")

        if not code_content:
             print(f"Warning: No non-empty .java files found in the ZIP: {zip_path}")

        return code_content

    except zipfile.BadZipFile:
        print(f"Error: Invalid or corrupted ZIP file: {zip_path}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: ZIP file not found: {zip_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading ZIP file '{zip_path}': {e}")
        sys.exit(1)

# --- Functions for User Input ---
def get_zip_path():
    """Prompts user for the ZIP file path and validates it."""
    while True:
        zip_path = input("Enter the path to the ZIP file containing Java source code: ").strip()
        if not zip_path:
            print("Error: ZIP file path cannot be empty.")
            continue
        if not os.path.isfile(zip_path):
            print(f"Error: File not found at '{zip_path}'. Please check the path.")
            continue
        if not zipfile.is_zipfile(zip_path):
            print(f"Error: File '{zip_path}' is not a valid ZIP archive.")
            continue
        return zip_path

def get_data_version():
    """Prompts user for the data version, allowing a default."""
    version = input("Enter the data version for the documentation (e.g., 1.0, default is 1.0): ").strip()
    return version if version else "1.0"

def get_output_path():
    """Prompts user for the output file path, allowing empty for console output."""
    path = input("Enter output file path for Markdown (leave blank to print to console): ").strip()
    return path if path else None


# --- Main Script Logic ---
if __name__ == "__main__":
    print("--- Java Code-to-Markdown Documentation Generator ---")

    # Get inputs from user
    zip_file_path = get_zip_path()
    data_version = get_data_version()
    output_file_path = get_output_path()

    print(f"\nProcessing Java code from: {zip_file_path}")
    java_files_content = extract_java_code_from_zip(zip_file_path)

    if not java_files_content:
        print("No Java code found to process. Exiting.")
        sys.exit(0) # Not an error, just nothing to do

    # --- Construct the Detailed Prompt ---
    # Base instructions - VERY IMPORTANT to be precise
    prompt_base = f"""
Generate technical documentation in a single Markdown file for the provided Java 'event' classes.

**Formatting Rules (Strictly Follow):**

1.  **Data Version:** Denote the data version as: `Data Version: {data_version}` at the very beginning of the output. NO other text or formatting should precede this line.
2.  **File Structure:**
    *   Use Level 1 headings (`#`) for the Java package structure containing each Java file. Use Title Case capitalization for these headings (e.g., `# Com/Example/Events`). Derive this path from the file path provided (e.g., `com/example/events/UserCreatedEvent.java` implies the heading `# Com/Example/Events`). Do NOT include any root directory names from the ZIP structure itself.
    *   If multiple files are in the same package directory, group them under the same Level 1 heading.
3.  **Event Documentation:**
    *   Use Level 2 headings (`##`) for each event name. Base the event name directly on the Java class name (e.g., `## UserCreatedEvent`).
4.  **Property Table:**
    *   Immediately following the Level 2 heading for each event, create a Markdown table detailing its properties (class fields/members).
    *   The table MUST have these columns: `Property Name`, `Data Type`, `Description (from JavaDoc)`, `Annotations`.
    *   Populate the table based on the Java class properties.
    *   For the 'Description', use the JavaDoc comment associated with the property, if available. If no JavaDoc, leave it blank or write "N/A".
    *   For the 'Annotations', list any Java annotations directly preceding the property definition (e.g., `@NotNull`, `@JsonProperty("userId")`). Include the full annotation text.
5.  **General Text:** All other text MUST be normal (non-header) paragraph text. Do NOT add introductory sentences before the tables unless they are part of a class-level JavaDoc description.
6.  **Annotations Focus:** Pay close attention to documenting the annotations accurately in the table.
7.  **Output Format:** Produce ONLY the raw Markdown content exactly as specified. Do NOT wrap the output in code fences (```markdown ... ``` or similar). Do not add any explanations, introductions, or conclusions outside the specified format. Start directly with the Data Version line and end immediately after the last documented item.

**Source Code:**

Below is the content of the relevant Java files, keyed by their path within the project/ZIP:

"""

    # Append the extracted code to the prompt
    code_blocks = []
    total_chars = len(prompt_base)
    for path, code in java_files_content.items():
        block = f"--- File: {path} ---\n```java\n{code}\n```\n"
        code_blocks.append(block)
        total_chars += len(block)

    # Simple check for excessive length (can be refined based on model limits)
    # ~4 chars per token is a rough estimate
    estimated_tokens = total_chars / 4
    print(f"Estimated prompt size: ~{estimated_tokens:.0f} tokens.")
    # Warn if potentially too large (e.g., > 100k tokens for gpt-4-turbo's 128k limit, leaving room for response)
    if estimated_tokens > 100000:
         print("Warning: Prompt size is very large, potentially exceeding model context limits. Consider reducing the input code.")


    full_prompt = prompt_base + "\n".join(code_blocks)

    # Optional: Print the prompt for debugging (can be long!)
    # print("\n--- Sending Prompt to AI ---")
    # print(full_prompt[:1000] + "\n...") # Print start of prompt
    # print("--- End of Prompt Snippet ---\n")

    print(f"Requesting Markdown documentation (Data Version: {data_version})...")
    print("-" * 30)

    markdown_output = get_ai_suggestion(full_prompt)

    print("Generation Complete.")
    print("-" * 30)

    if output_file_path:
        try:
            with open(output_file_path, 'w', encoding='utf-8') as f:
                f.write(markdown_output)
            print(f"Markdown documentation saved to: {output_file_path}")
        except IOError as e:
            print(f"Error writing to output file '{output_file_path}': {e}")
            print("\n--- Generated Markdown Output (Fallback) ---")
            print(markdown_output) # Print to console as fallback
    else:
        print("\n--- Generated Markdown Output ---")
        print(markdown_output)

    print("\nExiting.")
