# llama-metasearch

[![PyPI version](https://badge.fury.io/py/llama-metasearch.svg)](https://badge.fury.io/py/llama-metasearch)
[![Python Version](https://img.shields.io/pypi/pyversions/llama-metasearch.svg)](https://pypi.org/project/llama-metasearch/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/yourusername/llama-metasearch-pkg/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/llama-metasearch-pkg/actions/workflows/ci.yml)

## Installation

```bash
pip install -e .
```

## Usage

```python
from llama_metasearch import LlamaMetasearchClient

# Initialize the client
client = LlamaMetasearchClient(api_key="your-api-key")
result = client.query("your query")
print(result)
```

## Features

- Fast and efficient
- Easy to use API
- Comprehensive documentation
- Asynchronous support

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/nikjois/llama-metasearch.git
cd llama-metasearch

# Install development dependencies
pip install -e ".[dev]"
```

### Testing

```bash
pytest
```

## License

MIT

## Author

Nik Jois (nikjois@llamasearch.ai)
