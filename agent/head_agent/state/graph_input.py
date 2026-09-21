from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field


class GraphInput(BaseModel):
    messages: list[BaseMessage] = Field(default_factory=list)