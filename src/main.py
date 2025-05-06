"""
ClipPilot: A system for extracting and analyzing YouTube video content.

This module serves as the entry point for the ClipPilot application.
"""

import asyncio
import logging

from dotenv import load_dotenv

from src.agents.clip_pilot_agent import ClipPilotAgent
from src.config import Config

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    """Main entry point for the ClipPilot application."""
    logger.info("Starting ClipPilot application")

    load_dotenv()

    config = Config()

    agent = await ClipPilotAgent.create(config)

    try:
        await agent.start()
    finally:
        await agent.close()


if __name__ == "__main__":
    asyncio.run(main())
