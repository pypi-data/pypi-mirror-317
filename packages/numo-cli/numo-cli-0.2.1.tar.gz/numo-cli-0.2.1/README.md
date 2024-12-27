# 🚀 Numo CLI

> Your Swiss Army Knife for Calculations, Conversions, and Translations in the Terminal!


[![PyPI version](https://badge.fury.io/py/numo.svg)](https://badge.fury.io/py/numo-cli)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)


Numo CLI transforms your terminal into a powerful computational assistant. Whether you need to crunch numbers, convert units, or translate text, Numo CLI has got you covered - all without leaving your command line!

## ✨ Features

🧮 **Smart Calculations**
- Basic arithmetic operations
- Complex mathematical expressions
- Scientific calculations
- Support for parentheses and operator precedence

🔄 **Universal Converter**
- Length (km, m, mi, ft, etc.)
- Mass (kg, g, lb, oz, etc.)
- Currency (Real-time rates for USD, EUR, GBP, etc.)
- Temperature (°C, °F, K)
- And many more!

🌍 **Instant Translations**
- Support for multiple languages
- Natural language processing
- Instant results

⚡ **Powerful CLI**
- Interactive shell with command history
- Batch processing for multiple calculations
- Function and variable listing
- User-friendly error messages

## 🚀 Quick Start

### Installation

```bash
pip install numo-cli
```

For macOS/Linux users, add Python's bin directory to your PATH:
```bash
echo 'export PATH="$HOME/Library/Python/3.9/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Interactive Mode

Launch the interactive shell:
```bash
numo-cli
```

### Direct Commands

```bash
# Mathematical Operations
numo-cli "2 * (3 + 4)"          # Output: 14
numo-cli "sqrt(16)"             # Output: 4

# Unit Conversions
numo-cli "5.5 km to miles"      # Output: 3.42 miles
numo-cli "100 usd to eur"       # Output: 91.85 EUR
numo-cli "30 celsius to f"      # Output: 86°F

# Translations
numo-cli "hello world in spanish"  # Output: hola mundo
numo-cli "good morning in japanese" # Output: おはようございます
```

## 🎯 Advanced Usage

### Available Commands

In interactive mode, try these special commands:

```bash
# List all available functions
>>> list functions

# List all available variables
>>> list variables

# Complex calculations
>>> sin(45) + cos(30)
>>> log(1000) / ln(10)

# Chained conversions
>>> 100 km/h to m/s
>>> 1 btc to usd to eur
```

### Batch Processing

Process multiple expressions at once:
```bash
numo-cli "1 + 1" "2 * 2" "3 ^ 2"
```

## 🛠️ Development Setup

1. Clone and setup:
```bash
git clone https://github.com/furkancosgun/numo-cli.git
cd numo-cli
```

2. Create virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install -e .
```

## 🤝 Contributing

We love your input! Want to contribute? Here's how:

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Furkan Cosgun**
- GitHub: [@furkancosgun](https://github.com/furkancosgun)
- LinkedIn: [Furkan Cosgun](https://linkedin.com/in/furkancsgn)

## 🙏 Acknowledgments

- Built with ❤️ using [Numo](https://github.com/furkancosgun/numo) library
- Special thanks to all contributors

---

<p align="center">
Made with ❤️ by Furkan Cosgun
</p>
