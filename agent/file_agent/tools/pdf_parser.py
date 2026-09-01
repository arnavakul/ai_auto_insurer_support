import pypdf
import pdfplumber
from langchain_core.tools import tool
from agent.file_agent.state.document_info_state import DocumentInfo
from google import genai
from dotenv import load_dotenv  
import os

load_dotenv()

client = genai.Client(
    api_key = os.getenv("GOOGLE_API_KEY")
)

@tool
def extract_information_docs(file_path: str)-> DocumentInfo: 
    """Extract text and tables from a PDF document."""
    
    extracted_text = []
#PDF reader. 
    with open(file_path, "rb") as file: 
        
        reader = pypdf.PdfReader(file)
        
        for index, page in enumerate(reader.pages):
            text = page.extract_text()
            
            if text: 
                extracted_text.append(
                    f"Page {index + 1}: \n{text}"
                )

#Tables reader
    with pdfplumber.open(file_path) as pdf: 
        
        for index, page in enumerate(pdf.pages):
            
            tables = page.extract_tables()
            for table in tables: 
                for row in table:
                    extracted_text.append(
                        str([cell for cell in row if cell is not None])
                    )
    
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=[prompt, text],
        config={
            "response_mime_type": "application/json",
            "response_schema": DocumentInfo,
        },
    )

    return DocumentInfo.model_validate_json(response.text)

# @tool
# def parse_pdf(file_path):
    
#     with open(file_path, "rb") as file: 
        
#         reader = pypdf.PdfReader(file)
        
#         for index, page in enumerate(reader.pages):
#             text = page.extract_text()
#             print(f" Page{index+1}")
#             print(text)

# @tool
# def parse_tables(file_path):
    
#     with pdfplumber.open(file_path) as pdf: 
        
#         for index, page in enumerate(pdf.pages):
            
#             tables = page.extract_tables()
#             for table in tables: 
#                 for row in table:
#                     print([cell for cell in row if cell is not None])


#test 

# if __name__ == "__main__": 
#     print(parse_pdf("mock_fir.pdf"))
#     print(parse_tables("mock_fir.pdf"))