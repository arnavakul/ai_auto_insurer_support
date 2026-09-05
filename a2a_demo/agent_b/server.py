from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)

skill = AgentSkill(
    id="echo",
    name="Echo",
    description="Receives a message and sends it back.",
    tags=["echo", "test"],
    examples=[
        "Hello Agent B",
        "Can you hear me?"
    ],
)

agent_card = AgentCard(
    name="Agent B",
    description="A simple A2A test agent.",
    url="http://localhost:8001/",
    version="1.0.0",
    capabilities=AgentCapabilities(
        streaming=False
    ),
    default_input_modes=["text"],
    default_output_modes=["text"],
    skills=[skill],
)

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore

from .executor import MyAgentExecutor


request_handler = DefaultRequestHandler(
    agent_executor=MyAgentExecutor(),
    task_store=InMemoryTaskStore(),
)

server = A2AStarletteApplication(
    agent_card=agent_card,
    http_handler=request_handler,
)

app = server.build()