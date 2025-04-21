from google.adk.agents import Agent
from menu_tool import MenuTool
from sql_tool import SQLTool

class ADKMenuTool:
    def __init__(self):
        self.name = "Menu Generator"
        self.description = "Creates formatted titles and markdown menus"
        self.menu_tool = MenuTool()

    def can_handle(self, request: str) -> bool:
        return self.menu_tool.can_handle(request)

    def call(self, request: str) -> str:
        return self.menu_tool.handle(request)

class ADKSQLTool:
    def __init__(self):
        self.name = "SQL Builder"
        self.description = "Generates and optimizes SQL queries"
        self.sql_tool = SQLTool()

    def can_handle(self, request: str) -> bool:
        return self.sql_tool.can_handle(request)

    def call(self, request: str) -> str:
        return self.sql_tool.handle(request)

def create_adk_agent():
    tools = [ADKMenuTool(), ADKSQLTool()]
    agent = Agent(
        name="enterprise_agent",
        model="gemini-2.0-flash",
        instruction="You are a helpful assistant. Use tools when appropriate.",
        description="An enterprise AI agent with menu and SQL tools.",
        tools=tools
    )
    return agent

if __name__ == "__main__":
    agent = create_adk_agent()
    test_request = "Create my title with Appetizers: Bruschetta $8, Calamari $12"
    response = agent.run(test_request)
    print("Response:", response)
