# Llama Metasearch

Advanced search system with semantic understanding and vector search capabilities

[![GitHub](https://img.shields.io/github/license/llamasearchai/llama-metasearch)](https://github.com/llamasearchai/llama-metasearch/blob/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/llama_metasearch.svg)](https://pypi.org/project/llama_metasearch/)

## Overview


Advanced search system with semantic understanding and vector search capabilities. This library provides a comprehensive set of tools and utilities for
working with metasearch tasks in AI and data processing workflows.
It's designed to be easy to use while offering powerful capabilities for complex scenarios.


## Features


- **Semantic Search**: Understand the meaning behind search queries
- **Vector-Based Retrieval**: Find similar documents using embedding vectors
- **Hybrid Search**: Combine keyword and semantic approaches for best results
- **Customizable Ranking**: Adjust how search results are ranked and presented
- **Faceted Search**: Filter results by various dimensions and attributes


## Installation

```bash
pip install llama_metasearch
```

## Usage

```python

from llama_metasearch import SearchClient

# Initialize client
client = SearchClient(api_key="your_api_key")

# Perform search
results = client.search("quantum computing applications", max_results=10)

# Process results
for result in results:
    print(f"Title: {result.title}")
    print(f"URL: {result.url}")
    print(f"Score: {result.score}")

```

## Documentation

For more detailed documentation, see the [docs](docs/) directory.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
