from ..state.head_state import HeadState
from ..tools.organization_agent_tool import organizational_agent_tool

async def organization_node(state: HeadState) -> dict: 
    
    """
    LangGraph node responsible for organizing the file data and input message from the user.
    """
    
    user_message = state.messages[-1]
    
    result = await organizational_agent_tool.ainvoke(
        {
            "user_input": user_message.content
        }
    )
    
    return {
        "organized_claim": result
    }