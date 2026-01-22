"""Pytest configuration and shared fixtures."""

import pytest


@pytest.fixture
def sample_client_id() -> str:
    """Return a sample client ID for testing."""
    return "test-client-123"
