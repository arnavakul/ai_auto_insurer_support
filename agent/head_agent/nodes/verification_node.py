from ..state.head_state import HeadState
from ..tools.verification_agent_tool import verification_agent_tool

async def verification_node(state: HeadState) -> dict: 
    
    """
    LangGraph node responsible for verifying the file data and input message from the user.
    """
    
    user_message = state.messages[-1]
    
    result = await verification_agent_tool.ainvoke(
        {
            "user_input": user_message.content
        }
    )
    
    return {
        "verification_result": result
    }