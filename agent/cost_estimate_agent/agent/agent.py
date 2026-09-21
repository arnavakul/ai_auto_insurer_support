from system_prompt import COST_ESTIMATE_AGENT_PROMPT
from ...llm import llm
from langchain.agents import create_agent
from ..tools.web_search import repair_estimates
from ..state.agent_state import CostEstimate

cost_agent = create_agent(
    model=llm,
    tools=[
        repair_estimates
    ],
    system_prompt=COST_ESTIMATE_AGENT_PROMPT,
    response_format = CostEstimate
)