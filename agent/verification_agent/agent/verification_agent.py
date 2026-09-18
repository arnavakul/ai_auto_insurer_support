from ....system_prompt import VERIFICATION_AGENT_PROMPT
from langchain.agents import create_agent
from ..tools.extract_customer_info import extract_claim_info
from ..tools.compare_information import compare_information
from ..state.verification_agent_state import VerificationResult
from ...llm import llm

verification_agent = create_agent(
    model=llm,
    tools=[
        extract_claim_info,
        compare_information
    ],
    system_prompt=VERIFICATION_AGENT_PROMPT,
    response_format = VerificationResult
)

#Testing
# if __name__ == "__main__": 
#     print("hello world")