from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentInterface,
    AgentSkill
)

def organization_agent_card() -> AgentCard:
    
    organization_skill = AgentSkill(
        id = "organization_skill",
        name="Organization Skill",
        description=(
            "Organizes the information and files from the user. Prepares the files for sending them for claim"
        ),
        tags=[
            "organization",
            "comparison",
            "documents",
            "customer_message"
        ]
    )
    
    interface = AgentInterface(
        protocol_binding="JSONRPC",
        protocol_version="1.0"
    )
    
    interface.url = "http://127.0.0.1:9003/"
    
    return AgentCard(
        name="Organization Agent",
        description=("Organizes the information and files from the user. Prepares the files for sending them for claim"
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
            organization_skill
        ],
    )