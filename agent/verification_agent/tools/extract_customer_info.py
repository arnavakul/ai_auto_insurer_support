from ..state.verification_agent_state import CustomerClaimInfo
from langchain_core.tools import tool
from google import genai
from dotenv import load_dotenv  
import os

load_dotenv()

client = genai.Client(
    api_key = os.getenv("GOOGLE_API_KEY")
)

@tool
def extract_claim_info(message: str) -> CustomerClaimInfo:
    """Extract structured insurance claim information from the customer's message."""
    
    prompt = """
    You are an expert AI insurance claims processor. Your task is to analyze raw customer messages and extract structured insurance claim information into the required schema.

    ### INSTRUCTIONS:
    1. Carefully read the customer's message.
    2. Identify the type of insurance being discussed (Auto, Home, Health, etc.).
    3. Extract all relevant variables needed to process a claim, such as policy numbers, dates, descriptions, and damages.
    4. If a field is not explicitly mentioned or cannot be confidently inferred, set its value to null (or an empty list/appropriate default).
    5. Before outputting the final schema, think step-by-step inside <analysis> tags to map the raw text to the schema fields.

    ### EXTRACTION RULES:
    - **dates**: Convert all relative dates (e.g., "yesterday", "last night") or written dates into standard YYYY-MM-DD format if possible. (Assume today is {date.today{}}).
    - **claim_amount_estimated**: Extract numeric values only. Do not include currency symbols.
    - **severity**: Categorize as Low (cosmetic/minor), Medium (functional damage but safe), or High (total loss/injuries/unsafe environment).

    ### EXAMPLE WALKTHROUGH:
    User: "Someone backed into my Ford F150 last night while it was parked outside my house. The driver side door is dented bad and the window is smashed. My policy number is AUT-99218. I think it will cost about $1,500 to fix."
    - Policy Number: Found "AUT-99218"
    - Incident Date: "last night" -> Calculate based on today's date.
    - Claim Type: Auto (Ford F150, driver side door)
    - Description: Vehicle was hit while parked. Damage to driver side door and window.
    - Estimated Cost: 1500
    - Severity: Medium (smashed window makes it unsafe to leave exposed, but drivable)

    """
    
    response = client.models.generate_content(
        model = "gemini-3.1-flash-lite",
        contents=[prompt],
        config={
            "response_schema": CustomerClaimInfo,
        }
    )
        
    return CustomerClaimInfo.model_validate_json(response.text)