import ast
import re


def is_mock_context_manager(item: ast.withitem, mock_name_pattern: str) -> bool:
    """Checks if item is a mock context manager with its name matching mock_name_pattern."""
    if (
            isinstance(item.context_expr, ast.Call)
            and isinstance(item.context_expr.func, ast.Name)
            and re.search(mock_name_pattern, item.context_expr.func.id)
    ):
        return True
    return False
