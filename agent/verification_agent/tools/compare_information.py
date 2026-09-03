from langchain_core.tools import tool
from .extract_customer_info import CustomerClaimInfo
from file_agent.state.document_info_state import DocumentInfo
from ..state.verification_agent_state import FieldComparison,VerificationResult
from google import genai
from dotenv import load_dotenv  
import os

load_dotenv()

client = genai.Client(
    api_key = os.getenv("GOOGLE_API_KEY")
)


def compare_exact_field(
    field: str,
    customer_value: str | None,
    document_value: str | None,
    document_type: str
) -> FieldComparison:

    if customer_value is None and document_value is None:
        status = "MISSING"
        explanation = "The information is not available in either source."

    elif customer_value is None:
        status = "MISSING"
        explanation = "The customer did not provide this information."

    elif document_value is None:
        status = "MISSING"
        explanation = "The document does not contain this information."

    elif customer_value == document_value:
        status = "MATCH"
        explanation = "The values match."

    else:
        status = "CONFLICT"
        explanation = "The values are different."

    return FieldComparison(
        field=field,
        document_type=document_type,
        customer_value=customer_value,
        document_value=document_value,
        status=status,
        explanation=explanation
    )

@tool
def compare_information(customer: CustomerClaimInfo, document: DocumentInfo) -> list[FieldComparison]:
    """Compare customer-provided information against information extracted from a document."""
    
    prompt = f"""
    You are an insurance claim verification assistant.

    Your task is to compare information provided by a customer against
    information extracted from an insurance document.

    You must identify whether the information agrees, is missing, or conflicts.

    IMPORTANT RULES:

    1. Compare only information that is actually present in the inputs.
    2. Do not invent, infer, or assume facts that are not explicitly available.
    3. Do not accuse the customer or imply dishonesty.
    4. A missing value is NOT a conflict.
    5. Treat semantically equivalent statements as a MATCH.
    6. Minor wording differences should not automatically be treated as conflicts.
    7. Exact identifiers such as vehicle registration numbers should be treated
    strictly.
    8. Dates should be compared based on their actual calendar meaning.
    9. If two descriptions communicate the same meaning using different wording,
    classify them as MATCH.
    10. If the information is similar but there is a meaningful uncertainty,
        classify it as UNCERTAIN.
    11. If both sources contain information and the information clearly disagrees,
        classify it as CONFLICT.
    12. Return neutral explanations suitable for an insurance workflow.

    STATUS DEFINITIONS:

    MATCH:
    The customer information agrees with the document information.

    CLOSE_MATCH:
    The information is substantially similar but has a minor difference that
    may require clarification.

    CONFLICT:
    Both sources contain information but the information clearly contradicts.

    MISSING:
    One or both sources do not contain the information needed for comparison.

    UNCERTAIN:
    The available information is ambiguous or insufficient to determine whether
    the values agree.

    CUSTOMER INFORMATION:

    {customer.model_dump_json(indent=2)}

    DOCUMENT INFORMATION:

    {document.model_dump_json(indent=2)}

    DOCUMENT TYPE:

    {document.document_type}

    Compare the relevant fields between the customer information and the
    document information.

    Do not compare fields that are irrelevant to the document type.

    For every relevant field, produce a FieldComparison containing:

    - field
    - document_type
    - customer_value
    - document_value
    - status
    - explanation

    The explanation must briefly explain why the field was classified that way.

    Return only the structured output required by the schema.
    """
    
    response = client.models.generate_content(
        model = "gemini-3.1-flash-lite",
        contents=[prompt],
        config={
            "response_schema": list[FieldComparison],
        }
    )
    
    return [
        FieldComparison.model_validate(item)
        for item in response.parsed
    ]