"""
Configuration module for ClipPilot.

This module handles loading and managing configuration settings for the application.
"""

import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


class Config:
    """Configuration class for ClipPilot application."""

    def __init__(self, env_file=".env"):
        """Initialize configuration from environment variables."""
        self.base_dir = Path(__file__).parent.parent
        self.config_dir = self.base_dir / "config"

        self.mcp_config_path = str(self.config_dir / "mcp_servers_config.json")

        self.youtube_api_key = os.getenv("YOUTUBE_API_KEY")

        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.model_name = os.getenv("MODEL_NAME", "gpt-4")

        self._validate_config()

    def _validate_config(self):
        """Validate that all required configuration values are present."""
        if not self.youtube_api_key:
            logger.warning(
                "YOUTUBE_API_KEY not set. YouTube API functionality will be limited."
            )

        if not self.openai_api_key:
            logger.warning("OPENAI_API_KEY not set. LLM functionality will be limited.")

        self.config_dir.mkdir(exist_ok=True)
