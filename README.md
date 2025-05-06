# ClipPilot

ClipPilot is an open-source project that uses the CAMEL-AI framework to automatically extract and analyze YouTube video content, identify trending topics, and generate insights and daily highlights.

## Overview

ClipPilot integrates with a custom YouTube MCP server to:

1. Extract transcripts from specified YouTube videos based on user queries
2. Identify trending content within the extracted transcripts
3. Generate automated insights and daily highlights based on the trending content

The system uses the CAMEL-AI framework's MCPAgent to communicate with the YouTube MCP server for accessing YouTube data.

## Architecture

ClipPilot consists of several key components:

- **CAMEL-AI MCPAgent**: Core component that communicates with the YouTube MCP server to access YouTube data
- **YouTube MCP Server**: Provides tools for accessing YouTube data (videos, transcripts, channels, playlists)
- **YouTubeCoordinator**: Simple interface for using MCPAgent to search videos and extract transcripts

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Node.js and NPM (for YouTube MCP server)
- YouTube API key (for accessing YouTube data)
- OpenAI API key (for LLM functionality)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/YangLi-leo/ClipPilot.git
   cd ClipPilot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with your API keys:
   ```
   YOUTUBE_API_KEY=your_youtube_api_key
   OPENAI_API_KEY=your_openai_api_key
   MODEL_NAME=gpt-4  # or another model of your choice
   ```

### Usage

Basic usage example:

```python
import asyncio
from camel.agents import MCPAgent
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType
from src.agents.coordinator import YouTubeCoordinator
from src.config import Config

async def main():
    # Initialize configuration
    config = Config()
    
    # Create model backend
    model = ModelFactory.create(
        model_platform=ModelPlatformType.DEFAULT,
        model_type=ModelType.DEFAULT,
    )
    
    # Create and initialize MCP agent
    mcp_agent = await MCPAgent.create(
        config_path=config.mcp_config_path,
        model=model,
    )
    
    try:
        # Create coordinator
        coordinator = YouTubeCoordinator(mcp_agent)
        
        # Search for videos
        videos = await coordinator.search_videos("artificial intelligence trends 2025")
        
        # Get transcript for the first video
        if videos:
            video_id = videos[0].get("id", {}).get("videoId")
            if video_id:
                transcript = await coordinator.get_transcript(video_id)
                print(f"Transcript: {transcript[:500]}...")
    finally:
        # Ensure proper cleanup
        await mcp_agent.close()

# Run the main application
asyncio.run(main())
```

For more detailed usage examples, see the [examples](./examples) directory.

## Development

### Project Structure

```
ClipPilot/
├── src/                  # Source code
│   ├── agents/           # CAMEL-AI agent wrappers
│   │   ├── coordinator.py  # YouTubeCoordinator for MCPAgent
│   │   └── clip_pilot_agent.py  # ClipPilotAgent (optional wrapper)
│   ├── utils/            # Utility functions
│   ├── models/           # Model definitions and configurations
│   ├── config.py         # Configuration handling
│   └── main.py           # Main entry point
├── config/               # Configuration files
│   └── mcp_servers_config.json  # MCP server configuration
├── tests/                # Test files
├── docs/                 # Documentation
├── examples/             # Example usage
├── scripts/              # Helper scripts
├── .github/workflows/    # GitHub Actions for CI/CD
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

### Running Tests

```bash
pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please make sure your code follows the project's coding style and passes all tests.

### Code Style

This project uses:
- Black for code formatting
- isort for import sorting
- flake8 for linting
- mypy for type checking

You can run all style checks with:

```bash
black .
isort .
flake8
mypy .
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [CAMEL-AI Framework](https://github.com/camel-ai/camel) for the MCPAgent implementation
- [YouTube MCP Server](https://github.com/ZubeidHendricks/youtube-mcp-server) for YouTube integration
