# Examples

This page provides examples of using Llama Metasearch for various tasks.

## Basic Usage

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

## Advanced Usage

```python
from llama_metasearch import Client
import asyncio

# Initialize client with custom configuration
client = Client(
    config={
        "timeout": 60,
        "max_retries": 3,
        "log_level": "debug"
    }
)

# Process multiple inputs concurrently
async def process_batch(inputs):
    tasks = [client.process_async(inp) for inp in inputs]
    return await asyncio.gather(*tasks)

# Run async processing
inputs = ["input1", "input2", "input3", "input4"]
results = asyncio.run(process_batch(inputs))

# Print results
for i, result in enumerate(results):
    print(f"Result {i+1}: {result}")
```

For more examples, check out the [examples directory](https://github.com/llamasearchai/llama-metasearch/tree/main/examples) in the GitHub repository.
