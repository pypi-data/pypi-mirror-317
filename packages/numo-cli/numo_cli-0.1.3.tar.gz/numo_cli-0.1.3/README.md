# Numo CLI

A powerful command-line interface for calculations, unit conversions, and translations.

## Features

- Simple arithmetic calculations
- Unit conversions (length, mass, currency, etc.)
- Text translations
- Interactive shell mode
- Batch processing of multiple expressions

## Installation

You can install Numo CLI using pip:

```bash
pip install numo-cli
```

After installation, you might need to add Python's user scripts directory to your PATH. For macOS/Linux, add this line to your `~/.zshrc` or `~/.bashrc`:
```bash
export PATH="$HOME/Library/Python/3.9/bin:$PATH"  # Adjust Python version as needed
```

Then reload your shell:
```bash
source ~/.zshrc  # or source ~/.bashrc
```

## Usage

You can use Numo CLI in two ways:

### 1. Direct Command (Recommended)

Run in interactive mode:
```bash
numo-cli
```

Or with direct calculations:
```bash
numo-cli "2 + 2"
numo-cli "1 km to m"
numo-cli "hello in spanish"
```

### 2. Python Module

If the direct command doesn't work, you can always use the Python module syntax:
```bash
python -m numo_cli
```

Or with arguments:
```bash
python -m numo_cli "2 + 2"
python -m numo_cli "1 km to m"
python -m numo_cli "hello in spanish"
```

### Example Commands

Here are some examples of what you can do in either mode:
```
>>> 2 + 2
4

>>> 1 km to m
1000 m

>>> hello in spanish
hola

>>> 100 usd to eur
91.85 EUR
```

## Requirements

- Python 3.7 or higher
- `numo` package
- `aiohttp`
- `typing-extensions`

## Development

1. Clone the repository:
```bash
git clone https://github.com/furkancosgun/numo-cli.git
cd numo-cli
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install in development mode:
```bash
pip install -e .
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

- Furkan Cosgun ([@furkancosgun](https://github.com/furkancosgun))

## Acknowledgments

- Built with [Numo](https://github.com/furkancosgun/numo) library
