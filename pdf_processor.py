import PyPDF2
from io import BytesIO

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract selectable text from a bounded, non-encrypted PDF."""
    try:
        if not pdf_bytes:
            raise ValueError("The uploaded PDF is empty")
        if len(pdf_bytes) > 15 * 1024 * 1024:
            raise ValueError("The PDF is larger than the 15 MB demo limit")

        pdf_file = BytesIO(pdf_bytes)
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        if pdf_reader.is_encrypted:
            raise ValueError("Password-protected PDFs are not supported")
        if len(pdf_reader.pages) > 100:
            raise ValueError("The PDF has more than the 100-page demo limit")
        
        pages = []
        for page in pdf_reader.pages:
            pages.append(page.extract_text() or "")
        
        text = "\n".join(pages).strip()
        if not text:
            raise ValueError("No selectable text was found. Please upload a text-based PDF rather than a scan")
        return text
    except Exception as e:
        raise ValueError(f"PDF processing error: {str(e)}") from e
