from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentInterface,
    AgentSkill
)

def verification_agent_card() -> AgentCard:
    
    verification_skill = AgentSkill(
        id = "verification_skill",
        name="Verification Skill",
        description=(
            "Performs comparison between the information present in the official documents and the message by the user."
        ),
        tags=[
            "verification",
            "comparison",
            "documents",
            "customer_message"
        ]
    )
    
    interface = AgentInterface(
        protocol_binding="JSONRPC",
        protocol_version="1.0"
    )
    
    interface.url = "http://127.0.0.1:9002/"
    
    return AgentCard(
        name="Verification Agent",
        description=("Performs comparison between the information present in the official documents and the message by the user."
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
            verification_skill
        ],
    )