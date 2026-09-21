from ..state.head_state import HeadState
from ..agent.agent import head_agent


async def head_node(state: HeadState) -> dict:
    if not state.messages:
        raise ValueError("No user message was provided.")

    result = await head_agent.ainvoke(
        {
            "messages": state.messages
        }
    )

    decision = result["structured_response"]

    return {
        "next_action": decision.next_action
    }