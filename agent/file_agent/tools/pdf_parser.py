import pypdf
import pdfplumber
from langchain_core.tools import tool

@tool
def parse_pdf(file_path):
    
    with open(file_path, "rb") as file: 
        
        reader = pypdf.PdfReader(file)
        
        for index, page in enumerate(reader.pages):
            text = page.extract_text()
            print(f" Page{index+1}")
            print(text)

@tool
def parse_tables(file_path):
    
    with pdfplumber.open(file_path) as pdf: 
        
        for index, page in enumerate(pdf.pages):
            
            tables = page.extract_tables()
            for table in tables: 
                for row in table:
                    print([cell for cell in row if cell is not None])


#test 

# if __name__ == "__main__": 
#     print(parse_pdf("mock_fir.pdf"))
#     print(parse_tables("mock_fir.pdf"))