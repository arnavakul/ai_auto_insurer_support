from file_agent.state.document_info_state import DocumentInfo
from head_agent.state.input_state import InputState
from pydantic import BaseModel
from typing import Literal

class Verification_State(InputState): 
    documents: list[DocumentInfo]
    
    verification_status: str
    conflicts: list
    missing_information: list
    questions_for_customer: list

class CustomerClaimInfo(BaseModel):
    accident_date: str | None = None
    accident_time: str | None = None
    location: str | None = None
    vehicle_number: str | None = None
    vehicle_details: str | None = None
    accident_description: str | None = None
    damage_description: str | None = None

class FieldComparison(BaseModel):
    field: str
    document_type: str

    customer_value: str | None
    document_value: str | None

    status: Literal[
        "MATCH",
        "CLOSE_MATCH",
        "CONFLICT",
        "MISSING",
        "UNCERTAIN"
    ]

    explanation: str

class VerificationResult(BaseModel):
    overall_status: Literal[
        "VERIFIED",
        "NEEDS_CLARIFICATION",
        "INCOMPLETE"
    ]

    comparisons: list[FieldComparison]

    questions_for_customer: list[str]