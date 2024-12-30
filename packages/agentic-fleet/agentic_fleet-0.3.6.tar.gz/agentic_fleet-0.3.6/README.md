# Agentic Fleet

# Agentic Fleet

A powerful framework for building and managing fleets of AI agents.

## Vision

Agentic Fleet aims to provide a flexible and robust platform for developing and deploying sophisticated multi-agent systems. We strive to empower developers to create AI solutions that can tackle complex tasks through coordinated effort and intelligent collaboration.

## Features

- 🤖 **Multiple Agent Types**: Agentic Fleet supports a variety of specialized agents, each designed with specific capabilities:
  - **Planner**: Decomposes complex tasks into manageable steps and creates execution plans.
  - **Executor**: Executes tasks, monitors progress, and handles task completion.
  - **Researcher**: Gathers and analyzes information from various sources to support decision-making.
  - **Critic**: Evaluates the quality of work, provides feedback, and ensures adherence to standards.
  - **Video Surfer**: Analyzes video content, extracts key information, and summarizes findings.
  - **File Surfer**: Navigates and manipulates file systems, enabling agents to interact with local data.
  - **Web Surfer**: Interacts with web content, retrieves information, and automates web-based tasks.

- 🔄 **Advanced Prompt Management**: Efficiently manage and optimize agent behavior with:
  - Version control for prompts, allowing for iterative refinement and rollback.
  - Hot reloading capabilities, enabling real-time updates to prompt configurations.
  - A/B testing support for comparing the effectiveness of different prompts.
  - Metrics collection and analysis to understand prompt performance and impact.

- 🛠️ **Extensible Architecture**: Build upon a solid foundation with:
  - Modular design that promotes flexibility and maintainability.
  - Easy agent customization, allowing developers to tailor agents to specific needs.
  - Flexible tool integration, enabling agents to leverage a wide range of functionalities.
  - Robust error handling to ensure reliable operation and graceful recovery.

- 📊 **Monitoring & Analytics**: Gain insights into your agent fleet's performance with:
  - Detailed metrics tracking to monitor key performance indicators.
  - Performance analysis tools to identify bottlenecks and areas for optimization.
  - Usage statistics to understand agent activity and resource consumption.
  - Error reporting to quickly identify and address issues.

## Installation

### Using pip

```bash
pip install agentic-fleet
```

### Using PDM (recommended)

```bash
pdm add agentic-fleet
```

### Development Installation

To set up a development environment:

```bash
git clone https://github.com/yourusername/agentic-fleet.git
cd agentic-fleet
pdm install
```

## Quick Start

```python
from fleets import PlannerAgent, ExecutorAgent, ResearcherAgent

# Initialize agents
planner = PlannerAgent()
executor = ExecutorAgent()
researcher = ResearcherAgent()

# Create a task
task = "Build a web application with user authentication"

# Plan the task
plan = await planner.create_plan(task)

# Research requirements
research = await researcher.gather_information(task)

# Execute the plan
result = await executor.execute_plan(plan)
```

## Configuration

The framework can be configured using environment variables or a `.env` file:

```env
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_API_VERSION=2023-12-01
```

## Documentation

Detailed documentation is available at [docs/](https://github.com/yourusername/agentic-fleet/tree/main/docs):
- [Architecture Overview](https://github.com/yourusername/agentic-fleet/blob/main/docs/architecture.md)
- [Agent Types](https://github.com/yourusername/agentic-fleet/blob/main/docs/agents.md)
- [Prompt Management](https://github.com/yourusername/agentic-fleet/blob/main/docs/prompts.md)
- [API Reference](https://github.com/yourusername/agentic-fleet/tree/main/docs/api)

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) and our [Code of Conduct](CODE_OF_CONDUCT.md) for details on how to contribute to Agentic Fleet.

### Get Involved
- **Code of Conduct**: Please review our [Code of Conduct](CODE_OF_CONDUCT.md) to understand our community standards.

- **GitHub Issues**: Report bugs, suggest features, and see known issues.
- **GitHub Discussions**: Share ideas, ask questions, and engage with the community.

### Development Setup

1. Fork the repository
2. Create a virtual environment
3. Install dependencies:
   ```bash
   pdm install --dev
   ```
4. Run tests:
   ```bash
   pdm run pytest
   ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [AutoGen](https://microsoft.github.io/autogen/)
- Inspired by the work of the AI research community

## Support

- 📫 Email: zachary@qredence.ai
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/agentic-fleet/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/agentic-fleet/discussions)
