from ..state.head_state import HeadState
from ..tools.organization_agent_tool import organizational_agent_tool

async def organization_node(state: HeadState) -> dict: 
    
    """
    LangGraph node responsible for organizing the file data and input message from the user.
    """
    
    result = await organizational_agent_tool.ainvoke(
        {
            "user_input": str({
                "customer_claim": state.customer_claim,
                "documents": state.documents,
                "verification_result": state.verification_result,
                "cost_estimate": state.cost_estimate,
            })
        }
    )
    
    return {
        "organized_claim": result
    }