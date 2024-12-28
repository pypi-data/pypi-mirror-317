# Core API Reference

## Agent

The `Agent` class is the foundation of AgenticFleet, providing base functionality for all specialized agents.

### Basic Usage

```python
from agenticfleet.core import Agent, AgentConfig

config = AgentConfig(
    name="my_agent",
    role="general assistant"
)

agent = Agent(config)
```

### Configuration

The `Agent` class accepts the following parameters:

- `config`: An `AgentConfig` instance containing:
  - `name`: Agent identifier
  - `role`: Agent role description
  - `llm_config`: Language model configuration
  - `tools`: Optional dictionary of available tools

- `system_message`: Optional override for the default system message
- `tools`: Optional override for the config-specified tools

### Methods

#### Message Handling

- `async send(message: str, context: Optional[Dict[str, Any]] = None) -> str`
  Sends a message to the agent and returns its response.

- `async receive(message: str, sender: Agent) -> str`
  Receives a message from another agent and returns the response.

#### Tool Management

- `add_tool(name: str, tool: Any) -> None`
  Adds a new tool to the agent's toolkit.

- `remove_tool(name: str) -> None`
  Removes a tool from the agent's toolkit.

- `get_tools() -> Dict[str, Any]`
  Returns the current set of available tools.

## Fleet

The `Fleet` class manages collections of agents and their interactions.

### Basic Usage

```python
from agenticfleet.core import Fleet, Config

config = Config(
    project_id="my_project",
    azure_deployment="my_deployment"  # Optional
)

fleet = Fleet(config)
agent = fleet.add_agent("researcher", "research specialist")
```

### Methods

#### Agent Management

- `add_agent(name: str, role: str, system_message: Optional[str] = None, tools: Optional[Dict[str, Any]] = None) -> Agent`
  Creates and adds a new agent to the fleet.

- `get_agent(name: str) -> Optional[Agent]`
  Retrieves an agent by name.

- `remove_agent(name: str) -> None`
  Removes an agent from the fleet.

- `list_agents() -> List[str]`
  Lists all agent names in the fleet.

#### Communication

- `async broadcast(message: str, sender: str, exclude: Optional[List[str]] = None) -> Dict[str, str]`
  Broadcasts a message to all agents except excluded ones.

- `async direct_message(message: str, sender: str, recipient: str) -> Optional[str]`
  Sends a direct message between two agents.

## Configuration

The configuration system uses Pydantic models for validation and type safety.

### LLMConfig

```python
class LLMConfig(BaseModel):
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 1000
    stop_sequences: Optional[list[str]] = None
```

### AgentConfig

```python
class AgentConfig(BaseModel):
    name: str
    role: str
    llm_config: LLMConfig
    tools: Optional[Dict[str, Any]] = None
```

### Config

```python
class Config(BaseModel):
    project_id: str
    azure_deployment: Optional[str] = None
    default_llm_config: LLMConfig
    agent_configs: Dict[str, AgentConfig] = {}
``` 