from agent.file_agent.state.document_info_state import DocumentInfo
from langchain_core.tools import tool
from google import genai
from dotenv import load_dotenv  
import os
import mimetypes


load_dotenv()

client = genai.Client(
    api_key = os.getenv("GOOGLE_API_KEY")
)

@tool
def extract_information(file_path: str) -> DocumentInfo:
    
    """Analyze an uploaded image and extract structured information.""" 
    
    mime_type, _ = mimetypes.guess_type(file_path)
    
    uploaded_file = client.files.upload(
        file = file_path,
        config = {
            "mime_type": mime_type
        }
    )
    
    prompt = """
    Analyze the uploaded image for an insurance claim.

    Identify the type of document or image and extract the relevant information
    that is clearly visible.

    The document_type must be exactly one of:

    FIR
    VEHICLE_DAMAGE_REPORT
    REPAIR_ESTIMATE
    DAMAGE_PHOTO
    INVALID

    Definitions:

    - FIR:
    Return FIR only when the document appears to be an official First
    Information Report, police FIR, police complaint, or police-issued
    accident report.

    - VEHICLE_DAMAGE_REPORT:
    Return VEHICLE_DAMAGE_REPORT when the document describes vehicle
    or property damage and contains sections such as damaged property,
    description of damage, involved parties, witnesses, or recommendations.
    A vehicle damage report is not an FIR unless it is clearly identified
    as an official FIR or police report.

    - REPAIR_ESTIMATE:
    Return REPAIR_ESTIMATE when the document is a workshop or repair estimate
    containing repair parts, labor, prices, line items, totals, or vendor
    information.

    - DAMAGE_PHOTO:
    Return DAMAGE_PHOTO when the image is a photograph showing physical
    damage to a vehicle or an accident scene, without being a formal report.

    - INVALID:
    Return INVALID when the image is unrelated to the insurance claim,
    blank, corrupted, or too unclear to process.

    Determine whether the image is readable.

    Set is_usable to true only when the image is relevant to an insurance
    claim and contains enough visible information for further processing.

    Extract only information that is clearly visible.

    For FIR and VEHICLE_DAMAGE_REPORT, extract accident date, accident time,
    location, vehicle details, accident description, involved parties,
    witnesses, and recommendations when available.

    For REPAIR_ESTIMATE, extract workshop, estimate date, vehicle details,
    parts, labor, prices, and total amount when available.

    For DAMAGE_PHOTO, describe the visible damage and affected areas.

    For INVALID, leave the information fields empty.

    Do not guess or invent information.
    """
    
    response = client.models.generate_content(
        model = "gemini-3.1-flash-lite",
        contents=[prompt,uploaded_file],
        config={
            "response_mime_type": "application/json",
            "response_schema": DocumentInfo,
        }
    )
        
    return DocumentInfo.model_validate_json(response.text)


#test: 


# if __name__ == "__main__":

#     file_path = r"C:\Cisco\Programming\ai_claim_assistant\agent\file_agent\tools\images.jpeg"

#     result = extract_information.invoke({
#         "file_path": file_path
#     })

#     print("\n========== RESULT ==========\n")

#     print("Document Type:", result.document_type)
#     print("Readable:", result.is_readable)
#     print("Usable:", result.is_usable)
#     print("Confidence:", result.confidence)

#     print("\nInformation:")

#     for key, value in result.information.model_dump().items():
#         print(f"  {key}: {value}")