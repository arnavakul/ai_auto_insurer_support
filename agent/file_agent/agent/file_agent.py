from ....system_prompt import FILE_ASSISTANT_AGENT_PROMPT
from ...llm import llm
from langchain.agents import create_agent
from ..tools.image_tool import extract_information
from ..tools.pdf_parser import extract_information_docs
from ..state.document_info_state import DocumentInfo

file_agent = create_agent(
    model=llm,
    tools=[
        extract_information_docs,
        extract_information
    ],
    system_prompt=FILE_ASSISTANT_AGENT_PROMPT,
    state_schema = DocumentInfo
)

#Testing
# if __name__ == "__main__": 
#     print("hello world")