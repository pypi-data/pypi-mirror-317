# Specialized Agents Guide

AgenticFleet provides several specialized agents designed for specific tasks and roles. This guide covers their usage and customization.

## Available Specialized Agents

### ResearchAgent

The `ResearchAgent` specializes in information gathering and analysis.

```python
from agenticfleet.agents import ResearchAgent
from agenticfleet.core import AgentConfig

config = AgentConfig(
    name="researcher",
    role="research specialist"
)

researcher = ResearchAgent(config)
```

#### Features

- Information gathering from multiple sources
- Data analysis and synthesis
- Summarization capabilities
- Source citation and academic rigor

#### Example Usage

```python
# Basic research
findings = await researcher.research_topic("quantum computing")

# Detailed research with depth level
detailed_findings = await researcher.research_topic("quantum computing", depth=3)
```

### PlannerAgent (Coming Soon)

The `PlannerAgent` will specialize in task decomposition and planning.

- Breaking down complex tasks
- Creating execution plans
- Resource allocation
- Timeline management

### ExecutorAgent (Coming Soon)

The `ExecutorAgent` will focus on task execution and monitoring.

- Task execution
- Progress tracking
- Error handling
- Result validation

### CriticAgent (Coming Soon)

The `CriticAgent` will provide evaluation and feedback.

- Result evaluation
- Quality assessment
- Improvement suggestions
- Performance metrics

## Creating Custom Specialized Agents

You can create custom specialized agents by extending the base `Agent` class:

```python
from agenticfleet.core import Agent

class CustomAgent(Agent):
    DEFAULT_SYSTEM_MESSAGE = """
    Your custom system message here.
    Define the agent's role and responsibilities.
    """

    def __init__(self, config: AgentConfig, **kwargs):
        super().__init__(config, system_message=self.DEFAULT_SYSTEM_MESSAGE, **kwargs)

    async def custom_method(self):
        # Implement custom functionality
        pass
```

## Best Practices

1. **System Messages**
   - Keep them clear and focused
   - Define specific responsibilities
   - Include any constraints or limitations

2. **Tool Management**
   - Group related tools together
   - Document tool interfaces
   - Handle tool errors gracefully

3. **Agent Interaction**
   - Use meaningful agent names
   - Define clear communication protocols
   - Handle message failures

4. **Configuration**
   - Use appropriate temperature settings
   - Adjust max_tokens based on task
   - Configure appropriate model for the task

## Common Patterns

### Chain of Responsibility

```python
# Create a research and analysis chain
researcher = ResearchAgent(research_config)
analyzer = AnalyzerAgent(analyzer_config)
critic = CriticAgent(critic_config)

# Chain the process
research_data = await researcher.research_topic("topic")
analysis = await analyzer.analyze(research_data)
feedback = await critic.evaluate(analysis)
```

### Broadcast and Collect

```python
# Create a fleet with multiple specialized agents
fleet = Fleet(config)
fleet.add_agent("researcher", "research specialist")
fleet.add_agent("planner", "planning specialist")
fleet.add_agent("executor", "execution specialist")

# Broadcast a task and collect responses
responses = await fleet.broadcast(
    "Analyze the impact of AI on healthcare",
    sender="coordinator"
) 