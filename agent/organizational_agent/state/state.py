from pydantic import BaseModel,Field

from ...cost_estimate_agent.state.agent_state import CostEstimate
from ...file_agent.state.document_info_state import DocumentInfo
from ...verification_agent.state.verification_agent_state import CustomerClaimInfo,VerificationResult

#Input of the organizing agent
class OrganizationRequest(BaseModel):

    customer_information: CustomerClaimInfo | None = None

    documents: list[DocumentInfo] = Field(
        default_factory=list
    )

    verification_result: VerificationResult | None = None

    cost_estimate: CostEstimate | None = None

#output of the organizing agent
class OrganizedClaimPackage(BaseModel): 
    customer_information: CustomerClaimInfo | None = None
    
    documents: list[DocumentInfo] = Field(
        default_factory=list
    )
    
    verification_status: VerificationResult | None = None 
    
    cost_estimate: CostEstimate | None = None
    
    outstanding_issues: list[str] = Field (
        default_factory= list
    )
    required_actions: list[str] = Field(default_factory=list)
    overall_status: str
    summary: str
