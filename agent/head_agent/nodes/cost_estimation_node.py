from ..state.head_state import HeadState
from ..tools.cost_agent_tool import cost_estimation_agent_tool

async def cost_estimation_node(state: HeadState) -> dict: 
    
    """
    LangGraph node responsible for estimating the cost of the damage of the user's vehicle based on the images of the accident uploaded by the user.
    """    
    result = await cost_estimation_agent_tool.ainvoke(
        {
            "user_input": str({
                "customer_claim": state.customer_claim,
                "documents": state.documents,
            })
        }
    )
    
    return {
        "cost_estimate": result
    }