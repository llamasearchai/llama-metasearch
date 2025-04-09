"""Tests for core functionality"""
import pytest
from llama_metasearch.core import Client


def test_client_initialization():
    """Test that client initializes properly"""
    client = Client()
    assert client is not None
    assert client.config == {}
    
    # Test with config
    config = {"timeout": 60}
    client = Client(config=config)
    assert client.config == config


def test_client_process():
    """Test processing functionality"""
    client = Client()
    result = client.process("test data")
    assert isinstance(result, dict)
    assert "result" in result
    assert "input" in result
    assert result["input"] == "test data"


def test_client_status():
    """Test status functionality"""
    client = Client()
    status = client.get_status()
    assert isinstance(status, dict)
    assert "status" in status


def test_search():
    """Test search functionality"""
    client = Client()
    results = client.search("test query")
    assert "query" in results
    assert "results" in results
    assert "meta" in results
    assert results["query"] == "test query"
    assert len(results["results"]) > 0
    
    
def test_async_search():
    """Test async search functionality"""
    client = Client()
    job_id = client.async_search("test query")
    assert isinstance(job_id, str)
