# AgenticFleet

An advanced multi-agent system framework building upon Magentic-One concepts, focusing on agent collaboration and autonomous interactions.

## Features

- AutoGen AgentChat Integration
- Independent Framework Evolution
- PydanticAI for Validation
- Prompty Friendly Design

## Installation

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create and activate virtual environment
uv venv .venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows

# Install dependencies
uv pip install -e ".[dev]"
```

## Development

```bash
# Run tests
pytest

# Format code
black .
isort .

# Type checking
mypy src/

# Update dependencies
uv pip compile pyproject.toml -o requirements.txt
```

## Project Structure

```
agenticfleet/
├── src/agenticfleet/    # Main package directory
├── tests/               # Test files
├── docs/               # Documentation
│   ├── api/           # API documentation
│   └── guides/        # User guides
├── frontend/          # Frontend application
└── .github/           # GitHub specific files
    └── workflows/     # CI/CD workflows
```

## License

MIT License 