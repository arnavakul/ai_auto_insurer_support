from typing import Literal
from pydantic import BaseModel, Field


class ImageInformation(BaseModel):
    accident_date: str | None = None
    accident_time: str | None = None
    location: str | None = None
    vehicle_number: str | None = None
    vehicle_details: str | None = None
    accident_description: str | None = None

    workshop: str | None = None
    estimate_date: str | None = None
    parts: list[str] = Field(default_factory=list)
    labor: str | None = None
    total_amount: str | None = None

    damage_description: str | None = None
    affected_areas: list[str] = Field(default_factory=list)

