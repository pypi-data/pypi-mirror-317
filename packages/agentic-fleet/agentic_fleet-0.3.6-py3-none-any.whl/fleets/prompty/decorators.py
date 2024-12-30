"""
Decorators for prompt tracking and observability
"""

import time
import functools
from typing import Any, Callable, Dict, Optional
from .core import get_prompt_manager


def track_prompt(
    template_name: str,
    variables_extractor: Optional[Callable[..., Dict[str, Any]]] = None,
    metadata_extractor: Optional[Callable[..., Dict[str, Any]]] = None,
):
    """Decorator for tracking prompt invocations

    Args:
        template_name: Name of the prompt template
        variables_extractor: Optional function to extract variables from args/kwargs
        metadata_extractor: Optional function to extract metadata from args/kwargs

    Returns:
        Decorator function
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            manager = get_prompt_manager()
            start_time = time.time()

            # Extract variables and metadata
            variables = {}
            if variables_extractor:
                variables = variables_extractor(*args, **kwargs)

            metadata = {}
            if metadata_extractor:
                metadata = metadata_extractor(*args, **kwargs)

            # Render prompt
            try:
                rendered_prompt = manager.render_prompt(template_name, variables)
            except (KeyError, ValueError) as e:
                metadata["error"] = str(e)
                manager.record_invocation(
                    template_name=template_name,
                    variables=variables,
                    rendered_prompt="",
                    metadata=metadata,
                )
                raise

            # Execute function
            try:
                result = await func(*args, **kwargs)
                duration_ms = (time.time() - start_time) * 1000

                # Record successful invocation
                manager.record_invocation(
                    template_name=template_name,
                    variables=variables,
                    rendered_prompt=rendered_prompt,
                    completion=str(result) if result else None,
                    duration_ms=duration_ms,
                    metadata=metadata,
                )

                return result

            except Exception as e:
                duration_ms = (time.time() - start_time) * 1000
                metadata["error"] = str(e)

                # Record failed invocation
                manager.record_invocation(
                    template_name=template_name,
                    variables=variables,
                    rendered_prompt=rendered_prompt,
                    duration_ms=duration_ms,
                    metadata=metadata,
                )
                raise

        return wrapper
    return decorator


def extract_message_variables(message_key: str = "message"):
    """Create a variables extractor for message-based functions

    Args:
        message_key: Key for message in kwargs

    Returns:
        Variables extractor function
    """
    def extractor(*args: Any, **kwargs: Any) -> Dict[str, Any]:
        return {
            "message": kwargs.get(message_key, ""),
            "role": kwargs.get("role", "user"),
        }
    return extractor


def extract_agent_metadata(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    """Extract metadata from agent-based functions

    Args:
        args: Function arguments
        kwargs: Function keyword arguments

    Returns:
        Metadata dictionary
    """
    metadata = {}
    
    # Extract agent information if available
    if args and hasattr(args[0], "name"):
        metadata["agent_name"] = args[0].name
        metadata["agent_role"] = args[0].role

    # Extract message information
    if "message" in kwargs:
        metadata["message_length"] = len(kwargs["message"])

    return metadata 