from flake8_plugin_utils import assert_error, assert_not_error

from flake8_vedro_mocks.config import DefaultConfig
from flake8_vedro_mocks.errors import (
    MockCallResultNotAsserted,
    MockCallResultNotSavedAsSelfAttribute
)
from flake8_vedro_mocks.visitors import MockAssertChecker, ScenarioVisitor


def test_context_manager_mock_result_not_saved():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_steps_checker(MockAssertChecker)
    code = """
        class Scenario(vedro.Scenario):
            def given(self): pass
            def when(self):
                with mocked_hotel(): pass
            def then(self): pass
        """
    assert_error(ScenarioVisitor, code, MockCallResultNotSavedAsSelfAttribute,
                 mock_func_name='mocked_hotel', config=DefaultConfig())


def test_other_context_manager_result_not_saved():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_steps_checker(MockAssertChecker)
    code = """
        class Scenario(vedro.Scenario):
            def given(self): pass
            def when(self):
                with hotel_stub(): pass
            def then(self): pass
        """
    assert_not_error(ScenarioVisitor, code, config=DefaultConfig())


def test_context_manager_grpc_mock_result_not_saved():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_steps_checker(MockAssertChecker)
    code = """
        class Scenario(vedro.Scenario):
            def given(self): pass
            def when(self):
                with mocked_hotel_grpc(): pass
            def then(self): pass
        """
    assert_not_error(ScenarioVisitor, code, config=DefaultConfig())


def test_context_manager_mock_result_not_saved_when_custom_mock_name_pattern():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_steps_checker(MockAssertChecker)
    code = """
        class Scenario(vedro.Scenario):
            def given(self): pass
            def when(self):
                with hotel_stub(): pass
            def then(self): pass
        """
    assert_error(ScenarioVisitor, code, MockCallResultNotSavedAsSelfAttribute,
                 mock_func_name='hotel_stub', config=DefaultConfig(mock_name_pattern=r"(?=.*stub)"))


def test_nested_context_manager_mock_result_not_saved():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_steps_checker(MockAssertChecker)
    code = """
        class Scenario(vedro.Scenario):
            def given(self): pass
            def when(self):
                with mocked_hotel() as self.hotel_mock:
                    with mocked_offers(): pass
            def then(self):
                assert self.hotel_mock
        """
    assert_error(ScenarioVisitor, code, MockCallResultNotSavedAsSelfAttribute,
                 mock_func_name='mocked_offers', config=DefaultConfig())


def test_enumerated_context_manager_mock_result_not_saved():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_steps_checker(MockAssertChecker)
    code = """
        class Scenario(vedro.Scenario):
            def given(self): pass
            def when(self):
                with (
                         mocked_hotel() as self.hotel_mock,
                         mocked_offers()
                     ): pass
            def then(self):
                assert self.hotel_mock
        """
    assert_error(ScenarioVisitor, code, MockCallResultNotSavedAsSelfAttribute,
                 mock_func_name='mocked_offers', config=DefaultConfig())


def test_context_manager_mock_result_saved_as_func_var():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_steps_checker(MockAssertChecker)
    code = """
        class Scenario(vedro.Scenario):
            def given(self): pass
            def when(self):
                with mocked_hotel() as hotel_mock: pass
            def then(self): pass
        """
    assert_error(ScenarioVisitor, code, MockCallResultNotSavedAsSelfAttribute,
                 mock_func_name='mocked_hotel', config=DefaultConfig())


def test_context_manager_mock_result_saved_as_other_object_attribute():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_steps_checker(MockAssertChecker)
    code = """
        class Scenario(vedro.Scenario):
            def given(self): pass
            def when(self):
                with mocked_hotel() as some_instance.hotel_mock: pass
            def then(self): pass
        """
    assert_error(ScenarioVisitor, code, MockCallResultNotSavedAsSelfAttribute,
                 mock_func_name='mocked_hotel', config=DefaultConfig())


def test_context_manager_mock_result_saved_as_nested_self_attribute():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_steps_checker(MockAssertChecker)
    code = """
        class Scenario(vedro.Scenario):
            def given(self): pass
            def when(self):
                with mocked_hotel() as self.mocks.hotel_mock: pass
            def then(self): pass
        """
    assert_error(ScenarioVisitor, code, MockCallResultNotSavedAsSelfAttribute, mock_func_name='mocked_hotel',
                 config=DefaultConfig())


def test_context_manager_mock_result_saved_as_self_attribute_but_not_asserted():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_steps_checker(MockAssertChecker)
    code = """
        class Scenario(vedro.Scenario):
            def given(self): pass
            def when(self):
                with mocked_hotel() as self.hotel_mock: pass
            def then(self): pass
        """
    assert_error(ScenarioVisitor, code, MockCallResultNotAsserted,
                 mock_var_name='self.hotel_mock', config=DefaultConfig())


