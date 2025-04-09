"""Pytest configuration for testing"""
import pytest


@pytest.fixture
def sample_config():
    """Provide a sample configuration for testing"""
    return {"timeout": 30, "retries": 3, "log_level": "debug"}


@pytest.fixture
def sample_data():
    """Provide sample data for testing"""
    return {"key": "value", "nested": {"inner": "data"}}


@pytest.fixture
def sample_queries():
    """Provide sample search queries"""
    return ["machine learning", "artificial intelligence", "python programming"]
