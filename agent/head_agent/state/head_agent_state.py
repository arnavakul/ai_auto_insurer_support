from .input_state import InputState

class CustomerInteraction(InputState):
    
    request_id: str
    documents: list 
