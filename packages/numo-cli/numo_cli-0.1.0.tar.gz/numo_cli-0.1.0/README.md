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

## Usage

### Interactive Mode

Simply run `numo` to start the interactive shell:

```bash
numo
```

Example commands in interactive mode:
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

### Command Line Arguments

You can also use Numo CLI directly from the command line:

```bash
numo "2 + 2"
numo "1 km to m"
numo "hello in spanish"
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
