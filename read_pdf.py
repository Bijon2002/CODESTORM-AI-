from PyPDF2 import PdfReader

def read_pdf(file):
    """
    Reads PDF file and returns full text.
    """
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:  # skip pages with no text
            text += page_text + "\n"
    return text

def chunk_text(text, max_words=500):
    """
    Splits text into smaller chunks for summarization.
    Yields chunks of max_words words each.
    """
    words = text.split()
    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i:i + max_words])
        if chunk.strip():  # skip empty chunks
            yield chunk

def chunk_text_by_lines(text, lines_per_chunk=15):
    """
    Splits text into chunks of N lines (default 15 lines).
    Returns a list of text chunks.
    """
    lines = text.split("\n")
    chunks = []
    for i in range(0, len(lines), lines_per_chunk):
        chunk = "\n".join(lines[i:i + lines_per_chunk])
        if chunk.strip():  # skip empty chunks
            chunks.append(chunk)
    return chunks
