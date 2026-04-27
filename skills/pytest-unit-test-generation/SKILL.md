---
name: pytest-unit-test-generation
description: Generate comprehensive unit tests for Python source code with pytest. Covers test structure, fixtures, mocking, parametrization, and coverage patterns. Use when creating or modifying pytest unit tests.
---

# Unit Test Generation Skill

Generate comprehensive unit tests for Python source code with pytest.

## When to Use

This skill activates when:
- User asks for unit tests for a file or function
- User asks to create or modify unit tests
- Code needs test coverage
- User mentions "test", "coverage", "pytest", "unit test"
- After writing new code that needs testing

## Supported File Types

- Python modules (.py)
- Functions and classes
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
2. **Use descriptive test names** - `test_should_do_x` format
3. **Keep tests independent** - Each test can run in isolation
4. **Follow AAA pattern** - Arrange, Act, Assert
5. **Mock external dependencies** - Database, HTTP calls, file I/O
6. **Use fixtures** - Reusable test data via `@pytest.fixture`
7. **Parametrize when appropriate** - Multiple inputs with `@pytest.mark.parametrize`
8. **Aim for high branch coverage** - Test all code paths
9. **Use project ORM patterns** - For projects using an Object-Relational Mapping (ORM) library (Beanie, SQLAlchemy, Prisma, Hibernate, GORM, Sequelize, TypeORM, etc.), use ORM document/model classes and queries in tests to match project coding style

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