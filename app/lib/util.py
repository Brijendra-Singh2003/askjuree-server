import fitz
import docx

# Function to extract text from PDF
def extract_text_from_pdf(file):
    text = ""
    pdf_document = fitz.open(stream=file, filetype="pdf")
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        text += page.get_text()
    return text

# Function to extract text from DOCX
def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])