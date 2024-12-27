from flake8_plugin_utils import Error


class MockCallResultNotSavedAsSelfAttribute(Error):
    code = 'MCS001'
    message = 'result of "{mock_func_name}()" should be saved as "self" attribute for further assertion'


class MockCallResultNotAsserted(Error):
    code = 'MCS002'
    message = 'mock call result "{mock_var_name}" should be asserted in "then" or "and" or "but" step'
