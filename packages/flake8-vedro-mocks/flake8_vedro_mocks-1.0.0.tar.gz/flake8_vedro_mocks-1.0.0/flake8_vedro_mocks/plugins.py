import argparse
import ast
from typing import Callable, List, Optional

from flake8.options.manager import OptionManager
from flake8_plugin_utils import Plugin, Visitor

from flake8_vedro_mocks.visitors import ScenarioVisitor

from .config import Config


class PluginWithFilename(Plugin):
    def __init__(self, tree: ast.AST, filename: str, *args, **kwargs):
        super().__init__(tree)
        self.filename = filename

    def run(self):
        for visitor_cls in self.visitors:
            visitor = self._create_visitor(visitor_cls, filename=self.filename)
            visitor.visit(self._tree)
            for error in visitor.errors:
                yield self._error(error)

    @classmethod
    def _create_visitor(cls, visitor_cls: Callable, filename: Optional[str] = None) -> Visitor:
        if cls.config is None:
            return visitor_cls(filename=filename)
        return visitor_cls(config=cls.config, filename=filename)


class VedroMocksPlugin(PluginWithFilename):
    name = 'flake8_vedro_mocks'
    version = '1.0.0'
    visitors = [ScenarioVisitor]

    def __init__(self, tree: ast.AST, filename: str, *args, **kwargs):
        super().__init__(tree, filename)

    @classmethod
    def add_options(cls, option_manager: OptionManager):
        option_manager.add_option(
            '--mock-name-pattern',
            default=r"(?=.*mock)(?!.*grpc)",
            type=str,
            parse_from_config=True,
            help='Mock function name pattern to match when searching for mocks for further assertions',
        )

    @classmethod
    def parse_options_to_config(
        cls, option_manager: OptionManager, options: argparse.Namespace, args: List[str]
    ) -> Config:
        return Config(mock_name_pattern=options.mock_name_pattern)
