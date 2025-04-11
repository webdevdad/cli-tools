1#!/usr/bin/env python3
import subprocess
import sys
import os

def check_api_key():
    # Try to load from .env file first
    if os.path.exists('.env'):
        from dotenv import load_dotenv
        load_dotenv()
    
    if "OPENAI_API_KEY" not in os.environ:
        print("\n⚠️ OpenAI API key is not set!")
        print("You can get an API key from https://platform.openai.com/account/api-keys")
        key = input("Please enter your OpenAI API key (or press Enter to cancel): ")
        if key:
            # Save to .env file for future use
            with open('.env', 'w') as f:
                f.write(f"OPENAI_API_KEY={key}\n")
            os.environ["OPENAI_API_KEY"] = key
            print("API key saved to .env file for future sessions.")
            return True
        else:
            print("API key is required to use these tools.")
            return False
    return True

def show_menu():
    print("\n--- AI CLI Tools Launcher ---")
    print("1. Generate Alliterative Meeting Titles")
    print("2. Create Markdown Documentation from Java Code")
    print("3. Build SQL Queries")
    print("4. Exit")
    choice = input("\nEnter your choice (1-3): ")
    return choice

def run_meet_title():
    print("\nLaunching Meeting Title Generator...")
    subprocess.run([sys.executable, "meet_title.py"])

def run_code_docs():
    print("\nLaunching Code Documentation Generator...")
    subprocess.run([sys.executable, "code_docs.py"])

def run_sql_builder():
    print("\nLaunching Interactive SQL Query Builder...")
    subprocess.run([sys.executable, "sql_conversation.py"])

def main():
    if not check_api_key():
        return
        
    while True:
        choice = show_menu()
        if choice == "1":
            run_meet_title()
        elif choice == "2":
            run_code_docs()
        elif choice == "3":
            run_sql_builder()
        elif choice == "4":
            print("\nExiting...")
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()
