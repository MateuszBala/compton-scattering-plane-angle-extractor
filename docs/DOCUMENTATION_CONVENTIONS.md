# Python Documentation Conventions

This document outlines the standards for documenting Python code and project documentation in the Compton Scattering Plane Angle Extractor project.

## Table of Contents

1. [General Principles](#general-principles)
2. [Module Documentation](#module-documentation)
3. [Class Documentation](#class-documentation)
4. [Function and Method Documentation](#function-and-method-documentation)
5. [Docstring Style](#docstring-style)
6. [Code Examples](#code-examples)
7. [Project Documentation](#project-documentation)
8. [Best Practices](#best-practices)

---

## General Principles

### Documentation Standards

- **Every public module, class, function, and method must have a docstring**.
- **Docstrings are mandatory** and checked during code review.
- Use **NumPy docstring style** for consistency and clarity.
- Documentation should explain **what** and **why**, not just **how**.
- Examples should be practical and tested.
- Keep documentation close to code for easy updates.

### Docstring Format

All docstrings use **NumPy style** with these sections:

1. **Summary** (1-2 sentences)
2. **Extended Description** (optional, paragraph)
3. **Parameters** (for functions/methods)
4. **Attributes** (for classes)
5. **Returns** (for functions/methods)
6. **Raises** (optional, for exceptions)
7. **Examples** (practical code examples)
8. **Notes** (optional, important information)
9. **References** (optional, related documentation)

---

## Module Documentation

### Module Header Docstring

Every module must start with a docstring describing its purpose and listing public functions.

#### Format

```python
"""
Brief one-line description of module purpose.

Extended description explaining the module's functionality,
what problems it solves, and when to use it. Can span multiple
paragraphs if necessary.

Functions
---------
function_name(param1: type, param2: type) -> return_type
    Brief description of what function does.
another_function(param: type) -> return_type
    Brief description of another function.

Classes
-------
ClassName
    Brief description of what class does and its purpose.
AnotherClass
    Brief description of another class.

Examples
--------
Basic usage example:

>>> import module_name
>>> result = module_name.function_name(param)
>>> print(result)
result_value

See Also
--------
related_module : If function uses or relates to another module.
"""
```

#### Example Module Header

```python
"""
Calculate scattering angles from momentum vectors.

This module provides functions to compute Compton scattering angles
and plane angles from particle momentum vectors. Uses NumPy for
efficient vector operations.

The main functionality includes calculating scattering angles (theta),
azimuthal angles (phi), and angles between scattering planes.

Functions
---------
calculate_scattering_angle(initial, final) -> float
    Calculate angle between initial and final momentum vectors.
calculate_azimuthal_angle(vector, plane) -> float
    Calculate azimuthal angle within scattering plane.
calculate_plane_angle(plane_a, plane_b) -> float
    Calculate angle between two scattering planes.
normalize_vector(vector) -> np.ndarray
    Normalize vector to unit length.

Classes
-------
ScatteringCalculator
    Calculate scattering angles from momentum data.
PlaneAngleComputer
    Compute angles between scattering planes.

Examples
--------
Basic usage:

>>> import numpy as np
>>> from compton_scattering import angle_calculator
>>> k0 = np.array([1, 0, 0])
>>> k = np.array([0, 1, 0])
>>> angle = angle_calculator.calculate_scattering_angle(k0, k)
>>> print(f"Angle: {angle:.4f} rad")
Angle: 1.5708 rad

See Also
--------
data_loader : Load data from CSV/HDF5 files.
output_writer : Write results to output files.
"""
```

### Module Constants Documentation

Document important module constants:

```python
"""Module constants."""

# Number of dimensions for momentum vectors
VECTOR_DIMENSION: Final[int] = 3

# Numerical tolerance for near-zero values
DEFAULT_TOLERANCE: Final[float] = 1e-10

# Supported output formats
SUPPORTED_FORMATS: Final[list[str]] = ["csv", "hdf5"]
```

---

## Class Documentation

### Class Docstring Format

```python
class ClassName:
    """
    Brief one-line description of class purpose.

    Extended description of the class, explaining what it does,
    when to use it, and any important notes. Can span multiple
    paragraphs.

    Attributes
    ----------
    attribute_name : type
        Description of attribute, what it stores, and its units
        or constraints if applicable.
    another_attribute : type
        Description of another attribute.

    Methods
    -------
    method_name(param) -> return_type
        Brief description of method.
    another_method() -> return_type
        Brief description of another method.

    Examples
    --------
    Creating and using the class:

    >>> calculator = ClassName()
    >>> result = calculator.method_name(param)
    >>> print(result)

    Notes
    -----
    Important behavior or limitations of the class.
    """

    def __init__(self) -> None:
        """Initialize ClassName."""
        pass
```

### Class Attributes

Document both instance and class attributes:

```python
class ScatteringCalculator:
    """
    Calculate scattering angles from momentum vectors.

    Attributes
    ----------
    plane_normal : np.ndarray
        Normal vector to reference scattering plane (shape: (3,)).
    tolerance : float
        Numerical tolerance for floating-point comparisons.
        Default is 1e-10.
    cache : dict[str, float]
        Cache of computed angles for repeated calculations.

    Examples
    --------
    >>> calculator = ScatteringCalculator()
    >>> angle = calculator.calculate_angle(plane_b)
    """

    DEFAULT_TOLERANCE: Final[float] = 1e-10

    def __init__(
        self,
        plane_normal: Optional[np.ndarray] = None,
    ) -> None:
        """
        Initialize ScatteringCalculator.

        Parameters
        ----------
        plane_normal : np.ndarray, optional
            Normal vector to reference plane (shape: (3,)).
            If None, initialized to (0, 0, 1).
        """
        self.plane_normal = plane_normal or np.array([0, 0, 1])
        self.tolerance: float = self.DEFAULT_TOLERANCE
        self.cache: dict[str, float] = {}
```

---

## Function and Method Documentation

### Function Docstring Format

```python
def function_name(
    param1: type,
    param2: type,
    param3: type = default_value,
) -> return_type:
    """
    Brief one-line description of function purpose.

    Extended description explaining what the function does,
    why you would use it, and any important implementation
    details or algorithms used.

    Parameters
    ----------
    param1 : type
        Description of first parameter, including constraints,
        valid ranges, and expected shape for arrays.
    param2 : type
        Description of second parameter.
    param3 : type, optional
        Description of optional parameter with default value.
        Default is `default_value`.

    Returns
    -------
    return_type
        Description of return value, including shape for arrays,
        valid ranges, and units if applicable.

    Raises
    ------
    ValueError
        Description of when ValueError is raised.
    TypeError
        Description of when TypeError is raised.

    Notes
    -----
    Important information about function behavior, performance
    considerations, numerical stability, or limitations.

    Examples
    --------
    Basic usage:

    >>> result = function_name(param1, param2)
    >>> print(result)
    expected_output

    With optional parameter:

    >>> result = function_name(param1, param2, param3=value)
    >>> print(result)
    expected_output

    See Also
    --------
    related_function : Related function for similar task.
    other_function : Another related function.
    """
    # Implementation
    pass
```

### Example Function Documentation

```python
def calculate_scattering_angle(
    initial_direction: np.ndarray,
    final_direction: np.ndarray,
) -> float:
    """
    Calculate scattering angle between momentum vectors.

    Computes the angle between initial and final momentum directions
    using the dot product: θ = arccos(k̂₀ · k̂). The angle represents
    the scattering angle in the center-of-mass frame.

    Parameters
    ----------
    initial_direction : np.ndarray
        Initial momentum direction vector (shape: (3,)).
        Does not need to be normalized; function handles normalization.
    final_direction : np.ndarray
        Final momentum direction vector (shape: (3,)).
        Does not need to be normalized.

    Returns
    -------
    float
        Scattering angle in radians, range [0, π].

    Raises
    ------
    ValueError
        If either vector has magnitude near zero (< 1e-10).
    TypeError
        If inputs are not numpy arrays.

    Notes
    -----
    The function automatically normalizes input vectors before
    computing the angle. Numerical errors can arise from dot product
    values slightly outside [-1, 1] due to floating-point precision,
    which are handled by clamping.

    The angle represents:
    - θ = 0: no scattering (forward direction)
    - θ = π/2: perpendicular scattering
    - θ = π: backscattering

    Examples
    --------
    Calculate angle for perpendicular scattering:

    >>> k0 = np.array([1, 0, 0])
    >>> k = np.array([0, 1, 0])
    >>> angle = calculate_scattering_angle(k0, k)
    >>> np.isclose(angle, np.pi / 2)
    True

    Function handles non-normalized vectors:

    >>> k0 = np.array([2, 0, 0])  # magnitude 2
    >>> k = np.array([0, 3, 0])   # magnitude 3
    >>> angle = calculate_scattering_angle(k0, k)
    >>> np.isclose(angle, np.pi / 2)
    True

    See Also
    --------
    calculate_azimuthal_angle : Calculate azimuthal angle in plane.
    normalize_vector : Normalize vector to unit length.
    """
    # Normalize input vectors
    try:
        k0_normalized = normalize_vector(initial_direction)
        k_normalized = normalize_vector(final_direction)
    except ValueError as e:
        raise ValueError(
            f"Cannot calculate angle with zero-magnitude vector: {e}"
        ) from e

    # Calculate angle with numerical stability
    cos_angle = np.dot(k0_normalized, k_normalized)
    cos_angle = np.clip(cos_angle, -1.0, 1.0)

    return np.arccos(cos_angle)
```

### Method Documentation

Methods follow same format as functions:

```python
class ScatteringCalculator:
    """Calculate scattering angles."""

    def calculate_angle(
        self,
        initial_direction: np.ndarray,
        final_direction: np.ndarray,
    ) -> float:
        """
        Calculate angle between momentum vectors.

        Parameters
        ----------
        initial_direction : np.ndarray
            Initial momentum (shape: (3,)).
        final_direction : np.ndarray
            Final momentum (shape: (3,)).

        Returns
        -------
        float
            Scattering angle in radians.

        Raises
        ------
        ValueError
            If vector magnitude is near zero.

        Examples
        --------
        >>> calc = ScatteringCalculator()
        >>> k0 = np.array([1, 0, 0])
        >>> k = np.array([0, 1, 0])
        >>> angle = calc.calculate_angle(k0, k)
        """
        return calculate_scattering_angle(
            initial_direction,
            final_direction,
        )
```

---

## Docstring Style

### NumPy Docstring Components

#### 1. Summary (Required)

One-line description ending with period:

```python
def normalize_vector(vector: np.ndarray) -> np.ndarray:
    """Normalize vector to unit length."""
    pass
```

#### 2. Extended Description (Optional)

Multi-paragraph explanation:

```python
"""
Normalize vector to unit length.

This function takes any input vector and scales it so that its
magnitude is exactly 1.0. The result vector points in the same
direction as the input but with unit magnitude.

This is commonly used in physics to work with direction vectors
independent of magnitude.
"""
```

#### 3. Parameters (For functions/methods)

Document all parameters:

```python
"""
Parameters
----------
vector : np.ndarray
    Input vector of any dimension and magnitude.
    Must be a 1D array.
tolerance : float, optional
    Tolerance for magnitude (default: 1e-10).
"""
```

#### 4. Attributes (For classes)

Document instance attributes:

```python
"""
Attributes
----------
plane_normal : np.ndarray
    Normal vector to plane (shape: (3,)).
energy : float
    Energy of particle in GeV.
"""
```

#### 5. Returns (For functions/methods)

Document return value:

```python
"""
Returns
-------
np.ndarray
    Normalized vector with magnitude 1.0 and same direction
    as input (shape: same as input).
"""
```

#### 6. Raises (For exceptions)

Document exceptions:

```python
"""
Raises
------
ValueError
    If input vector magnitude is zero or very small (< 1e-10).
TypeError
    If input is not a numpy array.
"""
```

#### 7. Examples

Provide practical examples:

```python
"""
Examples
--------
Normalize simple vector:

>>> vector = np.array([3, 4])
>>> normalized = normalize_vector(vector)
>>> np.linalg.norm(normalized)
1.0

Handles 3D vectors:

>>> vector = np.array([1, 2, 2])
>>> normalized = normalize_vector(vector)
>>> np.allclose(np.linalg.norm(normalized), 1.0)
True
"""
```

#### 8. Notes (Optional)

Additional important information:

```python
"""
Notes
-----
The function uses np.linalg.norm for numerical stability.
For vectors very close to zero magnitude, use the tolerance
parameter to define the minimum acceptable magnitude.

Performance is O(n) where n is vector dimension.
"""
```

#### 9. References (Optional)

Link to external resources:

```python
"""
References
----------
.. [1] https://en.wikipedia.org/wiki/Unit_vector
.. [2] NumPy documentation on vector normalization
"""
```

---

## Code Examples

### Good Example: Complete Documentation

```python
"""
Data loading utilities for Compton scattering analysis.

This module provides functions to load experimental or simulated
scattering data from CSV and HDF5 files, with validation and
data cleaning capabilities.

Functions
---------
load_csv_data(filepath) -> pd.DataFrame
    Load scattering data from CSV file.
load_hdf5_data(filepath, dataset) -> pd.DataFrame
    Load scattering data from HDF5 file.
validate_scattering_data(data) -> bool
    Validate that data has required columns.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional


def load_csv_data(filepath: str) -> pd.DataFrame:
    """
    Load scattering data from CSV file.

    Reads a CSV file containing momentum vectors and scattering data.
    Automatically detects and handles standard column names.

    Parameters
    ----------
    filepath : str
        Path to CSV file containing scattering data.
        Must be readable CSV format with headers.

    Returns
    -------
    pd.DataFrame
        DataFrame with scattering data. Columns typically include:
        - theta_a, phi_a: scattering angles for plane A
        - theta_b, phi_b: scattering angles for plane B
        - plane_angle: angle between scattering planes

    Raises
    ------
    FileNotFoundError
        If file does not exist.
    ValueError
        If CSV format is invalid.
    pd.errors.ParserError
        If CSV cannot be parsed.

    Examples
    --------
    Load data from file:

    >>> data = load_csv_data("scattering_data.csv")
    >>> print(data.shape)
    (1000, 5)

    Check column names:

    >>> print(data.columns.tolist())
    ['theta_a', 'phi_a', 'theta_b', 'phi_b', 'plane_angle']
    """
    file_path = Path(filepath)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    try:
        return pd.read_csv(file_path)
    except pd.errors.ParserError as e:
        raise ValueError(f"Invalid CSV format: {e}") from e


def validate_scattering_data(
    data: pd.DataFrame,
    required_columns: Optional[list[str]] = None,
) -> bool:
    """
    Validate that data has required scattering columns.

    Checks that DataFrame has all necessary columns for scattering
    angle analysis. By default, requires theta_a, phi_a, theta_b,
    phi_b, and plane_angle columns.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame to validate.
    required_columns : list[str], optional
        List of required column names. If None, uses default
        scattering columns. Default is None.

    Returns
    -------
    bool
        True if all required columns present, False otherwise.

    Raises
    ------
    ValueError
        If data is empty or not a DataFrame.

    Examples
    --------
    Validate with default columns:

    >>> data = pd.DataFrame({
    ...     'theta_a': [0.5, 1.0],
    ...     'phi_a': [0.1, 0.2],
    ...     'theta_b': [0.3, 0.8],
    ...     'phi_b': [0.4, 0.5],
    ...     'plane_angle': [0.1, 0.2]
    ... })
    >>> validate_scattering_data(data)
    True

    Validate with custom columns:

    >>> custom_cols = ['angle1', 'angle2']
    >>> validate_scattering_data(data, custom_cols)
    False
    """
    if not isinstance(data, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame")

    if data.empty:
        raise ValueError("DataFrame is empty")

    if required_columns is None:
        required_columns = [
            'theta_a', 'phi_a', 'theta_b', 'phi_b', 'plane_angle'
        ]

    return all(col in data.columns for col in required_columns)
```

### Bad Example: Missing Documentation

```python
# Bad: No module docstring
import pandas as pd

def load_data(f):
    # Bad: No docstring, unclear parameter
    return pd.read_csv(f)

def validate(d):
    # Bad: No docstring, no type hints
    return 'theta_a' in d.columns
```

---

## Project Documentation

### README Structure

Create comprehensive README.md with:

```markdown
# Compton Scattering Plane Angle Extractor

Brief description of project.

## Installation

Installation instructions.

## Quick Start

Quick usage examples.

## Features

List of main features.

## API Reference

Link to API.md or inline documentation.

## Examples

Practical usage examples with code.

## Testing

How to run tests.

## Documentation

Links to detailed documentation.

## Contributing

Link to CONTRIBUTION.md.

## License

License information.
```

### API Documentation

Create API.md documenting all public functions and classes.

---

## Best Practices

### 1. Keep Examples Executable

```python
"""
Examples
--------
Examples should run without modification:

>>> import numpy as np
>>> from module import function
>>> result = function(np.array([1, 0, 0]))
>>> print(f"{result:.4f}")
0.0000
"""
```

### 2. Document Exceptions

```python
"""
Raises
------
ValueError
    If input validation fails or values are out of acceptable range.
TypeError
    If input type is unexpected (e.g., not np.ndarray).
"""
```

### 3. Use Consistent Formatting

```python
"""
Parameters
----------
param1 : type
    Description with consistent format.
param2 : type, optional
    Optional parameter description.
"""
```

### 4. Link Related Functions

```python
"""
See Also
--------
related_function : What it does.
another_function : What it does.
"""
```

### 5. Include Type Information

```python
"""
Parameters
----------
data : pd.DataFrame
    Input DataFrame with columns [col1, col2, ...].
    Expected shape: (n_samples, n_features).
"""
```

---

## Documentation Checklist

Before submitting code, verify:

- [ ] Module has header docstring with functions and classes listed
- [ ] All public functions have docstrings
- [ ] All public classes have docstrings
- [ ] All public methods have docstrings
- [ ] Docstrings use NumPy style
- [ ] All parameters documented with types
- [ ] All return values documented
- [ ] Exceptions documented
- [ ] Examples provided and executable
- [ ] Type hints match docstring documentation
- [ ] No broken references in "See Also" sections
- [ ] Examples follow PEP 8 style

---

**Last Updated:** June 2026  
**Version:** 1.0