# String Utils Rjl

A simple Python package for string operations including reversal, palindrome check, and character frequency.

## Installation

pip install string_utils_rjl


## Usage

```python
from string_utils_rjl import reverse_string, is_palindrome, char_frequency

# Reverse a string
print(reverse_string("hello"))  # Output: "olleh"

# Check if a string is a palindrome
print(is_palindrome("racecar"))  # Output: True

# Calculate character frequency
print(char_frequency("moonshot"))  # Output: {'m': 1, 'o': 2, 'n': 1, 's': 1, 'h': 1, 't': 1}