from PyPDF2 import PdfReader

def read_pdf(file):
    """
    Reads PDF file and returns full text.
    """
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def chunk_text(text, max_words=500):
    """
    Split text into smaller chunks for summarization.
    """
    words = text.split()
    for i in range(0, len(words), max_words):
        yield " ".join(words[i:i+max_words])
