import ast
from typing import List


class ScenarioHelper:

    def get_all_steps(self, class_node: ast.ClassDef) -> List:
        return [
            element for element in class_node.body if (
                isinstance(element, ast.FunctionDef)
                or isinstance(element, ast.AsyncFunctionDef)
            )
        ]

    def get_when_steps(self, steps: List) -> List:
        return [
            step for step in steps if step.name.startswith('when')
        ]

    def get_assertion_steps(self, steps: List) -> List:
        return [
            step for step in steps if step.name.startswith(('then', 'and', 'but'))
        ]
