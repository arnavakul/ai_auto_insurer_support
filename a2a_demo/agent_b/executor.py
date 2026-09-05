from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message

from .agent import MyAgent


class MyAgentExecutor(AgentExecutor):

    def __init__(self):
        self.agent = MyAgent()  #this is my agent

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ):
        message = context.get_user_input()

        result = await self.agent.invoke(message) #This means - A2A gave us a message → give that message to our agent.

        await event_queue.enqueue_event(
            new_agent_text_message(result) # Means: Send the agent's response back through A2A.
        )

    async def cancel(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ):
        raise Exception("Cancellation not supported")