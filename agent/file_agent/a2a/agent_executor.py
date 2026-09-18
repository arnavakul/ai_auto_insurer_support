from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.helpers import new_text_message
from a2a.types import Role

from ..agent.file_agent import file_agent


class FileAgentExecutor(AgentExecutor):

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:

        user_input = context.get_user_input()

        print("\nFile Agent received input:")
        print(user_input)

        result = await file_agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_input,
                    }
                ]
            }
        )

        print("\nActual File Agent result:")
        print(result)

        print("\nResult keys:")
        print(result.keys())

        print("\nStructured response:")
        print(result.get("structured_response"))

        structured_response = result.get("structured_response")

        response = str(structured_response)

        await event_queue.enqueue_event(
            new_text_message(
                response,
                role=Role.ROLE_AGENT,
            )
        )

    async def cancel(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:

        raise Exception("Cancellation is not supported.")