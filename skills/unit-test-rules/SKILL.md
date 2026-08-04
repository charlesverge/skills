---
name: unit-test-rules
description: Generate unit tests for source code with. Covers test structure, fixtures, mocking, parametrization, and coverage patterns. Use when creating or modifying pytest unit tests.
---

# Unit Test Generation Skill

Generate unit tests.

## When to Use

This skill activates when:

- When a unit test to be modified, created or added
- When planning for a unit test to be modified, created or added
- User asks for unit tests for a file or function
- User asks to create or modify unit tests
- Code needs test coverage
- User mentions "test", "coverage", "pytest", "unit test", "jest", "playright", "mocha", "jasmine", "karma", "unittest", "test case", "test suite"
- After writing new code that needs testing

## Supported File Types

- Module, Functions and classes
- Utility functions
- API routes and handlers
- Database models and repositories

## Test Generation Process

### Analyze the source file

- Identify exported functions, classes, methods
- Map conditional branches and logic paths
- Note dependencies and imports
- Identify edge cases (empty, null, boundary)

### Generate test cases

**Happy path scenarios:**

- Test normal operation with typical inputs
- Test default parameter values
- Test successful state transitions

**Edge cases:**

- Empty inputs (empty string, empty list, None)
- Boundary values (max/min integers, empty collections)
- Single element collections
- Duplicate handling

**Error handling:**

- Invalid inputs raise appropriate exceptions
- Missing required parameters
- Type errors
- Value errors

**Regression tests:**

- Tests for previously reported bugs

## Test File Template

```python
import pytest
from module_under_test import FunctionName, ClassName


class TestFunctionName:
    """Tests for function_name."""

    def test_happy_path(self):
        """Should return expected result with valid input."""
        result = FunctionName(input_value)
        assert result == expected

    def test_edge_case_empty(self):
        """Should handle empty input gracefully."""
        result = FunctionName("")
        assert result == expected_empty

    def test_edge_case_none(self):
        """Should handle None input gracefully."""
        result = FunctionName(None)
        assert result == expected_default

    def test_invalid_input_raises_error(self):
        """Should raise ValueError for invalid input."""
        with pytest.raises(ValueError, match="expected error message"):
            FunctionName(invalid_value)


class TestClassName:
    """Tests for ClassName."""

    def test_init_with_defaults(self):
        """Should initialize with default values."""
        instance = ClassName()
        assert instance.attribute == default_value

    def test_init_with_custom_values(self):
        """Should initialize with provided values."""
        instance = ClassName(attr=value)
        assert instance.attribute == value

    def test_method_returns_expected(self):
        """Should return expected result from method."""
        instance = ClassName()
        result = instance.method()
        assert result == expected

    def test_method_with_param(self):
        """Should handle parameter correctly."""
        instance = ClassName()
        result = instance.method(param)
        assert result == expected


class TestClassNameEdgeCases:
    """Edge case tests for ClassName."""

    def test_handles_empty_collection(self):
        """Should handle empty collection."""
        instance = ClassName(items=[])
        assert instance.method() == expected

    def test_handles_none_value(self):
        """Should handle None value."""
        instance = ClassName(value=None)
        assert instance.method() == expected
```

## Best Practices

1. **Test behavior, not implementation** - Focus on public interfaces
1. **Use descriptive test names** - `test_should_do_x` format
1. **Keep tests independent** - Each test can run in isolation
1. **Follow AAA pattern** - Arrange, Act, Assert
1. **Mock external dependencies** - Database, HTTP calls, file I/O
1. **Use fixtures** - Reusable test data via `@pytest.fixture`
1. **Parametrize when appropriate** - Multiple inputs with `@pytest.mark.parametrize`
1. **Aim for high branch coverage** - Test all code paths
1. **Use project ORM patterns** - For projects using an Object-Relational Mapping (ORM) library (Beanie, SQLAlchemy, Prisma, Hibernate, GORM, Sequelize, TypeORM, etc.), use ORM document/model classes and queries in tests to match project coding style
1. **Use pytest temporary files** - Use tmp\_path directly in test arguments for single-test isolation. Use tmp\_path\_factory.mktemp() inside a session-scoped fixture for shared test assets.
1. **Static fixtures are files**: Static fixtures should be stored in a fixtures directory and should not be generated dynamically in the test. Use `tmp_path` for temporary files that are generated during the test that have dynamic content.

### Test design: avoid reproducing production behavior in tests

