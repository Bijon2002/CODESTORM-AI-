import os
import requests
from transformers import pipeline
import streamlit as st

@st.cache_resource
def load_local_summarizer():
    """Loads and caches the local summarizer model."""
    return pipeline("summarization", model="facebook/bart-large-cnn")

def chunk_text(text, max_words=500):
    """Splits text into word chunks."""
    words = text.split()
    for i in range(0, len(words), max_words):
        yield " ".join(words[i:i + max_words])

def summarize_text(text, use_hf_api=False):
    """
    Summarizes text either using local model or Hugging Face API.
    Handles big PDFs by chunking.
    """
    summaries = []

    if use_hf_api:
        api_key = os.getenv("HF_API_TOKEN")
        if not api_key:
            raise ValueError("Hugging Face API key not found in environment variables.")

        API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        headers = {"Authorization": f"Bearer {api_key}"}

        for chunk in chunk_text(text):
            response = requests.post(API_URL, headers=headers, json={"inputs": chunk})
            if response.status_code == 200:
                summaries.append(response.json()[0]['summary_text'])
            else:
                raise RuntimeError(f"HF API error: {response.text}")

    else:
        summarizer = load_local_summarizer()
        for chunk in chunk_text(text):
            result = summarizer(chunk, max_length=200, min_length=50, do_sample=False)
            summaries.append(result[0]['summary_text'])

    # Join all chunk summaries into one
    return " ".join(summaries)
