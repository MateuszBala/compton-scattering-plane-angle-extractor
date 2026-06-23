# Python Testing Conventions

This document outlines the standards and conventions for testing Python code in the Compton Scattering Plane Angle Extractor project using pytest.

## Table of Contents

1. [General Principles](#general-principles)
2. [Test Organization](#test-organization)
3. [Test Structure (AAA Pattern)](#test-structure-aaa-pattern)
4. [Running Tests](#running-tests)
5. [Pytest Configuration](#pytest-configuration)
6. [Fixtures](#fixtures)
7. [Parametrized Tests](#parametrized-tests)
8. [Mocking](#mocking)
9. [Test Coverage](#test-coverage)
10. [Best Practices](#best-practices)
11. [Examples](#examples)

---

## General Principles

### Testing Philosophy

- **Every function must have tests** that cover the happy path and edge cases.
- **One test file per module**: If module is `angle_calculator.py`, test file is `test_angle_calculator.py`.
- **Test structure**: Use Arrange-Act-Assert (AAA) pattern for clarity.
- **Test naming**: Descriptive names that explain what is being tested.
- **Test independence**: Tests should not depend on each other.
- **Test speed**: Tests should run quickly (< 5 seconds for unit tests).

### Test Goals

- Verify functionality works correctly
- Catch regressions early
- Document expected behavior
- Enable safe refactoring
- Maintain high code quality

### Framework

- **Testing Framework**: pytest
- **Test Discovery**: Automatic (files named `test_*.py` or `*_test.py`)
- **Virtual Environment**: Use `uv` for project management
- **Coverage Tool**: pytest-cov for coverage reporting

---

## Test Organization

### Directory Structure

```
project/
├── src/
│   └── compton_scattering/
│       ├── angle_calculator.py
│       ├── data_loader.py
│       └── output_writer.py
└── tests/
    ├── unit/
    │   ├── test_angle_calculator.py
    │   ├── test_data_loader.py
    │   └── test_output_writer.py
    ├── integration/
    │   └── test_end_to_end.py
    └── conftest.py
```

### File Naming Convention

- **Unit tests**: `test_<module_name>.py`
- **Integration tests**: `test_<workflow_name>.py`
- **Test classes**: `Test<ClassName>` (PascalCase)
- **Test functions**: `test_<expected_behavior>` (snake_case)

**Examples:**
```python
# test_angle_calculator.py
class TestScatteringCalculator:
    def test_calculate_angle_returns_correct_value(self):
        pass

    def test_calculate_angle_handles_zero_magnitude_vector(self):
        pass

    def test_calculate_angle_raises_error_for_invalid_input(self):
        pass

def test_normalize_vector_returns_unit_vector():
    pass

def test_normalize_vector_raises_error_for_zero_vector():
    pass
```

### Test File Placement

```
tests/
├── unit/
│   ├── test_angle_calculator.py       # Tests for src/angle_calculator.py
│   ├── test_data_loader.py            # Tests for src/data_loader.py
│   └── test_cli.py                    # Tests for src/cli.py
├── integration/
│   └── test_end_to_end_analysis.py    # Tests full workflow
└── conftest.py                         # Shared fixtures
```

---

## Test Structure (AAA Pattern)

Every test follows the **Arrange-Act-Assert** (AAA) pattern:

### Pattern Structure

```python
def test_function_expected_behavior():
    # ARRANGE: Set up test data and preconditions
    input_data = ...
    expected_result = ...

    # ACT: Execute the function being tested
    actual_result = function_under_test(input_data)

    # ASSERT: Verify the results
    assert actual_result == expected_result
```

### Detailed Example

```python
import numpy as np
import pytest
from compton_scattering.angle_calculator import (
    calculate_scattering_angle,
    normalize_vector,
)


def test_calculate_scattering_angle_returns_correct_value():
    """Test scattering angle calculation for perpendicular vectors."""
    # ARRANGE
    initial_direction = np.array([1.0, 0.0, 0.0])
    final_direction = np.array([0.0, 1.0, 0.0])
    expected_angle = np.pi / 2  # 90 degrees

    # ACT
    actual_angle = calculate_scattering_angle(
        initial_direction,
        final_direction,
    )

    # ASSERT
    assert np.isclose(actual_angle, expected_angle)


def test_calculate_scattering_angle_handles_non_normalized_vectors():
    """Test that function handles vectors needing normalization."""
    # ARRANGE
    initial_direction = np.array([2.0, 0.0, 0.0])  # magnitude 2
    final_direction = np.array([0.0, 3.0, 0.0])    # magnitude 3
    expected_angle = np.pi / 2

    # ACT
    actual_angle = calculate_scattering_angle(
        initial_direction,
        final_direction,
    )

    # ASSERT
    assert np.isclose(actual_angle, expected_angle)


def test_calculate_scattering_angle_raises_error_for_zero_vector():
    """Test that function raises ValueError for zero-magnitude vector."""
    # ARRANGE
    initial_direction = np.array([1.0, 0.0, 0.0])
    zero_vector = np.array([0.0, 0.0, 0.0])

    # ACT & ASSERT
    with pytest.raises(ValueError, match="zero-magnitude"):
        calculate_scattering_angle(initial_direction, zero_vector)
```

### AAA Pattern Rules

1. **ARRANGE**: Set up everything needed
   - Create input data
   - Set expected results
   - Configure mocks if needed

2. **ACT**: Execute one action
   - Call the function being tested
   - Do not add logic here

3. **ASSERT**: Verify results
   - Check return value
   - Verify side effects
   - One conceptual assertion (can have multiple assert statements)

---

## Running Tests

### Basic Test Execution

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_angle_calculator.py

# Run specific test
pytest tests/unit/test_angle_calculator.py::test_calculate_scattering_angle_returns_correct_value

# Run tests matching pattern
pytest -k "scattering_angle"

# Run with verbose output
pytest -v

# Run and show print statements
pytest -s

# Run with coverage
pytest --cov=src --cov-report=html
```

### With UV (Project Manager)

```bash
# Install dependencies and setup
uv sync

# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=src

# Run specific test
uv run pytest tests/unit/test_angle_calculator.py
```

### Test Output

```
tests/unit/test_angle_calculator.py::test_calculate_angle_returns_correct_value PASSED
tests/unit/test_angle_calculator.py::test_calculate_angle_handles_zero_vector PASSED
tests/unit/test_angle_calculator.py::test_normalize_vector_returns_unit PASSED

====== 3 passed in 0.15s ======
```

---

## Pytest Configuration

### pytest.ini or pyproject.toml

```toml
[tool.pytest.ini_options]
# Minimum version
minversion = "7.0"

# Test discovery patterns
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

# Paths to search for tests
testpaths = ["tests"]

# Plugins
addopts = [
    "--verbose",
    "--strict-markers",
    "--tb=short",
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-report=html",
]

# Markers for test categorization
markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "slow: Slow tests",
    "skip: Skip test",
]
```

### .coveragerc for Coverage

```ini
[run]
source = src

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
    @abstractmethod

precision = 2

[html]
directory = htmlcov
```

---

## Fixtures

Fixtures provide reusable test setup.

### Basic Fixtures

```python
# tests/conftest.py
import pytest
import numpy as np


@pytest.fixture
def sample_vector() -> np.ndarray:
    """Provide a sample 3D vector for testing."""
    return np.array([1.0, 0.0, 0.0])


@pytest.fixture
def perpendicular_vectors() -> tuple[np.ndarray, np.ndarray]:
    """Provide two perpendicular vectors."""
    return (
        np.array([1.0, 0.0, 0.0]),
        np.array([0.0, 1.0, 0.0]),
    )


@pytest.fixture
def scattering_data() -> dict:
    """Provide sample scattering data."""
    return {
        'theta_a': 0.5,
        'phi_a': 1.0,
        'theta_b': 0.3,
        'phi_b': 0.8,
        'plane_angle': 0.2,
    }
```

### Using Fixtures

```python
def test_normalize_with_sample_vector(sample_vector):
    """Test normalization with fixture."""
    # Use the fixture
    result = normalize_vector(sample_vector)
    
    assert np.isclose(np.linalg.norm(result), 1.0)


def test_angle_calculation(perpendicular_vectors):
    """Test angle calculation with fixture."""
    v1, v2 = perpendicular_vectors
    
    angle = calculate_scattering_angle(v1, v2)
    
    assert np.isclose(angle, np.pi / 2)
```

### Fixture Scopes

```python
# Module scope (created once per module)
@pytest.fixture(scope="module")
def expensive_data_load():
    """Load data once for entire test module."""
    return load_large_dataset()

# Class scope (created once per test class)
@pytest.fixture(scope="class")
def test_calculator():
    """Create calculator for test class."""
    return ScatteringCalculator()

# Function scope (created for each test) - DEFAULT
@pytest.fixture(scope="function")
def fresh_data():
    """Create fresh data for each test."""
    return np.random.randn(100, 3)
```

---

## Parametrized Tests

Test multiple inputs with one test function.

### Basic Parametrization

```python
import pytest


@pytest.mark.parametrize(
    "initial,final,expected_angle",
    [
        (
            np.array([1, 0, 0]),
            np.array([1, 0, 0]),
            0.0,  # Same direction
        ),
        (
            np.array([1, 0, 0]),
            np.array([0, 1, 0]),
            np.pi / 2,  # Perpendicular
        ),
        (
            np.array([1, 0, 0]),
            np.array([-1, 0, 0]),
            np.pi,  # Opposite
        ),
    ],
)
def test_scattering_angle_multiple_cases(initial, final, expected_angle):
    """Test scattering angle for various vector configurations."""
    # ARRANGE
    initial_norm = initial / np.linalg.norm(initial)
    final_norm = final / np.linalg.norm(final)

    # ACT
    angle = calculate_scattering_angle(initial_norm, final_norm)

    # ASSERT
    assert np.isclose(angle, expected_angle)
```

### Indirect Parametrization

```python
@pytest.fixture
def angle_data(request):
    """Fixture that uses parametrization."""
    return request.param


@pytest.mark.parametrize(
    "angle_data",
    [
        {"theta": 0.5, "phi": 1.0},
        {"theta": 1.0, "phi": 0.5},
        {"theta": 2.0, "phi": 3.0},
    ],
    indirect=True,
)
def test_with_parametrized_fixture(angle_data):
    """Test using parametrized fixture."""
    assert angle_data["theta"] > 0
```

---

## Mocking

Mock external dependencies for isolated unit tests.

### Basic Mocking

```python
from unittest.mock import Mock, patch
import pytest


def test_load_data_with_mocked_file():
    """Test data loading with mocked file operations."""
    # ARRANGE
    mock_data = [1, 2, 3, 4, 5]
    
    with patch('pandas.read_csv') as mock_read:
        mock_read.return_value = mock_data
        
        # ACT
        result = load_data('fake_file.csv')
        
        # ASSERT
        assert result == mock_data
        mock_read.assert_called_once_with('fake_file.csv')


def test_api_call_with_mocked_request():
    """Test API calls with mocked requests."""
    # ARRANGE
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = {'result': 'success'}
        mock_get.return_value = mock_response
        
        # ACT
        result = call_api('https://api.example.com')
        
        # ASSERT
        assert result['result'] == 'success'
```

### When to Mock

**Use mocks for:**
- External APIs
- File I/O
- Database operations
- Time-dependent functions

**Don't mock:**
- Functions under test
- NumPy/Pandas operations
- Pure mathematical functions

---

## Test Coverage

### Coverage Goals

- **Minimum**: 80% overall coverage
- **Target**: 90%+ for critical functions
- **Edge cases**: 100% coverage for error paths

### Measuring Coverage

```bash
# Run tests with coverage
pytest --cov=src --cov-report=html

# Check coverage for specific module
pytest --cov=src.angle_calculator

# Show missing lines
pytest --cov=src --cov-report=term-missing
```

### Interpreting Coverage

```
src/angle_calculator.py           95    90    95    89   85%
src/data_loader.py               120    15    85    45   87%
src/output_writer.py              75    10    80    12   87%

TOTAL                            290    25    76    54   87%
```

### Coverage Report

```bash
# Generate HTML coverage report
pytest --cov=src --cov-report=html
# Open htmlcov/index.html in browser
```

---

## Best Practices

### 1. One Assertion Per Concept

```python
# Good: Each assertion tests one concept
def test_calculate_and_store_angle():
    """Test angle calculation and storage."""
    # ARRANGE
    calc = ScatteringCalculator()
    vectors = (np.array([1, 0, 0]), np.array([0, 1, 0]))
    
    # ACT
    angle = calc.calculate_angle(*vectors)
    
    # ASSERT - conceptually one idea: result is correct
    assert np.isclose(angle, np.pi / 2)
    assert angle in calc.cache.values()  # Still one concept: storage


# Bad: Multiple unrelated concepts
def test_everything():
    """Test multiple unrelated things."""
    calc = ScatteringCalculator()
    
    angle = calc.calculate_angle(v1, v2)
    assert angle == expected
    
    data = load_data('file.csv')
    assert data.shape == (100, 5)
    
    result = process_output(data)
    assert result is not None
```

### 2. Descriptive Test Names

```python
# Good: Name explains what is tested
def test_calculate_angle_returns_pi_over_2_for_perpendicular_vectors():
    pass

def test_normalize_raises_valueerror_for_zero_magnitude_vector():
    pass

def test_load_csv_with_missing_file_raises_filenotfounderror():
    pass

# Bad: Vague names
def test_angle():
    pass

def test_normalize():
    pass

def test_load():
    pass
```

### 3. Test Behavior, Not Implementation

```python
# Good: Tests the behavior
def test_vector_normalization_produces_unit_magnitude():
    """Test that normalized vector has magnitude 1."""
    vector = np.array([3, 4])
    normalized = normalize_vector(vector)
    
    assert np.isclose(np.linalg.norm(normalized), 1.0)

# Bad: Tests implementation details
def test_normalize_divides_by_norm():
    """Test that normalize divides by norm (implementation detail)."""
    # Should not test how it's done, just that it works
    pass
```

### 4. Use Appropriate Assertions

```python
# Good: Use specific assertions
assert result == expected_value
assert isinstance(result, np.ndarray)
assert result.shape == (3,)
assert np.allclose(result, expected_array, atol=1e-10)

# Use pytest helpers
assert result in expected_set
assert key in dictionary
assert "substring" in text

# For exceptions
with pytest.raises(ValueError, match="pattern"):
    function_that_raises()

# Bad: Generic assertions
assert result  # Too vague
assert True  # Always passes!
```

### 5. Avoid Test Interdependencies

```python
# Good: Each test is independent
def test_angle_1():
    """Test angle calculation."""
    angle = calculate_angle(v1, v2)
    assert angle == expected

def test_angle_2():
    """Test another angle calculation."""
    angle = calculate_angle(v3, v4)
    assert angle == expected

# Bad: Tests depend on execution order
global_data = None

def test_1_load_data():
    global global_data
    global_data = load_data()  # Depends on this running first
    assert global_data is not None

def test_2_process_data():
    result = process(global_data)  # Depends on test_1 running first!
    assert result is not None
```

### 6. Test Edge Cases

```python
def test_scattering_angle_edge_cases():
    """Test boundary conditions and edge cases."""
    # Same vector (angle = 0)
    v = np.array([1, 0, 0])
    assert np.isclose(calculate_angle(v, v), 0.0)
    
    # Opposite vectors (angle = π)
    assert np.isclose(
        calculate_angle(v, -v),
        np.pi,
    )
    
    # Very small magnitude (should raise)
    tiny_v = np.array([1e-11, 0, 0])
    with pytest.raises(ValueError):
        calculate_angle(v, tiny_v)
    
    # Very large magnitude (should still work)
    large_v = np.array([1e10, 0, 0])
    assert np.isclose(calculate_angle(v, large_v), 0.0)
```

---

## Examples

### Complete Test File Example

```python
"""
Unit tests for angle_calculator module.

Tests the calculation of scattering angles and plane angles
from momentum vectors.
"""

import numpy as np
import pytest
from compton_scattering.angle_calculator import (
    calculate_scattering_angle,
    normalize_vector,
    calculate_azimuthal_angle,
)


class TestNormalizeVector:
    """Test vector normalization function."""

    def test_normalize_produces_unit_vector(self):
        """Test that normalize returns vector with magnitude 1."""
        # ARRANGE
        vector = np.array([3.0, 4.0])  # magnitude 5

        # ACT
        normalized = normalize_vector(vector)

        # ASSERT
        assert np.isclose(np.linalg.norm(normalized), 1.0)

    def test_normalize_preserves_direction(self):
        """Test that normalization preserves vector direction."""
        # ARRANGE
        vector = np.array([3.0, 4.0, 0.0])

        # ACT
        normalized = normalize_vector(vector)

        # ASSERT
        # Direction preserved if cross product is zero
        assert np.allclose(np.cross(vector, normalized), 0)

    def test_normalize_raises_for_zero_magnitude(self):
        """Test that normalization raises ValueError for zero vector."""
        # ARRANGE
        zero_vector = np.array([0.0, 0.0, 0.0])

        # ACT & ASSERT
        with pytest.raises(ValueError, match="magnitude"):
            normalize_vector(zero_vector)


class TestScatteringAngle:
    """Test scattering angle calculation."""

    @pytest.mark.parametrize(
        "initial,final,expected",
        [
            (
                np.array([1, 0, 0]),
                np.array([1, 0, 0]),
                0.0,
            ),
            (
                np.array([1, 0, 0]),
                np.array([0, 1, 0]),
                np.pi / 2,
            ),
            (
                np.array([1, 0, 0]),
                np.array([-1, 0, 0]),
                np.pi,
            ),
        ],
    )
    def test_angle_for_standard_vectors(
        self,
        initial,
        final,
        expected,
    ):
        """Test scattering angle for standard vector pairs."""
        # ARRANGE
        initial_norm = initial / np.linalg.norm(initial)
        final_norm = final / np.linalg.norm(final)

        # ACT
        angle = calculate_scattering_angle(initial_norm, final_norm)

        # ASSERT
        assert np.isclose(angle, expected)

    def test_angle_handles_non_normalized_input(self):
        """Test that function handles non-normalized input vectors."""
        # ARRANGE
        initial = np.array([2.0, 0.0, 0.0])  # magnitude 2
        final = np.array([0.0, 3.0, 0.0])    # magnitude 3
        expected = np.pi / 2

        # ACT
        angle = calculate_scattering_angle(initial, final)

        # ASSERT
        assert np.isclose(angle, expected)

    def test_angle_raises_for_zero_vector(self):
        """Test that function raises ValueError for zero-magnitude input."""
        # ARRANGE
        valid_vector = np.array([1.0, 0.0, 0.0])
        zero_vector = np.array([0.0, 0.0, 0.0])

        # ACT & ASSERT
        with pytest.raises(ValueError):
            calculate_scattering_angle(valid_vector, zero_vector)
```

### Integration Test Example

```python
"""Integration tests for end-to-end scattering analysis."""

import numpy as np
import pandas as pd
import pytest
from compton_scattering.cli import main
from pathlib import Path


@pytest.fixture
def sample_scattering_data(tmp_path):
    """Create sample scattering data for integration tests."""
    data = pd.DataFrame({
        'k0_x': [1.0, 0.8, 0.9],
        'k0_y': [0.0, 0.6, 0.436],
        'k0_z': [0.0, 0.0, 0.0],
        'k_x': [0.9, 0.7, 0.8],
        'k_y': [0.436, 0.7, 0.6],
        'k_z': [0.0, 0.0, 0.0],
    })
    
    filepath = tmp_path / "data.csv"
    data.to_csv(filepath, index=False)
    
    return filepath


def test_end_to_end_analysis(sample_scattering_data, tmp_path):
    """Test complete analysis workflow."""
    # ARRANGE
    input_file = sample_scattering_data
    output_dir = tmp_path

    # ACT
    result = main(input_file, output_dir)

    # ASSERT
    assert result == 0
    
    # Check output file was created
    output_file = output_dir / "compton-scattering-plane-angles.csv"
    assert output_file.exists()
    
    # Check output has expected columns
    output_data = pd.read_csv(output_file)
    expected_columns = ['theta_a', 'phi_a', 'theta_b', 'phi_b', 'plane_angle']
    assert all(col in output_data.columns for col in expected_columns)
```

---

## Test Checklist

Before submitting tests, verify:

- [ ] One test file per module (`test_<module>.py`)
- [ ] Tests use AAA pattern (Arrange-Act-Assert)
- [ ] Test names describe expected behavior
- [ ] All public functions have tests
- [ ] Edge cases tested (boundaries, errors, etc.)
- [ ] Error cases tested (exceptions, invalid inputs)
- [ ] Tests are independent (no interdependencies)
- [ ] Fixtures used for common setup
- [ ] No hardcoded paths (use tmp_path fixture)
- [ ] Appropriate assertions (not just `assert True`)
- [ ] Coverage >= 80% (aim for 90%+)
- [ ] Tests run quickly (< 5 seconds total)
- [ ] No warnings when running tests
- [ ] All tests pass before submission
- [ ] Type hints present in test code
- [ ] Pytest configuration properly set up

---

## References

- [Pytest Documentation](https://docs.pytest.org/)
- [Python Testing Best Practices](https://docs.python-guide.org/writing/tests/)
- [AAA Pattern](https://arrange-act-assert.com/)

---

**Last Updated:** June 2026  
**Version:** 1.0