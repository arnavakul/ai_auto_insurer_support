from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentInterface,
    AgentSkill
)

def cost_estimate_agent_card() -> AgentCard:
    
    cost_estimation_skill = AgentSkill(
        id = "cost_estimation_skill",
        name="Cost Estimation Skill",
        description=(
            "Estimates the costs of damage of the user's vehicles."
        ),
        tags=[
            "Cost Estimation",
            "web search",
            "damage images",
            "customer_message"
        ]
    )
    
    interface = AgentInterface(
        protocol_binding="JSONRPC",
        protocol_version="1.0"
    )
    
    interface.url = "http://127.0.0.1:9004/"
    
    return AgentCard(
        name="Cost Estimation Agent",
        description=("Estimates the costs of damage of the user's vehicles."
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
            cost_estimation_skill
        ],
    )