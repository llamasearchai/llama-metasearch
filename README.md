# llama-metasearch

[![PyPI version](https://img.shields.io/pypi/v/llama_metasearch.svg)](https://pypi.org/project/llama_metasearch/)
[![License](https://img.shields.io/github/license/llamasearchai/llama-metasearch)](https://github.com/llamasearchai/llama-metasearch/blob/main/LICENSE)
[![Python Version](https://img.shields.io/pypi/pyversions/llama_metasearch.svg)](https://pypi.org/project/llama_metasearch/)
[![CI Status](https://github.com/llamasearchai/llama-metasearch/actions/workflows/llamasearchai_ci.yml/badge.svg)](https://github.com/llamasearchai/llama-metasearch/actions/workflows/llamasearchai_ci.yml)

**Llama Metasearch (llama-metasearch)** is a powerful metasearch engine within the LlamaSearch AI ecosystem. It aggregates results from multiple underlying search sources, ranks them, and presents a unified set of results to the user.

## Key Features

- **Metasearch Engine:** Core logic for querying multiple sources and combining results (`metasearch.py`).
- **Source Aggregation:** Fetches results from various configured search engines or APIs.
- **Result Ranking:** Implements algorithms to rank aggregated results effectively.
- **Unified API:** Provides a single point of access for querying diverse sources.
- **Core Module:** Manages the overall metasearch process (`core.py`).
- **Configurable:** Allows defining search sources, ranking parameters, and other settings (`config.py`).

## Installation

```bash
pip install llama-metasearch
# Or install directly from GitHub for the latest version:
# pip install git+https://github.com/llamasearchai/llama-metasearch.git
```

## Usage

*(Usage examples demonstrating how to perform metasearch queries will be added here.)*

```python
# Placeholder for Python client usage
# from llama_metasearch import MetasearchClient, SearchConfig

# config = SearchConfig.load("config.yaml")
# client = MetasearchClient(config)

# # Perform a metasearch query
# results = client.search("artificial intelligence trends", sources=["web", "news", "academic"])
# for result in results:
#     print(f"[{result.source}] {result.title} - {result.url}")
```

## Architecture Overview

```mermaid
graph TD
    A[User Query] --> B{Core Orchestrator (core.py)};
    B --> C{Metasearch Engine (metasearch.py)};
    C -- Queries --> D[Source 1 Interface];
    C -- Queries --> E[Source 2 Interface];
    C -- Queries --> F[...];
    D --> G((Source 1 API / DB));
    E --> H((Source 2 API / DB));
    F --> I((...));
    G -- Results --> C;
    H -- Results --> C;
    I -- Results --> C;
    C --> J{Result Aggregation & Ranking};
    J --> K[Unified Search Results];

    L[Configuration (config.py)] -- Configures --> B;
    L -- Configures --> C;
    L -- Configures --> D;
    L -- Configures --> E;
    L -- Configures --> F;

    style C fill:#f9f,stroke:#333,stroke-width:2px
```

1.  **Query Input:** The user submits a search query.
2.  **Core Orchestrator:** Manages the request flow.
3.  **Metasearch Engine:** Receives the query and dispatches it to configured source interfaces.
4.  **Source Interfaces:** Interact with the actual underlying search sources (APIs, databases, etc.).
5.  **Aggregation & Ranking:** The engine gathers results from all sources, deduplicates, and ranks them.
6.  **Output:** Presents a unified list of ranked results.
7.  **Configuration:** Defines which sources to query, API keys, ranking strategies, etc.

## Configuration

*(Details on configuring search sources, API keys, ranking algorithms, result caching, etc., will be added here.)*

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/llamasearchai/llama-metasearch.git
cd llama-metasearch

# Install in editable mode with development dependencies
pip install -e ".[dev]"
```

### Testing

```bash
pytest tests/
```

### Contributing

Contributions are welcome! Please refer to [CONTRIBUTING.md](CONTRIBUTING.md) and submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
*Developed by lalamasearhc.*
