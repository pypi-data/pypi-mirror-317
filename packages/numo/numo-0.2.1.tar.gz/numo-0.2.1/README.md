# 🔢 Numo: Your Smart Mathematical Companion

[![PyPI version](https://badge.fury.io/py/numo.svg)](https://badge.fury.io/py/numo)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Numo is a powerful, intuitive Python library that brings mathematics to life. It combines mathematical operations, unit conversions, currency exchanges, and translations into a single, elegant package. Whether you're a student, developer, or data scientist, Numo makes complex calculations and conversions feel natural and straightforward.

## ✨ Key Features

### 🧮 Smart Mathematical Expression Evaluation
- Safe and intelligent expression parsing
- Support for complex mathematical operations
- Built-in protection against dangerous operations

```python
from numo import Numo
numo = Numo()

# Basic calculations
await numo.calculate("2 * (3 + 4)")  # Returns "14.0"
await numo.calculate("2^3 + 4")      # Returns "12.0"

# Use mathematical constants
await numo.calculate("2 * pi")       # Returns "6.28318530717959"
await numo.calculate("e^2")          # Returns "7.3890560989307"
```

### 📐 Comprehensive Function Library
Built-in mathematical and statistical functions:

```python
# Statistical functions
await numo.calculate("avg(1, 2, 3, 4)")     # Returns "2.50"
await numo.calculate("std(1, 2, 3, 4)")     # Returns "1.29"

# Mathematical functions
await numo.calculate("sin(pi/2)")           # Returns "1.00"
await numo.calculate("log10(100)")          # Returns "2.00"
await numo.calculate("sqrt(16)")            # Returns "4.00"
```

Available functions include:
- Basic: `abs`, `round`, `floor`, `ceil`
- Statistical: `sum`, `avg`, `min`, `max`, `median`, `var`, `std`
- Trigonometric: `sin`, `cos`, `tan`, `asin`, `acos`, `atan`
- Advanced Math: `pow`, `sqrt`, `log`, `log10`, `exp`, `fact`, `gcd`

### 📏 Intuitive Unit Conversions
Convert between various units seamlessly:

```python
# Length conversions
await numo.calculate("5.5 km to miles")    # Returns "3.42"
await numo.calculate("72 inch to cm")      # Returns "182.88"

# Weight/Mass conversions
await numo.calculate("100 kg to lbs")      # Returns "220.46"
await numo.calculate("16 oz to grams")     # Returns "453.59"

# Temperature conversions
await numo.calculate("32 F to C")          # Returns "0.00"
await numo.calculate("100 C to F")         # Returns "212.00"

# Digital storage
await numo.calculate("1.5 GB to MB")       # Returns "1536.00"
```

### 💱 Real-time Currency Conversion
Up-to-date currency conversion with major world currencies:

```python
# Currency conversions
await numo.calculate("100 USD to EUR")     # Real-time conversion
await numo.calculate("1000 JPY to GBP")    # Real-time conversion
await numo.calculate("50 EUR to TRY")      # Real-time conversion
```

### 🌍 Language Translation
Quick and accurate translations:

```python
# Simple translations
await numo.calculate("hello in spanish")    # Returns "hola"
await numo.calculate("good morning in french")  # Returns "bonjour"
```

### 📝 Smart Variable Management
Define and use variables in your calculations:

```python
# Variable definitions and operations
results = await numo.calculate([
    "radius = 5",
    "area = pi * radius^2",
    "circumference = 2 * pi * radius",
    "area"                          # Returns "78.54"
])

# Using predefined constants
await numo.calculate("phi * 10")    # Golden ratio * 10
await numo.calculate("sqrt2 * 5")   # √2 * 5
```

Built-in constants include:
- Mathematical: `pi`, `e`, `tau`, `phi` (golden ratio)
- Common values: `sqrt2`, `sqrt3`
- Angles: `deg30`, `deg45`, `deg60`, `deg90`, `deg180`, `deg360`
- Scientific: `c` (speed of light), `g` (gravity), `h` (Planck constant)

## 🚀 Installation

```bash
pip install numo
```

## 🎯 Quick Start

```python
from numo import Numo

# Create a Numo instance
numo = Numo()

# Start calculating!
result = await numo.calculate("5 km to miles")
print(result)  # "3.11"

# Chain operations
results = await numo.calculate([
    "distance = 100",              # Store variable
    "time = 9.58",                # Usain Bolt's record
    "speed = distance / time",     # Calculate speed
    "speed km/h to mph"           # Convert to mph
])
```

## 🛠️ Advanced Usage

### Custom Variable Management
```python
# Define and use custom variables
await numo.calculate([
    "tax_rate = 0.18",
    "price = 100",
    "tax = price * tax_rate",
    "total = price + tax",
    "total"                        # Returns "118.00"
])
```

### Complex Calculations
```python
# Combine multiple features
await numo.calculate([
    "radius = 10 cm to m",         # Unit conversion
    "volume = (4/3) * pi * radius^3",  # Mathematical expression
    "volume m^3 to liters"         # Another conversion
])
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Star Us!

If you find Numo helpful, please consider giving us a star on GitHub! It helps us know that you find the project useful and encourages further development.
