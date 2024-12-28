"""
Chainlit frontend for AgenticFleet
"""

import chainlit as cl
from chainlit.types import AskFileResponse
from agenticfleet.core.fleet import Fleet
from agenticfleet.core.config import Settings

# Initialize settings and fleet
settings = Settings()
fleet = Fleet(settings)

@cl.on_chat_start
async def on_chat_start():
    """Initialize the chat session."""
    await cl.Message(
        content="👋 Welcome to AgenticFleet! How can I help you today?",
        author="system",
    ).send()

@cl.on_message
async def on_message(message: cl.Message):
    """Handle incoming messages."""
    try:
        # Process the message with the fleet
        response = await fleet.process_message(message.content)
        
        # Send the response
        await cl.Message(
            content=response,
            author="fleet",
        ).send()
    except Exception as e:
        await cl.Message(
            content=f"❌ Error: {str(e)}",
            author="system",
        ).send()

@cl.on_chat_end
async def on_chat_end():
    """Clean up the chat session."""
    await cl.Message(
        content="👋 Thank you for using AgenticFleet! Have a great day!",
        author="system",
    ).send()

@cl.on_file_upload(accept=["text/plain", "text/markdown", "application/json", "text/yaml", "text/csv"])
async def on_file_upload(files: list[AskFileResponse]):
    """Handle file uploads."""
    try:
        for file in files:
            content = file.content.decode("utf-8")
            await cl.Message(
                content=f"📄 Processing file: {file.name}",
                author="system",
            ).send()
            
            # Process the file content with the fleet
            response = await fleet.process_message(f"Process this file content: {content}")
            
            await cl.Message(
                content=response,
                author="fleet",
            ).send()
    except Exception as e:
        await cl.Message(
            content=f"❌ Error processing file: {str(e)}",
            author="system",
        ).send() 