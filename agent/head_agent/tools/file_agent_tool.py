import base64
from uuid import uuid4

import httpx

from langchain_core.tools import tool

from a2a.client import create_client, ClientConfig
from a2a.types import Message, Part, Role, SendMessageRequest, Task


FILE_AGENT_URL = "http://127.0.0.1:9001/"

GENERIC_TYPE = "application/octet-stream"


@tool
async def file_agent_tool(
    user_input: str,
    files: list[dict],
) -> str:
    """
    Send uploaded documents to the File Agent through A2A.
    """

    return await _call_file_agent(
        user_input=user_input,
        files=files,
    )


# ------------------------------------------------------------------
# Response parsing helpers (a2a-sdk 1.x yields StreamResponse wrappers)
# ------------------------------------------------------------------

def _has(msg, field: str) -> bool:
    """Safe protobuf HasField."""
    try:
        return msg.HasField(field)
    except (ValueError, AttributeError):
        return False


def _text_from_parts(parts) -> str | None:
    for part in parts:
        if part.text:
            return part.text
    return None


def _text_from_task(task) -> str | None:
    for artifact in task.artifacts:
        text = _text_from_parts(artifact.parts)
        if text:
            return text

    if _has(task, "status") and _has(task.status, "message"):
        return _text_from_parts(task.status.message.parts)

    return None


def _extract_text(response) -> str | None:
    """Pull text out of a StreamResponse (or a bare Message/Task)."""

    if isinstance(response, Message):
        return _text_from_parts(response.parts)

    if isinstance(response, Task):
        return _text_from_task(response)

    if _has(response, "message"):
        return _text_from_parts(response.message.parts)

    if _has(response, "task"):
        return _text_from_task(response.task)

    if _has(response, "artifact_update"):
        return _text_from_parts(
            response.artifact_update.artifact.parts
        )

    if _has(response, "status_update"):
        status = response.status_update.status
        if _has(status, "message"):
            return _text_from_parts(status.message.parts)

    return None


# ------------------------------------------------------------------
# File decoding
# ------------------------------------------------------------------

def _decode_file(file: dict) -> tuple[bytes, str]:
    """
    Return (raw_bytes, media_type).
    Handles data URLs ("data:application/pdf;base64,....") and plain
    base64, and recovers the media type from the data URL when the
    caller did not provide a specific one.
    """

    file_data = file["data"]
    media_type = file.get("media_type") or GENERIC_TYPE

    if file_data.startswith("data:"):
        header, encoded = file_data.split(",", 1)

        # header looks like "data:application/pdf;base64"
        url_type = header[5:].split(";")[0].strip()

        if url_type and media_type == GENERIC_TYPE:
            media_type = url_type
    else:
        encoded = file_data

    raw_bytes = base64.b64decode(encoded)

    return raw_bytes, media_type


# ------------------------------------------------------------------
# A2A call
# ------------------------------------------------------------------

async def _call_file_agent(
    user_input: str,
    files: list[dict],
) -> str:

    httpx_client = httpx.AsyncClient(
        timeout=120.0,
    )

    client = await create_client(
        FILE_AGENT_URL,
        client_config=ClientConfig(
            streaming=False,
            httpx_client=httpx_client,
        ),
    )

    try:

        parts = [
            Part(
                text=user_input,
            )
        ]

        for file in files:

            raw_bytes, media_type = _decode_file(file)

            print(
                f"[file_agent_tool] sending "
                f"{file.get('filename')!r} "
                f"type={media_type!r} size={len(raw_bytes)} "
                f"head={raw_bytes[:8]!r}"
            )

            parts.append(
                Part(
                    raw=raw_bytes,
                    media_type=media_type,
                    filename=file.get(
                        "filename",
                        "uploaded_file",
                    ),
                )
            )

        message = Message(
            message_id=uuid4().hex,
            role=Role.ROLE_USER,
            parts=parts,
        )

        request = SendMessageRequest(
            message=message,
        )

        responses = []

        async for response in client.send_message(request):
            responses.append(response)

        if not responses:
            raise RuntimeError(
                "File Agent returned no A2A response."
            )

        # Take the last response that actually carries text
        for response in reversed(responses):
            text = _extract_text(response)
            if text:
                return text

        raise RuntimeError(
            "File Agent responded but no text payload was found: "
            f"{[type(r).__name__ for r in responses]}"
        )

    finally:

        await client.close()
        await httpx_client.aclose()