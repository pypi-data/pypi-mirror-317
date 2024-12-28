"""
Default prompt templates for different agent types
"""

from typing import Dict
from .core import PromptTemplate, get_prompt_manager


RESEARCHER_TEMPLATES: Dict[str, PromptTemplate] = {
    "research_query": PromptTemplate(
        name="research_query",
        template="""As a research specialist, analyze the following query:
{message}

Consider:
1. Key research questions
2. Required information sources
3. Potential methodologies
4. Expected challenges

Provide a structured research plan.""",
        description="Template for analyzing research queries",
        variables={"message": "Research query to analyze"},
        tags=["research", "planning"],
    ),
    
    "analyze_findings": PromptTemplate(
        name="analyze_findings",
        template="""Analyze the following research findings:
{findings}

Focus on:
1. Key insights and patterns
2. Supporting evidence
3. Limitations and gaps
4. Potential implications

Provide a comprehensive analysis.""",
        description="Template for analyzing research findings",
        variables={"findings": "Research findings to analyze"},
        tags=["research", "analysis"],
    ),
}


PLANNER_TEMPLATES: Dict[str, PromptTemplate] = {
    "task_decomposition": PromptTemplate(
        name="task_decomposition",
        template="""Break down the following task into manageable subtasks:
{message}

Consider:
1. Dependencies between subtasks
2. Resource requirements
3. Potential risks
4. Timeline constraints

Provide a structured breakdown with estimates.""",
        description="Template for task decomposition",
        variables={"message": "Task to decompose"},
        tags=["planning", "organization"],
    ),
    
    "plan_validation": PromptTemplate(
        name="plan_validation",
        template="""Validate the following execution plan:
{plan}

Check for:
1. Completeness of tasks
2. Resource allocation
3. Timeline feasibility
4. Risk mitigation

Provide a validation report.""",
        description="Template for plan validation",
        variables={"plan": "Plan to validate"},
        tags=["planning", "validation"],
    ),
}


EXECUTOR_TEMPLATES: Dict[str, PromptTemplate] = {
    "task_execution": PromptTemplate(
        name="task_execution",
        template="""Execute the following task:
{task}

Follow these steps:
1. Verify prerequisites
2. Execute task steps
3. Monitor progress
4. Handle any issues

Provide execution status updates.""",
        description="Template for task execution",
        variables={"task": "Task to execute"},
        tags=["execution", "monitoring"],
    ),
    
    "error_handling": PromptTemplate(
        name="error_handling",
        template="""Handle the following error during task execution:
Error: {error}
Context: {context}

Steps:
1. Analyze error cause
2. Assess impact
3. Determine recovery steps
4. Implement solution

Provide error resolution details.""",
        description="Template for error handling",
        variables={
            "error": "Error details",
            "context": "Execution context",
        },
        tags=["execution", "error-handling"],
    ),
}


CRITIC_TEMPLATES: Dict[str, PromptTemplate] = {
    "result_evaluation": PromptTemplate(
        name="result_evaluation",
        template="""Evaluate the following result:
{result}

Evaluation criteria:
1. Completeness
2. Quality
3. Effectiveness
4. Areas for improvement

Provide a detailed evaluation.""",
        description="Template for result evaluation",
        variables={"result": "Result to evaluate"},
        tags=["evaluation", "feedback"],
    ),
    
    "improvement_suggestions": PromptTemplate(
        name="improvement_suggestions",
        template="""Based on the following analysis:
{analysis}

Suggest improvements in:
1. Methodology
2. Execution
3. Documentation
4. Future considerations

Provide actionable recommendations.""",
        description="Template for improvement suggestions",
        variables={"analysis": "Analysis to improve upon"},
        tags=["evaluation", "recommendations"],
    ),
}


def initialize_templates() -> None:
    """Initialize default prompt templates"""
    manager = get_prompt_manager()

    # Add researcher templates
    for template in RESEARCHER_TEMPLATES.values():
        manager.add_template(template)

    # Add planner templates
    for template in PLANNER_TEMPLATES.values():
        manager.add_template(template)

    # Add executor templates
    for template in EXECUTOR_TEMPLATES.values():
        manager.add_template(template)

    # Add critic templates
    for template in CRITIC_TEMPLATES.values():
        manager.add_template(template) 