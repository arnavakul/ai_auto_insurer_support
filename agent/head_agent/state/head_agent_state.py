from pydantic import BaseModel, Field
from typing import Literal

from ..state.input_state import InputState
from file_agent.state.document_info_state import DocumentInfo
from verification_agent.state.verification_agent_state import (
    CustomerClaimInfo,
    VerificationResult,
)


class CustomerInteraction(InputState):
    customer_claim: CustomerClaimInfo | None = None

    documents: list[DocumentInfo] = Field(default_factory=list)

    verification_result: VerificationResult | None = None

    next_action: Literal[
        "PROCESS_FILES",
        "VERIFY",
        "ASK_CUSTOMER",
        "COMPLETE"
    ] | None = None