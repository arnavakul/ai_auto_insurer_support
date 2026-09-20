from ..state.head_state import HeadState
from ..tools.file_agent_tool import file_agent_tool


async def file_node(state: HeadState) -> dict:
    """
    LangGraph node responsible for sending the customer's
    document-processing request to the File Agent.

    The actual document processing is performed by the
    File Agent through the A2A-based tool.
    """

    conversation = "\n".join(
        f"{message.type}: {message.content}"
        for message in state.messages
    )


    result = await file_agent_tool.ainvoke(
        {
            "user_input": conversation 
        }
    )

    return {
        "documents": result
    }