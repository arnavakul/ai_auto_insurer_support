from pydantic import BaseModel, Field
from typing import Literal

from ..state.input_state import InputState
from file_agent.state.document_info_state import DocumentInfo
from verification_agent.state.verification_agent_state import (
    CustomerClaimInfo,
    VerificationResult,
)

from ...cost_estimate_agent.state.agent_state import CostEstimate
from ...organizational_agent.state.state import OrganizedClaimPackage
class CustomerInteraction(InputState):
    customer_claim: CustomerClaimInfo | None = None

    documents: list[DocumentInfo] = Field(default_factory=list)

    verification_result: VerificationResult | None = None

    cost_estimate: CostEstimate | None = None

    organized_claim: OrganizedClaimPackage | None = None
    next_action: str | None = None