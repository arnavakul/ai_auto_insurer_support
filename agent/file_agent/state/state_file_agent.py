from ...head_agent.state.head_state import HeadState
from typing import Any
from .document_info_state import DocumentInfo
class FileAssistant(HeadState): 
    
    documents: list[DocumentInfo]