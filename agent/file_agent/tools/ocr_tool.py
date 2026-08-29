from paddleocr import PaddleOCR
from langchain_core.tools import tool

ocr = PaddleOCR(
    lang="en"
)

# @tool
def extract_file_data(file_path: str) -> str:
    result = ocr.predict(file_path)
    
    extracted_text = []
    
    for page in result: 
        for line in page: 
            extracted_text.append(line)
    
    
    return "\n".join(extracted_text)

#Test
if __name__ == "__main__":
    file_path = "./images.jpeg" 
    extract_file_data(file_path)
