# 🔢 Numo: Your Smart Mathematical Companion

[![PyPI version](https://badge.fury.io/py/numo.svg)](https://badge.fury.io/py/numo)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

> 🚀 Numo is a powerful text-based calculator and unit converter that brings mathematics to life through natural language processing. Whether you're a student, developer, or data scientist, Numo makes complex calculations feel natural and intuitive.

## ✨ Key Features

### 🧮 Mathematical Functions
- **Basic Operations**
  - Arithmetic operations (`+`, `-`, `*`, `/`, `^`)
  - Parentheses support for complex expressions
  - Automatic decimal precision handling

- **Advanced Mathematics**
  - Trigonometric functions (`sin`, `cos`, `tan`, etc.)
  - Logarithmic functions (`log`, `log10`, `exp`)
  - Root calculations (`sqrt`, `cbrt`)

- **Statistical Analysis**
  - Basic statistics (`mean`, `median`, `mode`)
  - Variance and standard deviation
  - Quartiles and percentiles

- **Vector Operations**
  - Vector magnitude calculation
  - Dot product computation
  - Angle between vectors

- **Financial Tools**
  - Compound interest calculator
  - Simple interest calculator
  - Payment (PMT) calculator

- **Advanced Features**
  - Combinatorics (`permutation`, `combination`)
  - Percentage calculations
  - Custom rounding functions

### 📏 Unit Conversions
- **Physical Measurements**
  - Length (meters, feet, miles, etc.)
  - Weight (kilograms, pounds, etc.)
  - Volume (liters, gallons, etc.)
  - Area (square meters, acres, etc.)

- **Time & Speed**
  - Time units (seconds to years)
  - Speed conversions (km/h, mph, etc.)
  - Angular measurements (degrees, radians)

- **Digital Units**
  - Storage (bytes to yottabytes)
  - Data rates (bps to TBps)
  - Both decimal (MB) and binary (MiB) units

- **Scientific Units**
  - Pressure (pascal, bar, psi, etc.)
  - Electrical (volt, ampere, watt, etc.)
  - Power (horsepower, kilowatt, etc.)

- **Display Units**
  - Screen measurements (px, pt, em)
  - Resolution (dpi, ppi)
  - Typography units (pica)

### 🌍 Language Translation
- **Comprehensive Support**
  - 100+ languages supported
  - Natural language processing
  - Automatic language detection

- **Easy Syntax**
  - Simple format: "text in language"
  - Supports full sentences
  - Maintains formatting

### 💾 Variable Management
- **Smart Storage**
  - Dynamic variable assignment
  - Expression evaluation
  - Persistent storage between sessions

- **Advanced Features**
  - Complex expression support
  - Mathematical constants (`pi`, `e`, etc.)
  - Function results storage

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/furkancosgun/numo.git
cd numo

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from numo import Numo

# Initialize Numo
numo = Numo()

# Mathematical calculations
await numo.calculate("2 * (3 + 4)")  # Returns: "14.00"
await numo.calculate("sin(pi/2)")    # Returns: "1.00"

# Unit conversions
await numo.calculate("5.5 km to miles")  # Returns: "3.42 miles"
await numo.calculate("100 MB to GB")     # Returns: "0.10 GB"

# Language translation
await numo.calculate("Hello world in spanish")  # Returns: "hola mundo"

# Variable management
await numo.calculate([
    "radius = 5",
    "area = pi * radius^2",
    "area"  # Returns: "78.54"
])
```

## 📚 Detailed Examples

### 🧮 Mathematical Functions
```python
# Statistical Analysis
mean(1, 2, 3, 4)     # Returns: 2.50
std(1, 2, 3)         # Returns: 1.00
percentile(75, 1, 2, 3, 4)  # Returns: 3.00

# Vector Mathematics
vector_magnitude(3, 4)         # Returns: 5.00
vector_dot(1, 2, 3, 4)        # Returns: 11.00
vector_angle(1, 0, 0, 1)      # Returns: 90.00

# Financial Calculations
compound_interest(1000, 5, 2)  # Returns: 1102.50
pmt(1000, 5, 12)             # Returns: 85.47

# Advanced Operations
permutation(5, 2)    # Returns: 20.00
combination(5, 2)    # Returns: 10.00
percent_change(100, 150)  # Returns: 50.00
```

### 📏 Unit Conversions
```python
# Length & Distance
"5.5 meters to feet"      # Returns: 18.04 feet
"1 mile to kilometers"    # Returns: 1.61 kilometers
"100 yards to meters"     # Returns: 91.44 meters

# Weight & Mass
"150 pounds to kg"        # Returns: 68.04 kg
"1000 grams to ounces"    # Returns: 35.27 ounces
"2 tons to kilograms"     # Returns: 1814.37 kilograms

# Digital Storage
"1.5 GB to MB"           # Returns: 1536.00 MB
"1 TiB to GiB"           # Returns: 1024.00 GiB
"500 MB to bytes"        # Returns: 524288000 bytes

# Data Transfer Rates
"100 Mbps to Gbps"       # Returns: 0.10 Gbps
"1 GBps to Mbps"         # Returns: 8192.00 Mbps

# Scientific Units
"1 bar to psi"           # Returns: 14.50 psi
"760 mmHg to atm"        # Returns: 1.00 atm
"100 hp to kW"           # Returns: 74.57 kW
```

## 🤝 Contributing

We love your input! We want to make contributing to Numo as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

### Development Process

1. Fork the repo and create your branch from `main`
2. Add tests if you've added code that should be tested
3. Update documentation if you've changed APIs
4. Ensure the test suite passes
5. Make sure your code follows the style guidelines
6. Issue your pull request!

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Show Your Support

If you find Numo helpful, please consider giving us a star on GitHub! It helps us know that you find the project useful and encourages further development.

## 📬 Contact

Have questions? Feel free to [open an issue](https://github.com/furkancosgun/numo/issues)!

---

<p align="center">
Made with ❤️ by Furkan Cosgun
</p>

