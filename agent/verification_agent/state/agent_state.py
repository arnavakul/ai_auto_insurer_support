from file_agent.state.state_file_agent import CustomerInteraction
from head_agent.state.input_state import InputState
from typing import Any

class Verification_State(InputState): 
    documents: list[Any]
    
    verification_status: str
    conflicts: list
    missing_information: list
    questions_for_customer: list