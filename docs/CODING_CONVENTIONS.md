# Coding Conventions

This document outlines the coding standards and conventions for Python code and bash scripts in the Compton Scattering Plane Angle Extractor project. All code must conform to these guidelines.

## Table of Contents

1. [Language Standards](#language-standards)
2. [Python Coding Style](#python-coding-style)
3. [Type Hints](#type-hints)
4. [Naming Conventions](#naming-conventions)
5. [Code Organization](#code-organization)
6. [Bash Script Conventions](#bash-script-conventions)
7. [Tools and Analysis](#tools-and-analysis)
8. [Best Practices](#best-practices)
9. [Examples](#examples)

---

## Language Standards

### Python

- **Minimum Version**: Python 3.11
- **Maximum Versions Tested**: Python 3.14
- **Code Style**: PEP 8 compliant
- **Formatting Tool**: Ruff
- **Type Checking**: MyPy
- **Linting**: Ruff

### Bash Scripts

- **Shebang**: `#!/bin/bash`
- **Standard**: Bash 5.0+
- **Linting Tool**: ShellCheck
- **Formatting**: 2 spaces per indentation

---

## Python Coding Style

### PEP 8 Compliance

All Python code must follow PEP 8 with these specifics:

#### Indentation

- Use **4 spaces** per indentation level
- Never mix tabs and spaces
- Maximum line length: **88 characters** (Ruff default)

```python
# Good
def calculate_scattering_angle(
    initial_direction: np.ndarray,
    final_direction: np.ndarray,
) -> float:
    """Calculate scattering angle."""
    return np.arccos(np.dot(initial_direction, final_direction))

# Bad
def calculate_scattering_angle(initial_direction, final_direction):
    return np.arccos(np.dot(initial_direction, final_direction))
```

#### Line Length

- Maximum **88 characters** per line
- Break long lines logically
- Use implicit line continuation for readability

```python
# Good: Line continuation
result = (
    np.dot(vector_a, vector_b)
    + np.linalg.norm(vector_c)
    - scalar_value
)

# Good: Function call continuation
angle = compute_angle(
    initial_momentum=k0,
    final_momentum=k,
    scattering_plane=plane_a,
)

# Bad: Exceeds line limit
result = np.dot(vector_a, vector_b) + np.linalg.norm(vector_c) - scalar_value
```

#### Imports

Organize imports in this order:

1. Standard library imports
2. Third-party library imports
3. Local module imports

Separate groups with blank lines:

```python
# Standard library
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Optional

# Third-party
import numpy as np
import pandas as pd

# Local
from .angle_calculator import calculate_scattering_angle
from .data_loader import load_data
```

#### Blank Lines

- **Two blank lines** between top-level function/class definitions
- **One blank line** between method definitions inside a class
- Use blank lines sparingly within functions to organize logical sections

```python
class ScatteringCalculator:
    """Calculate scattering angles."""

    def __init__(self, plane_a: np.ndarray) -> None:
        """Initialize calculator."""
        self.plane_a = plane_a

    def calculate_angle(self, plane_b: np.ndarray) -> float:
        """Calculate plane angle."""
        return np.arccos(np.dot(self.plane_a, self.plane_b))


def process_data(data: pd.DataFrame) -> pd.DataFrame:
    """Process scattering data."""
    # processing logic
    return processed_data
```

#### Whitespace

```python
# Good: Spaces around operators
x = 1 + 2
result = value * scale
condition = a == b

# Good: Space after comma
items = [1, 2, 3]
function(arg1, arg2, arg3)

# Bad: No spaces
x=1+2
items=[1,2,3]

# Good: No space before function call
function(arg)

# Bad: Space before function call
function (arg)
```

---

## Type Hints

Type hints are **mandatory** for all function signatures and variable declarations.

### Function Type Hints

```python
def calculate_scattering_angle(
    initial_direction: np.ndarray,
    final_direction: np.ndarray,
) -> float:
    """
    Calculate angle between momentum vectors.

    Parameters
    ----------
    initial_direction : np.ndarray
        Initial momentum direction (shape: (3,)).
    final_direction : np.ndarray
        Final momentum direction (shape: (3,)).

    Returns
    -------
    float
        Scattering angle in radians.
    """
    return np.arccos(np.dot(initial_direction, final_direction))
```

### Optional and Union Types

```python
from typing import Optional, Union

# Optional parameters
def load_data(
    filepath: str,
    format: Optional[str] = None,
) -> pd.DataFrame:
    """Load data from file."""
    pass

# Union types
def process(
    data: Union[str, Path, pd.DataFrame],
) -> pd.DataFrame:
    """Process data from various sources."""
    pass
```

### Complex Type Hints

```python
from typing import Callable, Sequence

# Callable
processor: Callable[[np.ndarray], float] = calculate_angle

# Sequence
angles: Sequence[float] = [0.5, 1.0, 1.5]

# Generic types
def process_multiple(
    angles: list[float],
    weights: dict[str, float],
) -> tuple[float, float]:
    """Process angles with weights."""
    pass
```

### Generics for NumPy and Pandas

```python
import numpy as np
import pandas as pd

# NumPy arrays with type hints
def normalize_vector(vector: np.ndarray) -> np.ndarray:
    """Normalize vector to unit length."""
    return vector / np.linalg.norm(vector)

# Pandas DataFrames
def extract_columns(
    data: pd.DataFrame,
    columns: list[str],
) -> pd.DataFrame:
    """Extract specified columns."""
    return data[columns]
```

### MyPy Configuration

Ensure strict type checking with `.mypy.ini`:

```ini
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_incomplete_defs = True
check_untyped_defs = True
strict_optional = True
```

---

## Naming Conventions

### Module Names

- Lowercase with underscores
- Descriptive, concise names
- Match the functionality

```python
# Good module names
angle_calculator.py
data_loader.py
scattering_processor.py

# Bad
AngleCalculator.py
loader.py
proc.py
```

### Class Names

- **PascalCase** for all classes
- Descriptive, noun-based names
- No "Class" suffix

```python
# Good
class ScatteringCalculator:
    pass

class DataProcessor:
    pass

class AngleExtractor:
    pass

# Bad
class scattering_calculator:
    pass

class DataProcessorClass:
    pass
```

### Function and Method Names

- **snake_case** for all functions and methods
- Descriptive, verb-based names
- Use clear action verbs

```python
# Good
def calculate_scattering_angle():
    pass

def load_data_from_file():
    pass

def extract_momentum_vectors():
    pass

# Bad
def calc():
    pass

def load():
    pass

def process():
    pass
```

### Variable Names

- **snake_case** for all variables
- Descriptive names that indicate purpose
- Avoid single-letter names except in mathematical contexts

```python
# Good
scattering_angle = 0.5
initial_momentum = np.array([1, 0, 0])
plane_normal = compute_normal(plane)

# Bad
sa = 0.5
imp = np.array([1, 0, 0])
pn = compute_normal(plane)
x = 0.5  # ambiguous
```

### Constants

- **UPPERCASE_WITH_UNDERSCORES** for module-level constants
- Use `typing.Final` for type hints

```python
from typing import Final

# Module level
MAX_ITERATIONS: Final[int] = 1000
DEFAULT_OUTPUT_FORMAT: Final[str] = "csv"
PI: Final[float] = np.pi

# In classes
class Calculator:
    MAX_PRECISION: Final[int] = 10
    DEFAULT_TOLERANCE: Final[float] = 1e-6
```

### Private Members

- Prefix with single underscore for internal use
- No name mangling (double underscore) unless preventing collision

```python
class DataProcessor:
    """Process scattering data."""

    def __init__(self) -> None:
        """Initialize processor."""
        self._cache: dict[str, np.ndarray] = {}

    def _validate_input(self, data: np.ndarray) -> bool:
        """Validate input data (internal method)."""
        return data.shape == (3,)
```

---

## Code Organization

### Module Structure

```python
"""
Module for calculating Compton scattering angles.

This module provides functions to calculate scattering angles and
plane angles from momentum vectors.

Functions
---------
calculate_scattering_angle(initial, final) -> float
    Calculate angle between momentum vectors.
calculate_plane_angle(plane_a, plane_b) -> float
    Calculate angle between scattering planes.
"""

# Imports
import numpy as np
from typing import Optional

# Module constants
DEFAULT_TOLERANCE: float = 1e-10

# Classes
class ScatteringCalculator:
    """Calculate scattering angles from momentum vectors."""

    pass

# Functions
def calculate_scattering_angle(
    initial_direction: np.ndarray,
    final_direction: np.ndarray,
) -> float:
    """Calculate scattering angle."""
    pass

def calculate_plane_angle(
    plane_a: np.ndarray,
    plane_b: np.ndarray,
) -> float:
    """Calculate angle between planes."""
    pass

# Main execution
if __name__ == "__main__":
    # Run module as script
    pass
```

### Class Organization

```python
class ScatteringCalculator:
    """Calculate scattering angles from momentum vectors."""

    # Class constants
    DEFAULT_TOLERANCE: Final[float] = 1e-10

    def __init__(self, plane_normal: Optional[np.ndarray] = None) -> None:
        """Initialize calculator."""
        self._plane_normal = plane_normal
        self._cache: dict[str, float] = {}

    # Public methods
    def calculate_angle(self, vector_a: np.ndarray) -> float:
        """Calculate scattering angle."""
        return self._compute_angle(vector_a)

    # Private methods
    def _compute_angle(self, vector: np.ndarray) -> float:
        """Internal angle computation."""
        return np.arccos(np.dot(vector, self._plane_normal))

    # Magic methods
    def __repr__(self) -> str:
        """Return string representation."""
        return f"ScatteringCalculator(tolerance={self.DEFAULT_TOLERANCE})"
```

---

## Bash Script Conventions

Bash scripts follow conventions from the project's SCRIPTING_CONVENTIONS document with Python-specific integration:

### Python Integration in Bash

```bash
#!/bin/bash
# FILE: run_analysis.sh
#
# ABOUT: Run Compton scattering angle analysis on input data.
#
# ARGUMENTS:
#   --input-file : Path to input CSV/HDF5 file
#   --output-dir : Directory for output files
#
# USAGE:
#   bash run_analysis.sh --input-file data.csv --output-dir results

set -euo pipefail

INPUT_FILE=""
OUTPUT_DIR=""

function parse_arguments() {
  while [[ $# -gt 0 ]]; do
    case $1 in
      --input-file)
        INPUT_FILE="$2"
        shift 2
        ;;
      --output-dir)
        OUTPUT_DIR="$2"
        shift 2
        ;;
      *)
        echo "Error: Unknown argument: $1" >&2
        exit 1
        ;;
    esac
  done
}

function main() {
  parse_arguments "$@"

  # Run Python analysis
  python -m compton_scattering.cli \
    --input-file "${INPUT_FILE}" \
    --output-dir "${OUTPUT_DIR}"
}

main "$@"
```

---

## Tools and Analysis

### Ruff Configuration

Create `pyproject.toml` with Ruff settings:

```toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # Pyflakes
    "I",      # isort
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "UP",     # pyupgrade
]

[tool.ruff.format]
line-length = 88
```

### Running Ruff

```bash
# Format code
ruff format .

# Check code style
ruff check .

# Check and fix
ruff check --fix .
```

### MyPy Configuration

Create `.mypy.ini`:

```ini
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_incomplete_defs = True
check_untyped_defs = True
strict_optional = True

[mypy-numpy.*]
ignore_missing_imports = True

[mypy-pandas.*]
ignore_missing_imports = True
```

### Running MyPy

```bash
# Type check entire project
mypy src/

# Type check specific file
mypy src/angle_calculator.py

# Show error statistics
mypy src/ --stats
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Format with Ruff
ruff format .

# Check with Ruff
ruff check . || exit 1

# Type check with MyPy
mypy src/ || exit 1

# Lint bash scripts
shellcheck scripts/*.sh || exit 1
```

---

## Best Practices

### 1. Clear and Self-Documenting Code

```python
# Good: Self-explanatory variable names and clear logic
def calculate_azimuthal_angle(
    vector: np.ndarray,
    plane_normal: np.ndarray,
) -> float:
    """Calculate azimuthal angle in scattering plane."""
    return np.arctan2(
        np.dot(vector, perp_component),
        np.dot(vector, parallel_component),
    )

# Bad: Unclear logic
def calc(v, n):
    return np.arctan2(np.dot(v, x), np.dot(v, y))
```

### 2. Avoid Magic Numbers

```python
# Good: Use named constants
MIN_MAGNITUDE: Final[float] = 1e-10
ANGLE_RANGE_LOWER: Final[float] = 0.0
ANGLE_RANGE_UPPER: Final[float] = np.pi

if magnitude < MIN_MAGNITUDE:
    raise ValueError("Vector magnitude too small")

# Bad: Magic numbers in code
if magnitude < 1e-10:
    raise ValueError("Vector magnitude too small")
```

### 3. Use List and Dict Comprehensions

```python
# Good: Concise comprehensions
angles = [
    calculate_angle(v) for v in vectors
    if validate_vector(v)
]

mapping = {
    name: compute_value(name) for name in names
}

# Bad: Verbose loop
angles = []
for v in vectors:
    if validate_vector(v):
        angles.append(calculate_angle(v))
```

### 4. Use NumPy Vectorization

```python
# Good: Vectorized operations
def normalize_vectors(vectors: np.ndarray) -> np.ndarray:
    """Normalize vectors to unit length."""
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    return vectors / norms

# Bad: Python loop
def normalize_vectors(vectors):
    normalized = []
    for v in vectors:
        norm = np.linalg.norm(v)
        normalized.append(v / norm)
    return np.array(normalized)
```

### 5. Error Handling

```python
# Good: Specific exceptions
def load_data(filepath: str) -> pd.DataFrame:
    """Load data from file."""
    try:
        if not Path(filepath).exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        return pd.read_csv(filepath)
    except pd.errors.ParserError as e:
        raise ValueError(f"Invalid CSV format: {e}") from e

# Bad: Bare except
def load_data(filepath):
    try:
        return pd.read_csv(filepath)
    except:
        print("Error")
```

---

## Examples

### Good Python Code Example

```python
"""
Calculate scattering angles from momentum vectors.

This module provides functions to compute angles in Compton scattering
using plane geometry methods.

Functions
---------
calculate_scattering_angle(initial, final) -> float
    Calculate angle between momentum vectors.
normalize_vector(vector) -> np.ndarray
    Normalize vector to unit length.
"""

import numpy as np
from typing import Final

# Module constants
DEFAULT_TOLERANCE: Final[float] = 1e-10
VECTOR_DIMENSION: Final[int] = 3


def normalize_vector(vector: np.ndarray) -> np.ndarray:
    """
    Normalize vector to unit length.

    Parameters
    ----------
    vector : np.ndarray
        Input vector of any length.

    Returns
    -------
    np.ndarray
        Unit vector in same direction.

    Raises
    ------
    ValueError
        If vector magnitude is near zero.

    Examples
    --------
    >>> vector = np.array([3, 4])
    >>> normalized = normalize_vector(vector)
    >>> np.allclose(np.linalg.norm(normalized), 1.0)
    True
    """
    magnitude = np.linalg.norm(vector)
    if magnitude < DEFAULT_TOLERANCE:
        raise ValueError("Vector magnitude too small to normalize")
    return vector / magnitude


def calculate_scattering_angle(
    initial_direction: np.ndarray,
    final_direction: np.ndarray,
) -> float:
    """
    Calculate scattering angle between momentum vectors.

    The angle is computed as arccos(k0 · k) where k0 and k are
    unit vectors representing initial and final momentum directions.

    Parameters
    ----------
    initial_direction : np.ndarray
        Initial momentum direction (shape: (3,)).
    final_direction : np.ndarray
        Final momentum direction (shape: (3,)).

    Returns
    -------
    float
        Scattering angle in radians [0, π].

    Raises
    ------
    ValueError
        If input vectors have invalid magnitude.

    Examples
    --------
    >>> k0 = np.array([1, 0, 0])
    >>> k = np.array([0, 1, 0])
    >>> angle = calculate_scattering_angle(k0, k)
    >>> np.isclose(angle, np.pi / 2)
    True
    """
    k0_normalized = normalize_vector(initial_direction)
    k_normalized = normalize_vector(final_direction)
    
    cos_angle = np.dot(k0_normalized, k_normalized)
    # Clamp to [-1, 1] to handle numerical errors
    cos_angle = np.clip(cos_angle, -1.0, 1.0)
    
    return np.arccos(cos_angle)
```

### Bad Python Code Example

```python
# Bad: No module docstring
import numpy as np

# Bad: Magic number, unclear variable names
def calc(k0, k):
    mag1 = np.linalg.norm(k0)
    mag2 = np.linalg.norm(k)
    k0_n = k0 / mag1  # Unclear abbreviation
    k_n = k / mag2
    result = np.dot(k0_n, k_n)
    return np.arccos(result)  # No error handling
```

---

## Code Review Checklist

Before submitting code, verify:

- [ ] PEP 8 compliant (checked with Ruff)
- [ ] All functions have type hints
- [ ] All functions have docstrings (numpy style)
- [ ] Module has header docstring listing public functions
- [ ] No magic numbers (use named constants)
- [ ] Clear variable names
- [ ] Proper error handling with specific exceptions
- [ ] NumPy used for vector operations (not loops)
- [ ] Pandas used for data manipulation
- [ ] MyPy passes with no type errors
- [ ] Ruff format and lint checks pass
- [ ] ShellCheck passes for bash scripts
- [ ] No bare except clauses
- [ ] No logging print() statements (use logging module)

---

## References

- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [NumPy Docstring Style](https://numpydoc.readthedocs.io/en/latest/format.html)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [MyPy Documentation](https://mypy.readthedocs.io/)

---

**Last Updated:** June 2026  
**Version:** 1.0