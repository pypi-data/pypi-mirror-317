"""
Research Agent implementation for information gathering and analysis
"""

from typing import Optional, Dict, Any, List
from ...core import Agent
from ...core.config import AgentConfig
from ...prompty.decorators import track_prompt, extract_message_variables, extract_agent_metadata

class ResearchAgent(Agent):
    """Specialized agent for research and information gathering"""

    DEFAULT_SYSTEM_MESSAGE = """You are a research specialist focused on gathering and analyzing information.
Your responsibilities include:
1. Breaking down complex queries into research tasks
2. Gathering relevant information from provided sources
3. Analyzing and synthesizing findings
4. Providing well-structured, factual responses
5. Citing sources and maintaining academic rigor

Always maintain objectivity and highlight any limitations or uncertainties in your findings.
When using tools, provide clear reasoning for your choices and document your findings."""

    def __init__(
        self,
        config: AgentConfig,
        *,
        tools: Optional[Dict[str, Any]] = None,
        system_message: Optional[str] = None,
    ):
        """Initialize the research agent

        Args:
            config: Agent configuration
            tools: Optional specialized research tools
            system_message: Optional system message override
        """
        # Update tool definitions to use AutoGen's function calling format
        default_tools = [
            {
                "type": "function",
                "function": {
                    "name": "search",
                    "description": "Search for information using available sources",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query"
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "analyze",
                    "description": "Analyze provided data",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "data": {
                                "type": "object",
                                "description": "Data to analyze"
                            }
                        },
                        "required": ["data"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "summarize",
                    "description": "Summarize provided text",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "text": {
                                "type": "string",
                                "description": "Text to summarize"
                            },
                            "max_length": {
                                "type": "integer",
                                "description": "Optional maximum length of summary"
                            }
                        },
                        "required": ["text"]
                    }
                }
            }
        ]

        # Update config with tool definitions
        if not config.llm_config.tools:
            config.llm_config.tools = default_tools

        # Create tool implementations
        tool_implementations = {
            "search": self._search_tool,
            "analyze": self._analyze_tool,
            "summarize": self._summarize_tool,
        }
        if tools:
            tool_implementations.update(tools)

        super().__init__(
            config,
            tools=tool_implementations,
            system_message=system_message or self.DEFAULT_SYSTEM_MESSAGE,
        )

    @track_prompt(
        template_name="research_query",
        variables_extractor=extract_message_variables(),
        metadata_extractor=extract_agent_metadata,
    )
    async def _search_tool(self, query: str) -> Dict[str, Any]:
        """Search for information using available sources

        Args:
            query: Search query

        Returns:
            Search results
        """
        # Implement actual search functionality
        return {"status": "not_implemented", "message": "Search functionality pending"}

    @track_prompt(
        template_name="analyze_findings",
        variables_extractor=lambda *args, **kwargs: {"findings": str(kwargs.get("data", {}))},
        metadata_extractor=extract_agent_metadata,
    )
    async def _analyze_tool(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze provided data

        Args:
            data: Data to analyze

        Returns:
            Analysis results
        """
        # Implement actual analysis functionality
        return {"status": "not_implemented", "message": "Analysis functionality pending"}

    @track_prompt(
        template_name="research_query",
        variables_extractor=lambda *args, **kwargs: {
            "message": kwargs.get("text", ""),
            "max_length": kwargs.get("max_length", "not specified"),
        },
        metadata_extractor=extract_agent_metadata,
    )
    async def _summarize_tool(self, text: str, max_length: Optional[int] = None) -> str:
        """Summarize provided text

        Args:
            text: Text to summarize
            max_length: Optional maximum length of summary

        Returns:
            Summarized text
        """
        # Implement actual summarization functionality
        return "Summary functionality pending"

    async def research_topic(self, topic: str, depth: int = 1) -> Dict[str, Any]:
        """Conduct research on a specific topic

        Args:
            topic: Research topic
            depth: Research depth level (1-3)

        Returns:
            Research findings
        """
        # Validate depth
        if depth not in (1, 2, 3):
            raise ValueError("Research depth must be between 1 and 3")

        # Conduct research
        tasks = []
        for _ in range(depth):
            search_results = await self._search_tool(topic)
            analysis = await self._analyze_tool(search_results)
            summary = await self._summarize_tool(str(analysis))
            tasks.append({
                "search": search_results,
                "analysis": analysis,
                "summary": summary,
            })

        return {
            "topic": topic,
            "depth": depth,
            "tasks": tasks,
            "summary": await self._summarize_tool(
                "\n".join(task["summary"] for task in tasks)
            ),
        }

    async def research(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Research a topic with context.
        
        Args:
            query: Research query
            context: Additional context like plan details
            
        Returns:
            Research findings
        """
        # Search for information
        search_results = await self._search_tool(query)
        
        # Analyze findings
        analysis = await self._analyze_tool(search_results)
        
        # Create summary
        summary = await self._summarize_tool(str(analysis))
        
        return {
            "query": query,
            "findings": search_results,
            "analysis": analysis,
            "summary": summary,
            "context": context
        }
