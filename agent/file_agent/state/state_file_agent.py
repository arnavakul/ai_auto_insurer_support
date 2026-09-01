from ...head_agent.state.head_agent_state import CustomerInteraction
from typing import Any
from .document_info_state import DocumentInfo
class FileAssistant(CustomerInteraction): 
    
    documents: list[DocumentInfo]