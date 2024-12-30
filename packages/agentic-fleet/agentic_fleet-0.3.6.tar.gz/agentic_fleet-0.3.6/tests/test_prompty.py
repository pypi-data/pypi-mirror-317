"""
Tests for Prompty integration
"""

import pytest
from datetime import datetime
from unittest.mock import AsyncMock, patch
from agenticfleet.prompty.core import (
    PromptTemplate,
    PromptInvocation,
    PromptManager,
    get_prompt_manager,
)
from agenticfleet.prompty.decorators import (
    track_prompt,
    extract_message_variables,
    extract_agent_metadata,
)


@pytest.fixture
def template():
    """Create test prompt template"""
    return PromptTemplate(
        name="test_template",
        template="Hello, {name}!",
        description="Test template",
        variables={"name": "Name to greet"},
        tags=["test"],
    )


@pytest.fixture
def manager():
    """Create test prompt manager"""
    return PromptManager()


def test_prompt_template():
    """Test prompt template creation and validation"""
    template = PromptTemplate(
        name="test",
        template="Hello, {name}!",
    )
    assert template.name == "test"
    assert template.template == "Hello, {name}!"
    assert template.description is None
    assert template.variables == {}
    assert template.tags == []


def test_prompt_invocation():
    """Test prompt invocation creation"""
    invocation = PromptInvocation(
        template_name="test",
        variables={"name": "World"},
        rendered_prompt="Hello, World!",
        completion="Hi there!",
        duration_ms=100.0,
    )
    assert invocation.template_name == "test"
    assert invocation.variables == {"name": "World"}
    assert invocation.rendered_prompt == "Hello, World!"
    assert invocation.completion == "Hi there!"
    assert invocation.duration_ms == 100.0
    assert isinstance(invocation.timestamp, datetime)
    assert invocation.metadata == {}


def test_prompt_manager_templates(manager, template):
    """Test prompt manager template handling"""
    # Add template
    manager.add_template(template)
    assert manager.get_template("test_template") == template

    # Get non-existent template
    assert manager.get_template("non_existent") is None


def test_prompt_manager_render(manager, template):
    """Test prompt rendering"""
    manager.add_template(template)

    # Render with valid variables
    rendered = manager.render_prompt("test_template", {"name": "World"})
    assert rendered == "Hello, World!"

    # Render with missing template
    with pytest.raises(KeyError):
        manager.render_prompt("non_existent", {})

    # Render with missing variable
    with pytest.raises(ValueError):
        manager.render_prompt("test_template", {})


def test_prompt_manager_invocations(manager, template):
    """Test prompt invocation recording"""
    manager.add_template(template)

    # Record invocation
    invocation = manager.record_invocation(
        template_name="test_template",
        variables={"name": "World"},
        rendered_prompt="Hello, World!",
        completion="Hi!",
        duration_ms=100.0,
    )
    assert isinstance(invocation, PromptInvocation)

    # Get invocations
    invocations = manager.get_invocations()
    assert len(invocations) == 1
    assert invocations[0] == invocation

    # Get invocations with filter
    filtered = manager.get_invocations(template_name="test_template")
    assert len(filtered) == 1
    assert filtered[0] == invocation

    # Get invocations with limit
    limited = manager.get_invocations(limit=1)
    assert len(limited) == 1
    assert limited[0] == invocation


def test_prompt_manager_stats(manager, template):
    """Test prompt statistics"""
    manager.add_template(template)

    # Record invocations
    manager.record_invocation(
        template_name="test_template",
        variables={"name": "World"},
        rendered_prompt="Hello, World!",
        completion="Hi!",
        duration_ms=100.0,
    )
    manager.record_invocation(
        template_name="test_template",
        variables={"name": "User"},
        rendered_prompt="Hello, User!",
        duration_ms=200.0,
    )

    # Get statistics
    stats = manager.get_template_stats("test_template")
    assert stats["total_invocations"] == 2
    assert stats["avg_duration_ms"] == 150.0
    assert stats["completion_rate"] == 0.5
    assert isinstance(stats["last_invocation"], datetime)


def test_global_manager():
    """Test global manager instance"""
    manager = get_prompt_manager()
    assert isinstance(manager, PromptManager)
    assert get_prompt_manager() is manager


@pytest.mark.asyncio
async def test_track_prompt_decorator():
    """Test prompt tracking decorator"""
    # Create mock function
    mock_func = AsyncMock(return_value="Hello!")

    # Create decorated function
    @track_prompt(
        template_name="test",
        variables_extractor=lambda *args, **kwargs: {"name": kwargs.get("name", "")},
    )
    async def test_func(*args, **kwargs):
        return await mock_func(*args, **kwargs)

    # Add template
    manager = get_prompt_manager()
    manager.add_template(PromptTemplate(
        name="test",
        template="Hello, {name}!",
    ))

    # Call function
    result = await test_func(name="World")
    assert result == "Hello!"

    # Verify invocation
    invocations = manager.get_invocations("test")
    assert len(invocations) == 1
    assert invocations[0].variables == {"name": "World"}
    assert invocations[0].rendered_prompt == "Hello, World!"
    assert invocations[0].completion == "Hello!"


def test_variable_extractors():
    """Test variable extractor functions"""
    # Test message variables
    extractor = extract_message_variables()
    variables = extractor(message="Hello", role="user")
    assert variables == {"message": "Hello", "role": "user"}

    # Test agent metadata
    class MockAgent:
        name = "test_agent"
        role = "test_role"

    metadata = extract_agent_metadata(MockAgent(), message="Hello")
    assert metadata == {
        "agent_name": "test_agent",
        "agent_role": "test_role",
        "message_length": 5,
    } 