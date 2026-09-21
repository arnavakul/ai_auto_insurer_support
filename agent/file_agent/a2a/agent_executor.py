import mimetypes
import os
import tempfile

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.helpers import new_text_message
from a2a.types import Role

from ..tools.pdf_parser import extract_information_docs
from ..tools.image_tool import extract_information


def _resolve_media_type(
    raw: bytes,
    declared: str | None,
    filename: str | None,
) -> str:
    """
    Work out the real media type.
    Trust the declared type only if it is specific; otherwise sniff the
    file's first bytes, then fall back to the filename extension.
    """

    if declared and declared != "application/octet-stream":
        return declared

    if raw.startswith(b"%PDF"):
        return "application/pdf"
    if raw.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if raw.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if raw.startswith((b"GIF87a", b"GIF89a")):
        return "image/gif"
    if raw[:4] == b"RIFF" and raw[8:12] == b"WEBP":
        return "image/webp"
    if raw.startswith(b"BM"):
        return "image/bmp"
    if raw.startswith((b"II*\x00", b"MM\x00*")):
        return "image/tiff"

    guessed, _ = mimetypes.guess_type(filename or "")
    return guessed or "application/octet-stream"


class FileAgentExecutor(AgentExecutor):

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:

        print("\n==============================")
        print("FILE AGENT A2A REQUEST")
        print("==============================")

        user_input = context.get_user_input()

        print("\nUser input:")
        print(user_input)

        temporary_files = []
        results_json = []

        try:

            for part in context.message.parts:

                if not getattr(part, "raw", None):
                    continue

                raw_bytes = bytes(part.raw)

                filename = (
                    part.filename
                    or "uploaded_file"
                )

                media_type = _resolve_media_type(
                    raw_bytes,
                    part.media_type,
                    filename,
                )

                suffix = os.path.splitext(filename)[1]
                if not suffix:
                    suffix = mimetypes.guess_extension(media_type) or ""

                print("\nUploaded file:")
                print(f"Filename: {filename}")
                print(f"Declared media type: {part.media_type!r}")
                print(f"Resolved media type: {media_type}")
                print(f"Size: {len(raw_bytes)} bytes")
                print(f"First bytes: {raw_bytes[:16]!r}")

                is_pdf = media_type == "application/pdf"
                is_image = media_type.startswith("image/")

                if not (is_pdf or is_image):
                    raise ValueError(
                        f"Unsupported file type: {media_type} "
                        f"(filename={filename!r}, "
                        f"first bytes={raw_bytes[:16]!r}). "
                        "Only PDF and image files are supported."
                    )

                temp_file = tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=suffix,
                )

                temp_file.write(raw_bytes)
                temp_file.close()

                temp_path = temp_file.name
                temporary_files.append(temp_path)

                print(f"Temporary path: {temp_path}")

                if is_pdf:

                    print("\nUsing PDF extraction tool...")

                    result = extract_information_docs.invoke(
                        {
                            "file_path": temp_path
                        }
                    )

                else:

                    print("\nUsing image extraction tool...")

                    result = extract_information.invoke(
                        {
                            "file_path": temp_path
                        }
                    )

                print("\nDocument extraction completed.")

                print("\nDocumentInfo:")
                print(result)

                results_json.append(result.model_dump_json())

            if not results_json:
                raise ValueError(
                    "No processable file found in the request."
                )

            # JSON list of DocumentInfo objects (one per file)
            response = "[" + ",".join(results_json) + "]"

            await event_queue.enqueue_event(
                new_text_message(
                    response,
                    role=Role.ROLE_AGENT,
                )
            )

            print("\nA2A response sent.")

        finally:

            for file_path in temporary_files:

                try:
                    os.remove(file_path)

                    print(
                        f"\nDeleted temporary file: "
                        f"{file_path}"
                    )

                except OSError:
                    pass

    async def cancel(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:

        raise Exception(
            "Cancellation is not supported."
        )