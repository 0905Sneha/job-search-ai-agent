from pypdf import PdfReader
import io

def extract_text_from_pdf(uploaded_file):
    """
    uploaded_file: a Streamlit UploadedFile object
    """
    reader = PdfReader(io.BytesIO(uploaded_file.read()))
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text