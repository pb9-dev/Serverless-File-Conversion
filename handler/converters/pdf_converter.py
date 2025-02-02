import fitz  # PyMuPDF
from io import BytesIO
from docx import Document

def convert_pdf_to_word(pdf_content):
    try:
        buffer = BytesIO(pdf_content)
        document = Document()
        
        pdf = fitz.open(stream=buffer, filetype="pdf")
        for page in pdf:
            text = page.get_text()
            if text:
                document.add_paragraph(text)
        
        word_buffer = BytesIO()
        document.save(word_buffer)
        word_buffer.seek(0)
        return word_buffer, None
    except Exception as e:
        return None, str(e)
