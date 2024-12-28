"""
FastAPI application for fleet management
"""

from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

from ..core import Fleet, Config, AgentConfig, LLMConfig
from ..llm.azure import AzureConfig, initialize_azure, get_azure_client


app = FastAPI(
    title="AgenticFleet API",
    description="API for managing agent fleets",
    version="0.1.0",
)


# API Models
class CreateFleetRequest(BaseModel):
    """Request model for fleet creation"""
    project_id: str
    azure_config: AzureConfig
    default_llm_config: Optional[LLMConfig] = None


class AddAgentRequest(BaseModel):
    """Request model for adding an agent"""
    name: str
    role: str
    agent_type: str
    system_message: Optional[str] = None


class MessageRequest(BaseModel):
    """Request model for sending messages"""
    message: str
    sender: str
    recipient: Optional[str] = None
    exclude: Optional[List[str]] = None


class FleetResponse(BaseModel):
    """Response model for fleet operations"""
    project_id: str
    agents: List[str]
    status: str


class MessageResponse(BaseModel):
    """Response model for message operations"""
    responses: Dict[str, str]
    status: str


# Fleet storage
fleets: Dict[str, Fleet] = {}


def get_fleet(project_id: str) -> Fleet:
    """Get fleet by project ID

    Args:
        project_id: Project identifier

    Returns:
        Fleet instance

    Raises:
        HTTPException: If fleet not found
    """
    if project_id not in fleets:
        raise HTTPException(status_code=404, detail="Fleet not found")
    return fleets[project_id]


@app.post("/fleets", response_model=FleetResponse)
async def create_fleet(request: CreateFleetRequest):
    """Create a new fleet

    Args:
        request: Fleet creation request

    Returns:
        Fleet details
    """
    if request.project_id in fleets:
        raise HTTPException(status_code=400, detail="Fleet already exists")

    # Initialize Azure client
    initialize_azure(request.azure_config)

    # Create fleet configuration
    config = Config(
        project_id=request.project_id,
        azure_deployment=request.azure_config.deployment,
        default_llm_config=request.default_llm_config or LLMConfig(),
    )

    # Create fleet
    fleet = Fleet(config)
    fleets[request.project_id] = fleet

    return FleetResponse(
        project_id=request.project_id,
        agents=[],
        status="created",
    )


@app.post("/fleets/{project_id}/agents", response_model=FleetResponse)
async def add_agent(project_id: str, request: AddAgentRequest):
    """Add an agent to a fleet

    Args:
        project_id: Project identifier
        request: Agent creation request

    Returns:
        Updated fleet details
    """
    fleet = get_fleet(project_id)

    # Add agent to fleet
    fleet.add_agent(
        name=request.name,
        role=request.role,
        system_message=request.system_message,
    )

    return FleetResponse(
        project_id=project_id,
        agents=fleet.list_agents(),
        status="agent_added",
    )


@app.post("/fleets/{project_id}/broadcast", response_model=MessageResponse)
async def broadcast_message(
    project_id: str,
    request: MessageRequest,
    fleet: Fleet = Depends(get_fleet),
):
    """Broadcast message to fleet agents

    Args:
        project_id: Project identifier
        request: Message request
        fleet: Fleet instance

    Returns:
        Message responses
    """
    responses = await fleet.broadcast(
        message=request.message,
        sender=request.sender,
        exclude=request.exclude,
    )

    return MessageResponse(
        responses=responses,
        status="broadcast_complete",
    )


@app.post("/fleets/{project_id}/direct", response_model=MessageResponse)
async def direct_message(
    project_id: str,
    request: MessageRequest,
    fleet: Fleet = Depends(get_fleet),
):
    """Send direct message between agents

    Args:
        project_id: Project identifier
        request: Message request
        fleet: Fleet instance

    Returns:
        Message response
    """
    if not request.recipient:
        raise HTTPException(status_code=400, detail="Recipient required")

    response = await fleet.direct_message(
        message=request.message,
        sender=request.sender,
        recipient=request.recipient,
    )

    return MessageResponse(
        responses={request.recipient: response},
        status="message_sent",
    )


@app.get("/fleets/{project_id}", response_model=FleetResponse)
async def get_fleet_info(project_id: str, fleet: Fleet = Depends(get_fleet)):
    """Get fleet information

    Args:
        project_id: Project identifier
        fleet: Fleet instance

    Returns:
        Fleet details
    """
    return FleetResponse(
        project_id=project_id,
        agents=fleet.list_agents(),
        status="active",
    )


@app.delete("/fleets/{project_id}")
async def delete_fleet(project_id: str):
    """Delete a fleet

    Args:
        project_id: Project identifier

    Returns:
        Deletion status
    """
    if project_id not in fleets:
        raise HTTPException(status_code=404, detail="Fleet not found")

    del fleets[project_id]
    return {"status": "deleted"} 