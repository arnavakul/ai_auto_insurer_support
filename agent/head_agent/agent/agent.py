from langchain.agents import create_agent

from ...llm import llm
from ..state.head_decision import HeadDecision

from system_prompt import HEAD_AGENT_PROMPT


head_agent = create_agent(
    model=llm,
    tools=[],
    system_prompt=HEAD_AGENT_PROMPT,
    response_format=HeadDecision
)