Tests must not reimplement production workflows, state machines, dispatch logic, retry behavior, lifecycle management, or component coordination inside test doubles.

#### Required approach

- Test one responsibility at a time.
- Replace only the immediate dependency boundary of the unit under test.
- Configure the minimum return value, exception, or observable effect required by the scenario.
- Assert externally observable behavior such as calls, arguments, ordering, state changes, outputs, and persisted results.
- Keep orchestration tests separate from component implementation tests.
- Test behavior in the component that owns that behavior.

#### Prohibited patterns

Do not create test helpers that:

- reproduce production branching or decision logic;
- dispatch behavior based on roles, stages, modes, commands, or operation types;
- duplicate retry loops, state transitions, workflow sequencing, or lifecycle handling;
- simulate several production components in one object;
- create production-like artifacts solely to advance a simulated workflow;
- maintain mutable scenario state only to imitate successive production steps;
- act as an alternate implementation of a production service, executor, controller, dispatcher, or orchestrator.

Examples of problematic patterns include:

```python
class FakeWorkflow:
  def run(self, stage: str) -> Result:
    if stage == "prepare":
      ...
    elif stage == "execute":
      ...
    elif stage == "verify":
      ...
```

```python
def fake_dispatch(command: str) -> Response:
  if command == "create":
    ...
  elif command == "update":
    ...
  elif command == "delete":
    ...
```

These helpers duplicate production behavior and can drift independently from the code under test.

#### Preferred orchestration-test pattern

For orchestration code, replace delegated operations directly and assert their order and inputs:

```python
actions = Mock()

prepare = Mock(return_value=PrepareResult(success=True))
execute = Mock(return_value=ExecuteResult(success=True))
verify = Mock(return_value=VerifyResult(success=True))

actions.attach_mock(prepare, "prepare")
actions.attach_mock(execute, "execute")
actions.attach_mock(verify, "verify")

monkeypatch.setattr(subject, "prepare", prepare)
monkeypatch.setattr(subject, "execute", execute)
monkeypatch.setattr(subject, "verify", verify)

subject.run()

assert actions.mock_calls == [
  call.prepare(),
  call.execute(),
  call.verify(),
]
```

The test should verify the orchestration contract without reproducing the implementation of the delegated operations.

#### Preferred component-test pattern

Test each delegated component separately:

- orchestration tests verify which operations are called and in what order;
- component tests verify the behavior of each operation;
- integration tests verify that real components work together;
- infrastructure tests verify persistence, network, process, queue, or filesystem boundaries;
- instrumentation tests verify logging, metrics, tracing, and reporting in the component that emits them.

Do not combine all of these responsibilities into one test unless the test is explicitly an integration or end-to-end test.

#### Stateful test doubles

Stateful test doubles should not be the default.

A stateful double is permitted only when:

- the dependency itself has an inherently stateful contract;
- state transitions are relevant to the behavior being tested;
- using the real implementation is impractical;
- a simple mock, stub, fixed response sequence, or direct method replacement is insufficient;
- the double does not reproduce the unit under test’s control flow.

Examples that may justify a stateful double include:

- an in-memory repository implementing a documented storage contract;
- a protocol simulator whose connection state is part of the tested behavior;
- a queue or clock abstraction whose state is directly observable;
- a transactional resource used across several operations.

When a stateful double is used, it must:

- have a name that identifies it as a fake, stub, or spy;
- implement the smallest possible contract;
- reject unsupported operations;
- remain deterministic;
- expose explicit state rather than hidden counters or implicit transitions;
- be covered by contract tests when it is shared or nontrivial;
- document why a simpler test boundary was insufficient.

#### Test-boundary rule

Patch at the highest boundary that still preserves the behavior under test.

- If testing orchestration, patch delegated methods.
- If testing a component, patch its external dependencies.
- If testing integration, use real components and replace only external infrastructure.
- If testing end-to-end behavior, avoid replacing internal application components.

The test must not patch below the relevant boundary and then reconstruct the missing production behavior inside the test.

# Unit test setup

1. Identify unit tests which have repeating setup requirements and create fixtures for them. Use `@pytest.fixture` to create reusable test data or objects or pre defined functions

## Resolving test failures

1. Examine if the application code has changed since the tests where generated. Verify if the failure is a unit test failure that is not in line with the application code or the application code is not meeting the expected behavior.
1. When modifying a test, ensure that it remains as strong as it was before the test. If an attribute has been renamed, don't simply delete the assertion. Update the unit test.

