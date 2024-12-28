# REST API Reference

The AgenticFleet API provides endpoints for managing fleets of agents and their interactions.

## Authentication

Authentication is handled through Azure AD. Ensure you have the following environment variables set:
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_ENDPOINT`

Or use Azure AD credentials through `DefaultAzureCredential`.

## Endpoints

### Create Fleet

```http
POST /fleets
```

Create a new fleet of agents.

#### Request Body

```json
{
  "project_id": "string",
  "azure_config": {
    "deployment": "string",
    "api_key": "string",  // Optional
    "endpoint": "string",  // Optional
    "api_version": "string",  // Optional
    "embedding_deployment": "string"  // Optional
  },
  "default_llm_config": {  // Optional
    "model": "string",
    "temperature": 0.7,
    "max_tokens": 1000,
    "stop_sequences": ["string"]
  }
}
```

#### Response

```json
{
  "project_id": "string",
  "agents": [],
  "status": "created"
}
```

### Add Agent

```http
POST /fleets/{project_id}/agents
```

Add an agent to an existing fleet.

#### Request Body

```json
{
  "name": "string",
  "role": "string",
  "agent_type": "string",
  "system_message": "string"  // Optional
}
```

#### Response

```json
{
  "project_id": "string",
  "agents": ["string"],
  "status": "agent_added"
}
```

### Broadcast Message

```http
POST /fleets/{project_id}/broadcast
```

Broadcast a message to all agents in the fleet.

#### Request Body

```json
{
  "message": "string",
  "sender": "string",
  "exclude": ["string"]  // Optional
}
```

#### Response

```json
{
  "responses": {
    "agent_name": "response"
  },
  "status": "broadcast_complete"
}
```

### Direct Message

```http
POST /fleets/{project_id}/direct
```

Send a direct message between agents.

#### Request Body

```json
{
  "message": "string",
  "sender": "string",
  "recipient": "string"
}
```

#### Response

```json
{
  "responses": {
    "recipient": "response"
  },
  "status": "message_sent"
}
```

### Get Fleet Info

```http
GET /fleets/{project_id}
```

Get information about a fleet.

#### Response

```json
{
  "project_id": "string",
  "agents": ["string"],
  "status": "active"
}
```

### Delete Fleet

```http
DELETE /fleets/{project_id}
```

Delete a fleet.

#### Response

```json
{
  "status": "deleted"
}
```

## Error Handling

The API uses standard HTTP status codes:

- `200`: Success
- `400`: Bad Request
- `404`: Not Found
- `500`: Internal Server Error

Error responses include a detail message:

```json
{
  "detail": "Error message"
}
```

## Examples

### Creating a Fleet

```python
import requests

response = requests.post("http://localhost:8000/fleets", json={
    "project_id": "my_project",
    "azure_config": {
        "deployment": "gpt-4",
        "embedding_deployment": "text-embedding-large"
    }
})
print(response.json())
```

### Adding an Agent

```python
import requests

response = requests.post("http://localhost:8000/fleets/my_project/agents", json={
    "name": "researcher",
    "role": "research specialist",
    "agent_type": "researcher",
    "system_message": "You are a research specialist..."
})
print(response.json())
```

### Broadcasting a Message

```python
import requests

response = requests.post("http://localhost:8000/fleets/my_project/broadcast", json={
    "message": "What should we research about AI safety?",
    "sender": "coordinator"
})
print(response.json())
```

## Rate Limiting

The API implements rate limiting based on Azure OpenAI quotas. Ensure your requests stay within these limits to avoid throttling. 