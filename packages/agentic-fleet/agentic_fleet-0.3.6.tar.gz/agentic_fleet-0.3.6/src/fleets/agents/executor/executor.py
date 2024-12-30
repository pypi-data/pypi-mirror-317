"""
Executor Agent implementation for task execution and monitoring
"""

from typing import Optional, Dict, Any, List
from ...core import Agent
from ...core.config import AgentConfig

class ExecutorAgent(Agent):
    """Specialized agent for task execution and monitoring"""

    DEFAULT_SYSTEM_MESSAGE = """You are an execution specialist focused on implementing plans and monitoring progress.
Your responsibilities include:
1. Executing tasks according to plans
2. Monitoring progress and tracking metrics
3. Handling errors and exceptions
4. Providing status updates
5. Adapting execution based on feedback

Always maintain detailed execution logs and handle failures gracefully.
When using tools, provide clear reasoning for your choices and document your execution process."""

    def __init__(
        self,
        config: AgentConfig,
        *,
        tools: Optional[Dict[str, Any]] = None,
        system_message: Optional[str] = None,
    ):
        """Initialize the executor agent

        Args:
            config: Agent configuration
            tools: Optional specialized execution tools
            system_message: Optional system message override
        """
        # Update tool definitions to use AutoGen's function calling format
        default_tools = [
            {
                "type": "function",
                "function": {
                    "name": "execute",
                    "description": "Execute a single task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task": {
                                "type": "object",
                                "description": "Task details and parameters"
                            }
                        },
                        "required": ["task"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "monitor",
                    "description": "Monitor execution progress",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "execution_id": {
                                "type": "string",
                                "description": "Execution identifier"
                            }
                        },
                        "required": ["execution_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "handle_error",
                    "description": "Handle execution errors",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "error": {
                                "type": "object",
                                "description": "Error details"
                            },
                            "context": {
                                "type": "object",
                                "description": "Execution context"
                            }
                        },
                        "required": ["error", "context"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "report",
                    "description": "Generate execution report",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "execution_id": {
                                "type": "string",
                                "description": "Execution identifier"
                            },
                            "metrics": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                },
                                "description": "Optional list of metrics to include"
                            }
                        },
                        "required": ["execution_id"]
                    }
                }
            }
        ]

        # Update config with tool definitions
        if not config.llm_config.tools:
            config.llm_config.tools = default_tools

        # Create tool implementations
        tool_implementations = {
            "execute": self._execute_tool,
            "monitor": self._monitor_tool,
            "handle_error": self._handle_error_tool,
            "report": self._report_tool,
        }
        if tools:
            tool_implementations.update(tools)

        super().__init__(
            config,
            tools=tool_implementations,
            system_message=system_message or self.DEFAULT_SYSTEM_MESSAGE,
        )

    async def _execute_tool(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single task

        Args:
            task: Task details and parameters

        Returns:
            Execution results
        """
        # Implement task execution
        return {"status": "not_implemented", "message": "Execution pending", "execution_id": "pending"}

    async def _monitor_tool(self, execution_id: str) -> Dict[str, Any]:
        """Monitor execution progress

        Args:
            execution_id: Execution identifier

        Returns:
            Monitoring results
        """
        # Implement monitoring logic
        return {"status": "not_implemented", "message": "Monitoring pending"}

    async def _handle_error_tool(
        self, error: Dict[str, Any], context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle execution errors

        Args:
            error: Error details
            context: Execution context

        Returns:
            Error handling results
        """
        # Implement error handling
        return {"status": "not_implemented", "message": "Error handling pending"}

    async def _report_tool(
        self, execution_id: str, metrics: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Generate execution report

        Args:
            execution_id: Execution identifier
            metrics: Optional list of metrics to include

        Returns:
            Execution report
        """
        # Implement reporting logic
        return {"status": "not_implemented", "message": "Reporting pending"}

    async def execute_plan(
        self, plan: Dict[str, Any], monitoring_interval: float = 1.0
    ) -> Dict[str, Any]:
        """Execute a complete plan

        Args:
            plan: Plan to execute
            monitoring_interval: Interval between monitoring checks in seconds

        Returns:
            Execution results
        """
        results = []
        errors = []

        # Execute each task in the plan
        for task in plan.get("tasks", []):
            try:
                # Execute task
                result = await self._execute_tool(task)
                results.append(result)

                # Monitor execution
                execution_id = result.get("execution_id")
                if result and "execution_id" in result and execution_id is not None:
                    monitoring = await self._monitor_tool(execution_id)
                    # Handle any issues
                    if monitoring.get("status") == "error":
                        error_handling = await self._handle_error_tool(
                            monitoring.get("error", {}),
                            {"task": task, "result": result},
                        )
                        errors.append(error_handling)

            except Exception as e:
                # Handle unexpected errors
                error_handling = await self._handle_error_tool(
                    {"type": "unexpected", "message": str(e)},
                    {"task": task},
                )
                errors.append(error_handling)

        # Generate final report
        report = await self._report_tool(
            plan.get("id", "unknown"),
            metrics=["duration", "success_rate", "resource_usage"],
        )

        return {
            "plan_id": plan.get("id"),
            "results": results,
            "errors": errors,
            "report": report,
            "status": "completed" if not errors else "completed_with_errors",
        }

    async def execute(self, task: str, plan: Dict[str, Any], context: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute a task according to plan.
        
        Args:
            task: Task to execute
            plan: Execution plan
            context: Conversation context
            
        Returns:
            Execution results
        """
        result = await self._execute_tool({
            "task": task,
            "plan": plan,
            "context": context
        })
        
        # Monitor execution
        if result.get("execution_id"):
            monitoring = await self._monitor_tool(result["execution_id"])
            result["monitoring"] = monitoring
            
        # Generate report
        report = await self._report_tool(
            result.get("execution_id", "unknown"),
            metrics=["duration", "success_rate", "resource_usage"]
        )
        result["report"] = report
        
        return result

    async def refine(self, result: Dict[str, Any], critique: Dict[str, Any]) -> Dict[str, Any]:
        """Refine execution results based on critique.
        
        Args:
            result: Original execution result
            critique: Critique details
            
        Returns:
            Refined execution results
        """
        # Execute refinement as a new task
        refined_result = await self._execute_tool({
            "task": "refine_result",
            "original_result": result,
            "critique": critique
        })
        
        # Monitor refinement
        if refined_result.get("execution_id"):
            monitoring = await self._monitor_tool(refined_result["execution_id"])
            refined_result["monitoring"] = monitoring
        
        return refined_result
