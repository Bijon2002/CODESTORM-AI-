from transformers import pipeline
from read_pdf import chunk_text

# Initialize summarizer
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text):
    """
    Summarizes text in chunks and returns combined summary.
    """
    summary_chunks = []
    for chunk in chunk_text(text):
        result = summarizer(chunk, max_length=200, min_length=50, do_sample=False)
        summary_chunks.append(result[0]['summary_text'])
    return " ".join(summary_chunks)
