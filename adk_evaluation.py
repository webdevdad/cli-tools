import json
from adk_agent import create_adk_agent

class AgentEvaluator:
    def __init__(self, agent=None):
        self.agent = agent or create_adk_agent()
        self.test_cases = []

    def add_test_case(self, input_text, expected_output):
        self.test_cases.append({
            "input": input_text,
            "expected": expected_output
        })

    def run_evaluation(self):
        results = []
        for case in self.test_cases:
            response = self.agent.run(case["input"])
            passed = self._compare(response, case["expected"])
            results.append({
                "input": case["input"],
                "expected": case["expected"],
                "response": response,
                "passed": passed
            })
        return results

    def _compare(self, response, expected):
        # Simple string equality check; can be extended to fuzzy matching
        return response.strip() == expected.strip()

if __name__ == "__main__":
    evaluator = AgentEvaluator()
    evaluator.add_test_case(
        "Create my title with Appetizers: Bruschetta $8, Calamari $12",
        "# Menu\n\n## Appetizers\n- Bruschetta: $8\n- Calamari: $12\n\n"
    )
    evaluator.add_test_case(
        "Generate query for tables: users, orders fields: name, amount where: users.id = orders.user_id",
        "SELECT name, amount\nFROM users, orders\nWHERE users.id = orders.user_id"
    )
    results = evaluator.run_evaluation()
    print(json.dumps(results, indent=2))
