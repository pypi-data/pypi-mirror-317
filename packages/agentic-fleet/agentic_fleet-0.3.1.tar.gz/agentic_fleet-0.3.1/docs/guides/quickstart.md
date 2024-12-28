# Quick Start Guide

This guide will help you get started with AgenticFleet quickly.

## Installation

```bash
# Install using uv (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv .venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows

# Install AgenticFleet
uv pip install -e ".[dev]"
```

## Basic Usage

### 1. Create a Configuration

```python
from agenticfleet.core import Config, LLMConfig

# Create basic configuration
config = Config(
    project_id="my_first_project",
    default_llm_config=LLMConfig(
        model="gpt-4",
        temperature=0.7
    )
)
```

### 2. Create a Fleet

```python
from agenticfleet.core import Fleet

# Initialize fleet
fleet = Fleet(config)
```

### 3. Add Agents

```python
# Add a research agent
researcher = fleet.add_agent(
    name="researcher",
    role="research specialist",
    system_message="You are a research specialist focused on gathering information."
)

# Add a planner agent
planner = fleet.add_agent(
    name="planner",
    role="planning specialist",
    system_message="You are a planning specialist focused on task organization."
)
```

### 4. Agent Communication

```python
# Direct message between agents
response = await fleet.direct_message(
    message="What should we research about AI safety?",
    sender="planner",
    recipient="researcher"
)

# Broadcast to all agents
responses = await fleet.broadcast(
    message="Let's analyze the impact of quantum computing.",
    sender="planner"
)
```

## Using Specialized Agents

### Research Agent Example

```python
from agenticfleet.agents import ResearchAgent
from agenticfleet.core import AgentConfig

# Create research agent config
research_config = AgentConfig(
    name="quantum_researcher",
    role="quantum computing specialist"
)

# Initialize research agent
researcher = ResearchAgent(research_config)

# Conduct research
findings = await researcher.research_topic(
    "quantum supremacy",
    depth=2
)

print(findings["summary"])
```

## Azure OpenAI Integration

```python
from agenticfleet.core import Config, LLMConfig

# Configure with Azure deployment
config = Config(
    project_id="azure_project",
    azure_deployment="my_deployment",
    default_llm_config=LLMConfig(
        model="gpt-4",
        temperature=0.7
    )
)
```

## Next Steps

1. Explore the [Core API Reference](../api/core.md) for detailed documentation
2. Learn about [Specialized Agents](specialized_agents.md)
3. Check out common patterns and best practices
4. Join our community for support and discussions

## Common Issues

### Authentication

Make sure to set up your environment variables:

```bash
export AZURE_OPENAI_API_KEY="your_key_here"
export AZURE_OPENAI_ENDPOINT="your_endpoint_here"
```

### Debugging

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Memory Management

Monitor agent memory usage:

```python
# Get agent memory usage
agent_memory = researcher.get_memory_usage()
print(f"Current memory usage: {agent_memory}")
```

## Best Practices

1. **Error Handling**
   ```python
   try:
       response = await agent.send("message")
   except Exception as e:
       logging.error(f"Agent communication failed: {e}")
   ```

2. **Resource Cleanup**
   ```python
   # Remove unused agents
   fleet.remove_agent("unused_agent")
   ```

3. **Configuration Management**
   ```python
   # Save configuration
   config.save("config.json")
   
   # Load configuration
   config = Config.load("config.json")
   ``` 