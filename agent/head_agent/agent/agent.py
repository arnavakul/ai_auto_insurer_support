from langchain.agents import create_agent

from system_prompt import HEAD_AGENT_PROMPT
from ...llm import llm

from ..tools import (
    file_agent_tool,
    organization_agent_tool,
    cost_agent_tool,
    verification_agent_tool
)

head_agent = create_agent(
    model=llm,
    
    tools=[
        file_agent_tool,
        organization_agent_tool,
        cost_agent_tool,
        verification_agent_tool
    ],
    
    system_prompt=HEAD_AGENT_PROMPT,
)