## Test Organization

```
tests/
├── __init__.py
├── conftest.py          # Shared fixtures
├── test_module_a.py    # Tests for module_a
├── test_module_b.py    # Tests for module_b
└── utils.py           # Test utilities
```

## Common Fixtures

```python
# conftest.py
import pytest
from module_under_test import create_app


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def sample_data():
    return {"key": "value"}
```

## Temporary file fixtures

```python
def test_isolated_file(tmp_path):
    file_path = tmp_path / "data.txt"
    file_path.write_text("hello")
    assert file_path.read_text() == "hello"

@pytest.fixture(scope="session")
def shared_dataset(tmp_path_factory):
    # Base directory lasts for the whole test session
    base_dir = tmp_path_factory.mktemp("data_folder")
    data_file = base_dir / "large_dataset.csv"
    data_file.write_text("id,value\n1,100")
    return data_file

def test_use_case_one(shared_dataset):
    assert shared_dataset.exists()
```

## Manual unit tests

To handle multiple features at once and run all manual tests if no specific feature is passed, you can change the logic to split comma-separated strings into a list.
Here is how to update your setup to support commands like pytest --run-manual (runs all manual tests) or pytest --run-manual login,checkout (runs only those specific manual tests).

## 📑 1. Update your conftest.py

This updated code parses your input into a list of features. It also changes the logic so that regular automated tests are only skipped if you are explicitly focusing on manual tests.

```python
import pytest
def pytest_addoption(parser):
    # This can now be used as a flag on its own, OR with text
    parser.addoption(
        "--run-manual",
        action="store",
        nargs="?",
        const="all",
        default=None,
        help="Run manual tests. Provide features split by commas (e.g., --run-manual login,checkout)",
    )
def pytest_configure(config):
    # Register the manual marker
    config.addinivalue_line(
        "markers", "manual(feature): mark test as manual for a specific feature"
    )
def pytest_collection_modifyitems(config, items):
    # Get the raw option input
    raw_option = config.getoption("--run-manual")

    # Case 1: The user did NOT provide the --run-manual flag at all.
    # Skip all manual tests, keep automated tests.
    if raw_option is None:
        skip_manual = pytest.mark.skip(reason="Manual test. Use --run-manual to run.")
        for item in items:
            if "manual" in item.keywords:
                item.add_marker(skip_manual)
        return

    # Case 2: The user provided the flag.
    # Create a list of target features. If it's "all", the list stays empty.
    target_features = []
    if raw_option != "all":
        # Split "login,checkout" into ["login", "checkout"] and strip extra spaces
        target_features = [f.strip() for f in raw_option.split(",")]

    for item in items:
        manual_marker = item.get_closest_marker("manual")

        if manual_marker:
            # Get the feature assigned to the test mark
            marker_feature = manual_marker.args[0] if manual_marker.args else None

            # If targeting specific features, skip this test if it doesn't match
            if target_features and marker_feature not in target_features:
                item.add_marker(pytest.mark.skip(
                    reason=f"Manual test for '{marker_feature}' skipped. Targets: {target_features}"
                ))
        else:
            # Since we are running manual tests, skip the normal automated tests
            item.add_marker(pytest.mark.skip(reason="Running manual test mode only"))

## 📑 2. Your Test Code Example
You can mark your tests with single feature names. You can also leave a manual test blank if it does not belong to a specific feature.

import pytest
# Regular automated testdef test_automated_billing():
    assert True
# Manual test for login
@pytest.mark.manual("login")def test_manual_login():
    print("Verify login captcha")
    assert True
# Manual test for checkout
@pytest.mark.manual("checkout")def test_manual_checkout():
    print("Swipe physical test card")
    assert True
# Manual test for claude
@pytest.mark.manual("claude")def test_manual_claude_integration():
    print("Check Claude API response streaming")
    assert True
# General manual test with no specific feature
@pytest.mark.manualdef test_general_manual_check():
    print("General visual check of the landing page")
    assert True

## 📑 3. Run the Tests via CLI
```

- To run regular automated tests only (skips all manual tests):

pytest

- To run ALL manual tests (and skip normal automated ones):

pytest --run-manual

- To run specific manual features (e.g., login and claude):

pytest --run-manual login,claude

(This will run `test_manual_login` and `test_manual_claude_integration`, but will skip everything else). \[1, 2]