def test_nested_context_manager_mock_result_saved_as_self_attribute_but_not_asserted():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_steps_checker(MockAssertChecker)
    code = """
        class Scenario(vedro.Scenario):
            def given(self): pass
            def when(self):
                with mocked_hotel() as self.hotel_mock:
                    with mocked_offers() as self.offers_mock: pass
            def then(self):
                assert self.hotel_mock
        """
    assert_error(ScenarioVisitor, code, MockCallResultNotAsserted,
                 mock_var_name='self.offers_mock', config=DefaultConfig())


def test_enumerated_context_manager_mock_result_saved_as_self_attribute_but_not_asserted():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_steps_checker(MockAssertChecker)
    code = """
        class Scenario(vedro.Scenario):
            def given(self): pass
            def when(self):
                with (
                         mocked_hotel() as self.hotel_mock,
                         mocked_offers() as self.offers_mock
                     ): pass
            def then(self):
                assert self.hotel_mock
        """
    assert_error(ScenarioVisitor, code, MockCallResultNotAsserted,
                 mock_var_name='self.offers_mock', config=DefaultConfig())


def test_async_context_manager_mock_result_saved_as_self_attribute_and_asserted_in_then_step():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_steps_checker(MockAssertChecker)
    code = """
        class Scenario(vedro.Scenario):
            def given(self): pass
            async def when(self):
                async with mocked_hotel() as self.hotel_mock: pass
            def then(self):
                assert self.hotel_mock
        """
    assert_not_error(ScenarioVisitor, code, config=DefaultConfig())


def test_context_manager_mock_result_saved_as_self_attribute_and_asserted_in_and_step():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_steps_checker(MockAssertChecker)
    code = """
        class Scenario(vedro.Scenario):
            def given(self): pass
            def when(self):
                with mocked_hotel() as self.hotel_mock: pass
            def then(self): pass
            def and_(self):
                assert self.hotel_mock
        """
    assert_not_error(ScenarioVisitor, code, config=DefaultConfig())


def test_context_manager_mock_result_saved_as_self_attribute_and_asserted_in_but_step():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_steps_checker(MockAssertChecker)
    code = """
        class Scenario(vedro.Scenario):
            def given(self): pass
            def when(self):
                with mocked_hotel() as self.hotel_mock: pass
            def then(self): pass
            def and_(self): pass
            def but(self):
                assert self.hotel_mock
        """
    assert_not_error(ScenarioVisitor, code, config=DefaultConfig())


def test_context_manager_mock_result_saved_as_self_attribute_and_its_own_attribute_asserted():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_steps_checker(MockAssertChecker)
    code = """
        class Scenario(vedro.Scenario):
            def given(self): pass
            def when(self):
                with mocked_hotel() as self.hotel_mock: pass
            def then(self):
                assert self.hotel_mock.history[0] == {}
        """
    assert_not_error(ScenarioVisitor, code, config=DefaultConfig())


def test_context_manager_mock_result_saved_as_self_attribute_and_asserted_with_function():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_steps_checker(MockAssertChecker)
    code = """
        class Scenario(vedro.Scenario):
            def given(self): pass
            def when(self):
                with mocked_hotel() as self.hotel_mock: pass
            def then(self):
                assert len(self.hotel_mock) == 1
        """
    assert_not_error(ScenarioVisitor, code, config=DefaultConfig())


def test_context_manager_mock_result_saved_as_self_attribute_and_asserted_in_loop():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_steps_checker(MockAssertChecker)
    code = """
        class Scenario(vedro.Scenario):
            def given(self): pass
            def when(self):
                with mocked_hotel() as self.hotel_mock: pass
            def then(self):
                for i in range(2):
                    assert self.hotel_mock
        """
    assert_not_error(ScenarioVisitor, code, config=DefaultConfig())


def test_persistent_mock_result_not_saved():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_steps_checker(MockAssertChecker)
    code = """
        class Scenario(vedro.Scenario):
            def given(self): pass
            def when(self):
                mocked_hotel_persistent()
            def then(self): pass
        """
    assert_not_error(ScenarioVisitor, code, config=DefaultConfig())


def test_persistent_mock_result_saved_as_self_attribute_but_not_asserted():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_steps_checker(MockAssertChecker)
    code = """
        class Scenario(vedro.Scenario):
            def given(self): pass
            def when(self):
                self.hotel_mock = mocked_hotel_persistent()
            def then(self): pass
        """
    assert_not_error(ScenarioVisitor, code, config=DefaultConfig())
