from ...file_agent.state.image_information_state import ImageInformation
from pydantic import BaseModel

class CostEstimateRequest(BaseModel):
    vehicle_details: str | None = None
    damage_description: str | None = None
    affected_areas: list[str] = []
    location: str | None = None
    existing_estimate: float | None = None
    currency: str = "INR"


class SearchResult(BaseModel):
    title: str
    url: str
    content: str