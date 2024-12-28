"""
Run Chainlit frontend for AgenticFleet
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

# Load environment variables
load_dotenv()

# Set Chainlit environment variables
os.environ["CHAINLIT_MAX_TOKENS"] = "4096"
os.environ["CHAINLIT_TIMEOUT"] = "600"
os.environ["CHAINLIT_WEBSOCKET_PING_INTERVAL"] = "5"
os.environ["CHAINLIT_WEBSOCKET_PING_TIMEOUT"] = "10"

# Import and run Chainlit
if __name__ == "__main__":
    import chainlit as cl
    from agenticfleet.frontend.chainlit import on_message, on_chat_start, on_chat_end

    # Start the Chainlit app
    cl.run(
        host="0.0.0.0",
        port=8000,
        debug=True,
    ) 