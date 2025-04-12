#!/usr/bin/env python3
from typing import Dict, List
import re

class MenuTool:
    def __init__(self):
        self.name = "Menu Generator"
        self.description = "Creates formatted titles and markdown menus"

    def can_handle(self, request: str) -> bool:
        return any(keyword in request.lower() for keyword in 
                  ["menu", "title", "markdown", "create my title"])

    def handle(self, request: str) -> str:
        # Extract menu items from request
        items = self._parse_menu_items(request)
        
        if not items:
            return "Please provide menu items in format: 'Appetizers: Bruschetta, Calamari'"
            
        # Generate markdown
        markdown = "# Menu\n\n"
        for category, details in items.items():
            markdown += f"## {category}\n"
            if isinstance(details, dict):  # With prices
                for item, price in details.items():
                    markdown += f"- {item}: ${price}\n"
            else:  # Just items
                for item in details:
                    markdown += f"- {item}\n"
            markdown += "\n"
        
        return markdown

    def _parse_menu_items(self, text: str) -> Dict[str, List[str]]:
        # Parse different menu formats
        items = {}
        
        # Format: Category: item1, item2
        category_matches = re.findall(r'(\w+):\s*([\w\s,]+)', text)
        for category, item_list in category_matches:
            items[category] = [item.strip() for item in item_list.split(',')]
            
        # Format: Category: item1 $price, item2 $price
        price_matches = re.findall(r'(\w+):\s*((?:\w+\s*\$\d+(?:\.\d+)?[\s,]*)+)', text)
        for category, price_list in price_matches:
            items[category] = {}
            for item_price in price_list.split(','):
                if '$' in item_price:
                    item, price = item_price.strip().rsplit('$', 1)
                    items[category][item.strip()] = price.strip()
                    
        return items

if __name__ == "__main__":
    tool = MenuTool()
    print(tool.handle("Appetizers: Bruschetta $8, Calamari $12"))
