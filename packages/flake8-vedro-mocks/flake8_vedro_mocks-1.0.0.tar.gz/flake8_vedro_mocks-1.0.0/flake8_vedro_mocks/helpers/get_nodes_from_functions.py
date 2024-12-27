import ast
from typing import List

from flake8_vedro_mocks.helpers.context_manager_with_position import (
    CtxManagerWithPosition
)
from flake8_vedro_mocks.helpers.mock_assertions import is_mock_context_manager
from flake8_vedro_mocks.types import FuncType


def get_nodes_from_function_by_type(function: FuncType, node_types) -> List:
    return [
        node
        for statement in function.body
        for node in ast.walk(statement) if isinstance(node, node_types)
    ]


def get_assert_statements_from_functions(functions: List[FuncType]) -> List[ast.Assert]:
    return [
        assert_statement
        for step in functions
        for assert_statement in get_nodes_from_function_by_type(step, ast.Assert)
    ]


def get_mock_context_managers_from_function(function: FuncType,
                                            mock_name_pattern: str) -> List[CtxManagerWithPosition]:
    """
    Returns list of context managers that match mock_name_pattern and their positions (line and column offset).
    """
    context_manager_statements = get_nodes_from_function_by_type(function, (ast.With, ast.AsyncWith))
    return [
        CtxManagerWithPosition(item, statement.lineno, statement.col_offset)
        for statement in context_manager_statements
        for item in statement.items
        if is_mock_context_manager(item, mock_name_pattern)
    ]
