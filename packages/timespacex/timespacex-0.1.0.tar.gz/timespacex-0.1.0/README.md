# TimeSpaceX

A powerful Python Time and Space Complexity Analyzer that helps you understand the computational complexity of your code.

## Features

- Analyzes both time and space complexity
- Provides detailed explanations
- Detects common patterns:
  - Simple loops (O(n))
  - Nested loops (O(n²), O(n³))
  - Binary search patterns (O(log n))
  - Divide and conquer algorithms (O(n log n))
  - Recursive functions
  - Matrix operations
- Beautiful command-line interface with syntax highlighting

## Installation

```bash
pip install timespacex
```

## Usage

Analyze a Python file:
```bash
timespacex your_file.py
```

Options:
```bash
timespacex --no-color your_file.py  # Disable colored output
```

## Example

Given a Python file `example.py` with the following content:

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

Running:
```bash
timespacex example.py
```

Will output:
```
Time & Space Complexity Analysis
==================================================

┌─ Function: binary_search ──────────────────────┐
│ The function `binary_search` has a time        │
│ complexity of O(log n). This is because the    │
│ function uses a binary search pattern,         │
│ dividing the search space in half at each      │
│ step.                                          │
│                                               │
│ The space complexity is O(1). This is because │
│ the function uses a constant amount of extra   │
│ space regardless of input size.               │
└───────────────────────────────────────────────┘
```

## Limitations

- The analysis is based on static code analysis and may not catch all edge cases
- Complex algorithmic patterns might not be accurately detected
- The tool provides simplified complexity analysis and may not catch subtle optimizations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 