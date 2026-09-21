from langchain_core.messages import HumanMessage
from pydantic import TypeAdapter

from agent.file_agent.state.document_info_state import DocumentInfo

from ..state.head_state import HeadState
from ..tools.file_agent_tool import file_agent_tool


async def file_node(state: HeadState) -> dict:

    if not state.messages:
        raise ValueError("No messages found.")

    message = state.messages[-1]

    if not isinstance(message, HumanMessage):
        raise ValueError("Latest message is not a human message.")

    user_input = ""
    files = []

    content = message.content

    if isinstance(content, str):

        user_input = content

    elif isinstance(content, list):

        for part in content:

            if not isinstance(part, dict):
                continue

            if part.get("type") == "text":

                user_input += part.get("text", "")

            elif part.get("type") == "file":

                file_info = part.get("file", {})

                files.append(
                    {
                        "filename": file_info.get(
                            "filename",
                            "uploaded_file",
                        ),
                        "media_type": file_info.get(
                            "mime_type",
                            "application/octet-stream",
                        ),
                        "data": file_info.get(
                            "file_data",
                            "",
                        ),
                    }
                )

    if not files:

        raise ValueError(
            "No documents were uploaded. "
            "Please upload the required claim documents."
        )

    result = await file_agent_tool.ainvoke(
        {
            "user_input": user_input,
            "files": files,
        }
    )

    # The File Agent returns a JSON list: one DocumentInfo per file.
    documents = TypeAdapter(list[DocumentInfo]).validate_json(result)

    return {
        "documents": documents,
    }