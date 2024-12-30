"""
Pytest configuration and shared fixtures
"""

import pytest

@pytest.fixture
def sample_config():
    """
    Sample configuration fixture for testing
    """
    return {
        "model": "gpt-4o",
        "temperature": 0.7,
        "max_tokens": 1000
    }