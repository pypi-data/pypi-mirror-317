import ast
from typing import List, Optional, Type

from flake8_vedro_mocks.abstract_checkers import ScenarioHelper, StepsChecker
from flake8_vedro_mocks.config import Config
from flake8_vedro_mocks.types import FuncType
from flake8_vedro_mocks.visitors._visitor_with_filename import (
    VisitorWithFilename
)


class Context:
    def __init__(self, steps: List[FuncType], scenario_node: ast.ClassDef, filename: str):
        self.steps = steps
        self.scenario_node = scenario_node
        self.filename = filename


class ScenarioVisitor(VisitorWithFilename):
    steps_checkers: List[StepsChecker] = []

    def __init__(self, config: Optional[Config] = None, filename: Optional[str] = None) -> None:
        super().__init__(config, filename)

    @property
    def config(self):
        return self._config

    @classmethod
    def register_steps_checker(cls, checker: Type[StepsChecker]):
        cls.steps_checkers.append(checker())
        return checker

    @classmethod
    def deregister_all(cls):
        cls.steps_checkers = []

    def visit_ClassDef(self, node: ast.ClassDef):
        if node.name == 'Scenario':
            context = Context(steps=ScenarioHelper().get_all_steps(node),
                              scenario_node=node,
                              filename=self.filename)
            try:
                for checker in self.steps_checkers:
                    self.errors.extend(checker.check_steps(context, self.config))
            except Exception as e:
                print(f'Linter failed: checking {context.filename} with {checker.__class__}.\n'
                      f'Exception: {e}')
