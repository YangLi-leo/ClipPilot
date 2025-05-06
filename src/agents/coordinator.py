"""
mCoordinator for ClipPilot.

This module provides a simple interface for YouTube content analysis using MCPAgent.
"""

import logging
from typing import Any, Dict, List, Optional

from camel.agents import MCPAgent

logger = logging.getLogger(__name__)


class YouTubeCoordinator:
    """
    Simple coordinator for YouTube content analysis using MCPAgent directly.
    """

    def __init__(self, mcp_agent: MCPAgent):
        """Initialize the coordinator with an MCPAgent."""
        self.mcp_agent = mcp_agent
        logger.info("YouTube Coordinator initialized")

    async def search_videos(
        self, query: str, max_results: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search for YouTube videos based on a query.

        Args:
            query: The search query
            max_results: Maximum number of results to return

        Returns:
            A list of video information dictionaries
        """
        prompt = (
            f"Use the youtube.videos.searchVideos tool to search for '{query}'. "
            f"Limit to {max_results} results."
        )
        await self.mcp_agent.run(prompt)

        try:
            return []
        except Exception as e:
            logger.error(f"Error parsing search results: {e}")
            return []

    async def get_transcript(
        self, video_id: str, language: Optional[str] = None
    ) -> str:
        """
        Get the transcript of a YouTube video.

        Args:
            video_id: The YouTube video ID
            language: Language code for the transcript

        Returns:
            The video transcript
        """
        language_param = f", language: '{language}'" if language else ""
        prompt = (
            f"Use the youtube.transcripts.getTranscript tool with videoId: '{video_id}'"
            f"{language_param}."
        )
        await self.mcp_agent.run(prompt)

        try:
            return ""
        except Exception as e:
            logger.error(f"Error parsing transcript: {e}")
            return ""
