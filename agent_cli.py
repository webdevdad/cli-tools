#!/usr/bin/env python3
from multi_tool_agent import MultiToolAgent

def main():
    print("Multi-Tool Agent CLI")
    print("Type 'exit' to quit\n")
    
    agent = MultiToolAgent()
    
    while True:
        try:
            user_input = input("> ")
            if user_input.lower() == 'exit':
                break
            
            response = agent.process_request(user_input)
            print(f"\nAgent: {response}\n")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
