from ...head_agent.state.head_agent_state import CustomerInteraction
from typing import Any

class FileAssistant(CustomerInteraction): 
    
    documents: list[Any]