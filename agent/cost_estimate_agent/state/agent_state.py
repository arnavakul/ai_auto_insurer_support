from pydantic import BaseModel, Field
from typing import Literal
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
class CostEstimate(BaseModel):
    damaged_parts: list[str] = Field(default_factory=list)

    estimated_min: float | None = None
    estimated_max: float | None = None

    submitted_estimate: float | None = None

    currency: str = "INR"

    assessment: Literal[
        "WITHIN_EXPECTED_RANGE",
        "BELOW_EXPECTED_RANGE",
        "ABOVE_EXPECTED_RANGE",
        "INSUFFICIENT_INFORMATION",
    ]

    explanation: str

    confidence: float

    sources: list[str] = Field(default_factory=list)