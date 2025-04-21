import google.generativeai as genai
from menu_tool import MenuTool
from sql_tool import SQLTool


class MultiToolAgent:
    def __init__(self):
        genai.configure(api_key='AIzaSyCwdfQVYyTJ8N-sDb6XRdr8HP_InPwbxHo')
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest')
        self.tools = []
        self.register_tool(MenuTool())
        self.register_tool(SQLTool())
        
    def register_tool(self, tool):
        self.tools.append(tool)
        
    def process_request(self, request):
        # Route request to appropriate tool
        for tool in self.tools:
            if tool.can_handle(request):
                return tool.handle(request)
        # Fallback to generative model
        response = self.model.generate_content(request)
        return response.text

if __name__ == "__main__":
    agent = MultiToolAgent()
    agent.process_request("Test request")
