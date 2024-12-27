from typing import List

from flake8_plugin_utils import Error

from flake8_vedro_mocks.abstract_checkers import StepsChecker
from flake8_vedro_mocks.errors import (
    MockCallResultNotAsserted,
    MockCallResultNotSavedAsSelfAttribute
)
from flake8_vedro_mocks.helpers import (
    get_assert_statements_from_functions,
    get_mock_context_managers_from_function,
    is_self_attribute,
    is_self_attribute_asserted
)
from flake8_vedro_mocks.visitors.scenario_visitor import (
    Context,
    ScenarioVisitor
)


@ScenarioVisitor.register_steps_checker
class MockAssertChecker(StepsChecker):

    def check_steps(self, context: Context, config) -> List[Error]:
        errors = []
        when_steps = self.get_when_steps(context.steps)
        assertion_steps = self.get_assertion_steps(context.steps)
        if not when_steps or not assertion_steps:
            return []

        assert_statements = get_assert_statements_from_functions(assertion_steps)
        mock_context_managers = get_mock_context_managers_from_function(when_steps[0], config.mock_name_pattern)

        for ctx_manager in mock_context_managers:
            mock_func_name = ctx_manager.node.context_expr.func.id
            mock_var = ctx_manager.node.optional_vars
            if not is_self_attribute(mock_var):
                errors.append(MockCallResultNotSavedAsSelfAttribute(ctx_manager.lineno, ctx_manager.col_offset,
                                                                    mock_func_name=mock_func_name))
                continue

            if not is_self_attribute_asserted(assert_statements, mock_var):
                mock_var_name = '{}.{}'.format(mock_var.value.id, mock_var.attr)
                errors.append(MockCallResultNotAsserted(ctx_manager.lineno, ctx_manager.col_offset,
                                                        mock_var_name=mock_var_name))

        return errors
