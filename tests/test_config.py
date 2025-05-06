"""
Tests for the Config module.
"""

import os

import pytest

from src.config import Config


def test_config_initialization():
    """Test that Config initializes correctly with default values."""
    os.environ["YOUTUBE_API_KEY"] = "test_youtube_key"
    os.environ["OPENAI_API_KEY"] = "test_openai_key"

    config = Config()

    assert config.youtube_api_key == "test_youtube_key"
    assert config.openai_api_key == "test_openai_key"
    assert config.model_name == "gpt-4"  # Default value


def test_config_missing_keys():
    """Test that Config handles missing keys gracefully."""
    if "YOUTUBE_API_KEY" in os.environ:
        del os.environ["YOUTUBE_API_KEY"]
    if "OPENAI_API_KEY" in os.environ:
        del os.environ["OPENAI_API_KEY"]

    config = Config()

    assert config.youtube_api_key is None
    assert config.openai_api_key is None
    assert config.model_name == "gpt-4"  # Default value should still be set
