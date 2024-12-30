"""
FastAPI application for fleet management
"""
from dotenv import load_dotenv
from typing import AsyncGenerator, List, Sequence, Tuple
from typing import Dict, List, Optional, cast, Any
from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ConfigDict
import time
import os



from autogen_agentchat.agents import BaseChatAgent
from autogen_agentchat.base import Response
from autogen_agentchat.messages import AgentEvent, ChatMessage, TextMessage
from autogen_core import CancellationToken
from ..core.config import FleetConfig, LLMConfig, AzureConfig
from ..core.fleet import Fleet
from ..core.exceptions import AgenticFleetError, FleetError
from ..frontend.example_fleet import ExampleFleet

# Load environment variables
load_dotenv()

app = FastAPI(
    title="AgenticFleet API",
    description="API for managing autonomous agent fleets",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Models
class BaseAPIModel(BaseModel):
    """Base model for all API models"""
    model_config = ConfigDict(extra='allow')

class AddAgentRequest(BaseAPIModel):
    """Request model for adding an agent"""
    name: str = Field(..., min_length=1, max_length=100)
    role: str = Field(..., min_length=1)
    agent_type: str = Field(..., pattern="^(planner|executor|critic|researcher)$")
    system_message: Optional[str] = None
    functions: Optional[List[Dict[str, Any]]] = None

class MessageRequest(BaseAPIModel):
    """Request model for sending messages"""
    message: str = Field(..., min_length=1)
    sender: str = Field(..., min_length=1)
    recipient: Optional[str] = None
    exclude: Optional[List[str]] = None
    context: Optional[Dict[str, Any]] = None

class FleetResponse(BaseAPIModel):
    """Response model for fleet operations"""
    project_id: str
    agents: List[str]
    status: str
    metadata: Optional[Dict[str, Any]] = None

class MessageResponse(BaseAPIModel):
    """Response model for message operations"""
    responses: Dict[str, str]
    status: str
    metadata: Optional[Dict[str, Any]] = None

class CreateFleetRequest(BaseAPIModel):
    """Request model for fleet creation"""
    project_id: str = Field(..., min_length=1, max_length=100)
    azure_config: AzureConfig
    llm_config: Optional[LLMConfig] = None
    system_message: Optional[str] = None

class ErrorResponse(BaseAPIModel):
    """Response model for errors"""
    detail: str
    error_type: Optional[str] = None
    timestamp: float = Field(default_factory=time.time)

# Fleet storage
fleets: Dict[str, ExampleFleet] = {}

def get_fleet(project_id: str) -> ExampleFleet:
    """Get fleet by project ID"""
    if project_id not in fleets:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fleet '{project_id}' not found"
        )
    return fleets[project_id]

@app.exception_handler(AgenticFleetError)
async def agentic_fleet_exception_handler(request: Request, exc: AgenticFleetError):
    """Handle AgenticFleet-specific exceptions"""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=ErrorResponse(
            detail=str(exc),
            error_type=exc.__class__.__name__
        ).model_dump()
    )

@app.get("/fleets", response_model=List[str])
async def list_fleets():
    """List all fleet project IDs."""
    return list(fleets.keys())

@app.get("/fleets/{project_id}/verify")
async def verify_fleet(project_id: str):
    """Verify if a fleet exists."""
    exists = project_id in fleets
    return {
        "project_id": project_id,
        "exists": exists,
        "timestamp": time.time()
    }

@app.get("/fleets/{project_id}", response_model=FleetResponse)
async def get_fleet_info(
    project_id: str,
    fleet: ExampleFleet = Depends(get_fleet)
):
    """Get fleet information."""
    try:
        agents = [agent.name for agent in [fleet.planner, fleet.executor, fleet.critic, fleet.researcher]]
        return FleetResponse(
            project_id=fleet.config.project_id,
            agents=agents,
            status="active",
            metadata={
                "agent_count": len(agents),
                "config": fleet.config.dict()
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting fleet info: {str(e)}"
        )

@app.post("/fleets/{project_id}/message", response_model=MessageResponse)
async def process_message(
    project_id: str,
    request: MessageRequest,
    fleet: ExampleFleet = Depends(get_fleet)
):
    """Process a message through the fleet"""
    try:
        response = await fleet.process_message(
            message=request.message,
            extra_context=request.context
        )
        return MessageResponse(
            responses={"content": response["content"]},
            status="processed",
            metadata={
                "plan": response.get("plan"),
                "critique": response.get("critique"),
                "metadata": response.get("metadata")
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing message: {str(e)}"
        )

@app.post("/fleets/{project_id}/reset")
async def reset_fleet(
    project_id: str,
    fleet: ExampleFleet = Depends(get_fleet)
):
    """Reset fleet state"""
    try:
        await fleet.reset()
        return {
            "status": "reset",
            "project_id": project_id,
            "timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error resetting fleet: {str(e)}"
        )

@app.delete("/fleets/{project_id}")
async def delete_fleet(project_id: str):
    """Delete a fleet"""
    try:
        if project_id not in fleets:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Fleet '{project_id}' not found"
            )

        # Cleanup fleet resources
        await fleets[project_id].reset()
        del fleets[project_id]
        
        return {
            "status": "deleted",
            "project_id": project_id,
            "timestamp": time.time()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting fleet: {str(e)}"
        )

@app.post("/fleets", response_model=FleetResponse)
async def create_fleet(request: CreateFleetRequest):
    """Create a new agent fleet"""
    try:
        if request.project_id in fleets:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Fleet '{request.project_id}' already exists"
            )

        # Create fleet configuration
        config = FleetConfig(
            project_id=request.project_id,
            llm_config=request.llm_config or LLMConfig(
                model=request.azure_config.deployment,
                temperature=0.7,
                max_tokens=2000
            ),
            use_azure=True,
            system_message=request.system_message
        )
        
        # Create and store fleet
        fleet = ExampleFleet()
        fleet.config = config
        fleets[request.project_id] = fleet
        
        return FleetResponse(
            project_id=request.project_id,
            agents=[],
            status="created",
            metadata={
                "config": config.dict(),
                "timestamp": time.time()
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create fleet: {str(e)}"
        )
