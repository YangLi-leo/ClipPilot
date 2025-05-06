"""
ClipPilot Agent for YouTube content analysis.

This agent uses the CAMEL-AI framework to interact with YouTube content via MCP.
It combines search and transcript extraction functionality into a single agent.
"""

import json
import logging
import re
from typing import Any, Dict, List, Optional

from camel.agents import MCPAgent
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType

from src.config import Config

logger = logging.getLogger(__name__)


class ClipPilotAgent:
    """
    ClipPilot Agent that handles YouTube search and transcript extraction.

    This agent uses the CAMEL-AI MCPAgent to interact with the YouTube MCP server
    and provides a unified interface for searching videos and extracting transcripts
    in markdown format.
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
            f"Limit to {max_results} results. Return the full JSON response."
        )
        response = await self.mcp_agent.run(prompt)

        videos = self._extract_json_from_response(response)
        if not videos or not isinstance(videos, list):
            logger.warning(f"Failed to parse search results: {response}")
            return []

        logger.info(f"Found {len(videos)} videos for query: {query}")
        return videos

    async def get_transcript(
        self, video_id: str, language: Optional[str] = None
    ) -> str:
        """
        Get the transcript of a YouTube video in markdown format.

        Args:
            video_id: The YouTube video ID
            language: Language code for the transcript

        Returns:
            The video transcript formatted as markdown
        """
        language_param = f", language: '{language}'" if language else ""
        prompt = (
            f"Use the youtube.transcripts.getTranscript tool with videoId: '{video_id}'"
            f"{language_param}. Return the full transcript text."
        )
        response = await self.mcp_agent.run(prompt)

        transcript = self._extract_transcript_from_response(response)
        if not transcript:
            logger.warning(f"Failed to extract transcript for video {video_id}")
            return ""

        markdown_transcript = self._format_transcript_as_markdown(transcript, video_id)
        logger.info(f"Successfully extracted transcript for video {video_id}")

        return markdown_transcript

    async def search_and_get_transcripts(
        self, query: str, max_results: int = 3, language: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Search for videos and get their transcripts in one operation.

        Args:
            query: The search query
            max_results: Maximum number of videos to process
            language: Language code for the transcripts

        Returns:
            A dictionary mapping video titles to their transcripts in markdown format
        """
        logger.info(
            f"Searching for videos and extracting transcripts for query: {query}"
        )

        # Search for videos
        videos = await self.search_videos(query, max_results)
        if not videos:
            logger.warning(f"No videos found for query: {query}")
            return {}

        results = {}
        for video in videos:
            video_id = self._extract_video_id(video)
            if not video_id:
                continue

            video_title = self._extract_video_title(video)
            transcript = await self.get_transcript(video_id, language)

            if transcript:
                results[video_title] = transcript

        logger.info(f"Extracted transcripts for {len(results)} videos")
        return results

    def _extract_json_from_response(self, response: str) -> Any:
        """Extract JSON data from the MCP agent response."""
        try:
            json_match = re.search(r"```json\s*([\s\S]*?)\s*```", response)
            if json_match:
                json_str = json_match.group(1)
                return json.loads(json_str)

            json_match = re.search(r"\[\s*{.*}\s*\]", response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                return json.loads(json_str)

            return json.loads(response)
        except (json.JSONDecodeError, AttributeError):
            logger.error(f"Failed to extract JSON from response: {response[:100]}...")
            return None

    def _extract_transcript_from_response(self, response: str) -> str:
        """Extract transcript text from the MCP agent response."""
        try:
            transcript_match = re.search(
                r"```(?:text|plain)?\s*([\s\S]*?)\s*```", response
            )
            if transcript_match:
                return transcript_match.group(1).strip()

            lines = response.split("\n")
            content_lines = []
            for line in lines:
                if line.startswith(
                    ("I ", "Here", "The transcript", "This is", "Using")
                ):
                    continue
                content_lines.append(line)

            return "\n".join(content_lines).strip()
        except Exception as e:
            logger.error(f"Failed to extract transcript: {e}")
            return ""

    def _format_transcript_as_markdown(self, transcript: str, video_id: str) -> str:
        """Format a transcript as markdown with timestamps and speaker segments."""
        if not transcript:
            return ""

        lines = transcript.split("\n")
        markdown_lines = [f"# Transcript for Video {video_id}\n"]

        current_speaker = None
        for line in lines:
            timestamp_match = re.search(r"[\[\(](\d{1,2}:?\d{2}:?\d{2})[\]\)]", line)

            speaker_match = re.search(r"^([A-Za-z\s]+):", line)

            if speaker_match and (
                not timestamp_match or speaker_match.start() < timestamp_match.start()
            ):
                current_speaker = speaker_match.group(1).strip()
                content = line[speaker_match.end() :].strip()
                markdown_lines.append(f"\n### {current_speaker}\n")
                if content:
                    markdown_lines.append(content)
            elif timestamp_match:
                timestamp = timestamp_match.group(1)
                content = line[timestamp_match.end() :].strip()
                markdown_lines.append(f"**[{timestamp}]** {content}")
            else:
                markdown_lines.append(line.strip())

        return "\n".join(markdown_lines)

    def _extract_video_id(self, video: Dict[str, Any]) -> Optional[str]:
        """Extract video ID from a video dictionary."""
        try:
            if "id" in video:
                if isinstance(video["id"], dict) and "videoId" in video["id"]:
                    return video["id"]["videoId"]
                elif isinstance(video["id"], str):
                    return video["id"]
            elif "videoId" in video:
                return video["videoId"]

            if "url" in video:
                url_match = re.search(
                    r"(?:youtube\.com/watch\?v=|youtu\.be/)([^&\s]+)", video["url"]
                )
                if url_match:
                    return url_match.group(1)

            return None
        except Exception as e:
            logger.error(f"Failed to extract video ID: {e}")
            return None

    def _extract_video_title(self, video: Dict[str, Any]) -> str:
        """Extract video title from a video dictionary."""
        try:
            if "snippet" in video and "title" in video["snippet"]:
                return video["snippet"]["title"]
            elif "title" in video:
                return video["title"]
            else:
                return f"Video {self._extract_video_id(video)}"
        except Exception as e:
            logger.error(f"Failed to extract video title: {e}")
            return "Unknown Video"

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
            function_calling_available=True,
        )

        return cls(config, mcp_agent)
