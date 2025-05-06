"""
ClipPilot Agent for YouTube content analysis.

This agent uses the CAMEL-AI framework to interact with YouTube content via MCP.
"""

import logging
from typing import Any, Dict, List, Optional

from camel.agents import MCPAgent
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType

from src.config import Config

logger = logging.getLogger(__name__)


class ClipPilotAgent:
    """
    ClipPilot Agent that orchestrates YouTube content analysis.

    This agent uses the CAMEL-AI MCPAgent to interact with the YouTube MCP server.
    """

    def __init__(
        self,
        config: Config,
        mcp_agent: MCPAgent,
    ):
        """Initialize the ClipPilot agent."""
        self.config = config
        self.mcp_agent = mcp_agent
        logger.info("ClipPilot Agent initialized")

    async def close(self):
        """Close the agent and clean up resources."""
        await self.mcp_agent.close()
        logger.info("ClipPilot Agent closed")

    async def start(self):
        """Start the agent."""
        logger.info("ClipPilot Agent started")

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

        return ""

    async def analyze_transcript(self, transcript: str, query: str) -> Dict[str, Any]:
        """
        Analyze a transcript to identify trending content.

        Args:
            transcript: The video transcript
            query: The original search query for context

        Returns:
            Analysis results with trending topics and insights
        """
        return {"trending_topics": [], "key_insights": [], "sentiment": "neutral"}

    async def generate_report(
        self, analysis: Dict[str, Any], query: str
    ) -> Dict[str, Any]:
        """
        Generate a report with insights and highlights.

        Args:
            analysis: Analysis results with trending topics and insights
            query: The original search query for context

        Returns:
            A formatted report with insights and highlights
        """
        return {
            "title": f"Content Analysis Report: {query}",
            "summary": "This is a summary of the analysis results.",
            "trending_topics": analysis.get("trending_topics", []),
            "key_insights": analysis.get("key_insights", []),
            "daily_highlights": [],
            "sentiment_analysis": analysis.get("sentiment", "neutral"),
        }

    @classmethod
    async def create(cls, config: Config) -> "ClipPilotAgent":
        """
        Factory method to create and initialize a ClipPilotAgent.

        Args:
            config: The configuration object

        Returns:
            A fully initialized ClipPilotAgent
        """
        model = ModelFactory.create(
            model_platform=ModelPlatformType.DEFAULT,
            model_type=ModelType.DEFAULT,
        )

        mcp_agent = await MCPAgent.create(
            config_path=config.mcp_config_path,
            model=model,
            function_calling_available=False,
        )

        return cls(config, mcp_agent)
