# Numo

A Python library for mathematical operations, unit conversions, currency conversions, and translations.

## Features

- Safe mathematical expression evaluation
- Unit conversions (length, weight, time, etc.)
- Currency conversions
- Text translations
- Variable management
- Custom function support

## Installation

```bash
pip install numo
```

## Usage

```python
from numo import Numo

# Create a Numo instance
numo = Numo()

# Mathematical operations
result = await numo.calculate("2 + 2")  # Returns "4.0"
result = await numo.calculate("3 * 4")  # Returns "12.0"

# Unit conversions
result = await numo.calculate("1 km to m")  # Returns "1000.0"
result = await numo.calculate("100 cm to m")  # Returns "1.0"

# Currency conversions
result = await numo.calculate("100 USD to EUR")  # Returns amount in EUR

# Translations
result = await numo.calculate("hello in spanish")  # Returns "hola"

# Variable management
results = await numo.calculate([
    "x = 5",
    "y = 3",
    "x + y"  # Returns "8.0"
])

# Function calls
result = await numo.calculate("nsum(1,2,3,4)")  # Returns "10.0"
```

## Features

### Mathematical Operations
- Basic arithmetic operations (+, -, *, /, %, ^)
- Safe evaluation using AST
- Protection against dangerous operations

### Unit Conversions
- Length (km, m, cm, etc.)
- Weight (kg, g, lb, etc.)
- Time (hour, minute, second)
- Digital storage (gb, mb, kb)
- And more...

### Currency Conversions
- Real-time exchange rates
- Support for major currencies
- Accurate decimal handling

### Translations
- Support for multiple languages
- Simple "text in language" format
- Reliable translation service

### Variable Management
- Define and use variables
- Mathematical operations with variables
- Persistent variable storage

### Function Support
- Built-in mathematical functions
- Statistical functions (sum, average, min, max)
- Safe function execution

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
