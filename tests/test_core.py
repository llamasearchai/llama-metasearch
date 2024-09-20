"""Basic tests for the llama-metasearch package."""

import pytest

# Try importing the package
try:
    import llama_metasearch
except ImportError as e:
    pytest.fail(f"Failed to import llama_metasearch: {e}", pytrace=False)


def test_import():
    """Test that the main package can be imported."""
    assert llama_metasearch is not None


def test_version():
    """Test that the package has a version attribute."""
    assert hasattr(llama_metasearch, "__version__")
    assert isinstance(llama_metasearch.__version__, str)


# Add more tests later:
# - Test MetaSearcher initialization
# - Test asynchronous querying of mocked sources (using pytest-asyncio and httpx mocks)
# - Test result merging and deduplication logic
# - Test ranking logic (with simple or mocked rankers)
# - Test integration with actual (mocked) dependent services like llamafind
