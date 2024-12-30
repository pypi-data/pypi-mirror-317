# lilliepy_import

lilliepy_import is a Python package that provides utility functions for dynamically importing modules and components. 
It is designed to make it easy to set a component directory and load specific functions or classes dynamically.

## Features

- Dynamically set a component folder using `Importer`.
- Import specific functions or classes from files in the component folder with `_import`.
- Supports dynamic module imports with error handling.

## Installation

To install the package, use pip:

```bash
pip install lilliepy_import
```

## Usage

### Setting the Component Folder

First, set the component folder where your modules are stored:

```python
from lilliepy_import import Importer

# Set the component folder
Importer("components")
```

### Importing a Function or Class

You can then dynamically import a specific function or class:

```python
from lilliepy_import import _import

# Dynamically import a function or class
try:
    my_function = _import("my_module.py", "my_function")
    if my_function:
        my_function()  # Call the imported function
    else:
        print("Function not found in the module.")
except Exception as e:
    print(f"Error: {e}")
```

### Example

Assume the following directory structure:

```
project/
├── components/
│   └── my_module.py
└── main.py
```

**my_module.py**:
```python
from reactpy import component, html

@component
def my_function():
    return html.h1("yo")
```

**main.py**:
```python
from lilliepy_import import Importer, _import

# Set the component folder
Importer("components")

# Import and call the function
func = _import("my_module.py", "my_function")
if func:
    func()
```

When you run `main.py`, the output will be:

```
Hello from my_function!
```

## Error Handling

- Raises a `ValueError` if the component folder is not set before calling `_import`.
- Raises a `FileNotFoundError` if the specified file does not exist.
- Handles cases where the function or class is not found in the module.

## License

This project is licensed under the MIT License.
