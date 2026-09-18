from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentInterface,
    AgentSkill,
)


def file_agent_card() -> AgentCard:

    file_processing_skill = AgentSkill(
        id="insurance_document_processing",
        name="Insurance Document Processing",
        description=(
            "Classifies insurance claim documents, checks readability "
            "and usability, and extracts structured information."
        ),
        tags=[
            "insurance",
            "documents",
            "claims",
            "document-processing",
        ],
        examples=[
            "Process this insurance claim document.",
            "Extract information from this repair estimate.",
            "Identify the type of this uploaded document.",
        ],
    )

    interface = AgentInterface(
        protocol_binding="JSONRPC",
        protocol_version="1.0",
    )

    interface.url = "http://127.0.0.1:9001/"

    return AgentCard(
        name="Insurance File Agent",
        description=(
            "Processes insurance claim documents and extracts "
            "structured information."
        ),
        supported_interfaces=[
            interface
        ],
        version="1.0.0",
        capabilities=AgentCapabilities(
            streaming=False,
        ),
        default_input_modes=["text"],
        default_output_modes=["text"],
        skills=[
            file_processing_skill
        ],
    )