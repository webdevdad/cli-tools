#!/usr/bin/env python3
from typing import Dict, Optional
import re

class SQLTool:
    def __init__(self):
        self.name = "SQL Builder"
        self.description = "Generates and optimizes SQL queries"

    def can_handle(self, request: str) -> bool:
        return any(keyword in request.lower() for keyword in 
                 ["sql", "query", "database", "schema"])

    def handle(self, request: str) -> str:
        # Clean input by removing example prefixes if present
        clean_request = re.sub(r'^.*?(tables?:)', r'\1', request, flags=re.IGNORECASE)
        
        # Parse request for schema info or query requirements
        schema = self._parse_schema(clean_request)
        requirements = self._parse_requirements(clean_request)
        
        if not requirements:
            return "Please specify your query requirements (tables, fields, conditions)"
            
        # Generate base query
        query = self._generate_query(requirements, schema)
        
        # Add optimizations if schema provided
        if schema:
            query += "\n\n-- Optimization Suggestions:\n"
            query += self._generate_optimizations(requirements, schema)
            
        return query

    def _parse_schema(self, text: str) -> Optional[Dict]:
        # Extract schema information if provided
        schema_matches = re.findall(r'schema:\s*({.*?})', text)
        if schema_matches:
            try:
                return eval(schema_matches[0])
            except:
                return None
        return None

    def _parse_requirements(self, text: str) -> Dict:
        # Parse query requirements from structured input
        reqs = {'tables': [], 'fields': [], 'conditions': []}
        
        # Extract tables (after "tables:" but before next keyword)
        table_match = re.search(r'table[s]?:\s*([^,\n]+(?:,[^,\n]+)*)', text)
        if table_match:
            reqs['tables'] = [t.strip() for t in table_match.group(1).split(',')]
        
        # Extract fields (after "fields:" but before next keyword)
        field_match = re.search(r'field[s]?:\s*([^,\n]+(?:,[^,\n]+)*)(?=\s*(?:where:|$))', text)
        if field_match:
            reqs['fields'] = [f.strip() for f in field_match.group(1).split(',')]
        
        # Extract conditions (after "where:")
        condition_match = re.search(r'where:\s*([^\n]+)', text)
        if condition_match:
            reqs['conditions'] = [condition_match.group(1).strip()]
        
        return reqs

    def _generate_query(self, requirements: Dict, schema: Optional[Dict]) -> str:
        # Basic query generation
        query = "SELECT "
        if requirements.get('fields'):
            query += ", ".join(requirements['fields'])
        else:
            query += "*"
            
        query += "\nFROM "
        query += ", ".join(requirements['tables'])
        
        if requirements.get('conditions'):
            query += "\nWHERE " + requirements['conditions'][0]
            
        return query

    def _generate_optimizations(self, requirements: Dict, schema: Dict) -> str:
        # Generate optimization suggestions based on schema
        optimizations = []
        for table in requirements['tables']:
            if table in schema:
                if 'indexes' in schema[table]:
                    optimizations.append(f"- Consider using index: {schema[table]['indexes']}")
                if 'primary_key' in schema[table]:
                    optimizations.append(f"- Join on primary key: {schema[table]['primary_key']}")
        return "\n".join(optimizations)

if __name__ == "__main__":
    tool = SQLTool()
    print(tool.handle("Generate query for tables: users, orders fields: name, amount where: users.id = orders.user_id"))
