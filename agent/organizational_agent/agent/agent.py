from langchain.agents import create_agent
from ....system_prompt import ORGANIZATIONAL_AGENT_PROMPT
from ...llm import llm
from ..state.state import OrganizedClaimPackage

organizing_agent = create_agent(
    model=llm, 
    tools=[],
    system_prompt=ORGANIZATIONAL_AGENT_PROMPT,
    response_format=OrganizedClaimPackage
)