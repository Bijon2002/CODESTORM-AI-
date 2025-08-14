import os
import requests
from dotenv import load_dotenv
load_dotenv()


HF_API_TOKEN = os.getenv("HF_API_TOKEN")  # Your Hugging Face token
HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}

# ------------------------------
# Chunk text
# ------------------------------
def chunk_text(text, max_words=500):
    words = text.split()
    for i in range(0, len(words), max_words):
        yield " ".join(words[i:i + max_words])

# ------------------------------
# Simplify legal language
# ------------------------------
def simplify_language(text):
    replacements = {
        "hereinafter": "from now on",
        "heretofore": "until now",
        "pursuant to": "under",
        "shall": "must",
        "terminate": "end",
        "null and void": "no longer valid",
        "notwithstanding": "despite",
        "forthwith": "immediately",
        "in witness whereof": "as proof",
        "indemnify": "protect against losses",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

# ------------------------------
# Summarization using HF API
# ------------------------------
def summarize_text_plain(text):
    API_URL_SUM = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    summaries = []
    for chunk in chunk_text(text):
        response = requests.post(API_URL_SUM, headers=HEADERS, json={"inputs": chunk})
        if response.status_code == 200:
            summaries.append(response.json()[0]['summary_text'])
        else:
            summaries.append("Error in summarization chunk.")
    joined = " ".join(summaries)
    return simplify_language(joined)

# ------------------------------
# Detect key clauses & risks
# ------------------------------
def detect_key_points(text):
    clauses, risks = [], []
    lower = text.lower()
    if "penalty" in lower or "fine" in lower:
        clauses.append("Penalty or fine mentioned.")
    if "auto-renew" in lower or "automatic renewal" in lower:
        clauses.append("Contract auto-renews.")
    if "exclusive" in lower:
        clauses.append("Exclusive arrangement.")
    if "non-refundable" in lower:
        clauses.append("Payment is non-refundable.")

    if "cannot terminate" in lower or "no termination" in lower:
        risks.append("Contract may be hard to terminate early.")
    if "one-sided" in lower or "sole discretion" in lower:
        risks.append("One-sided clause — favors one party.")
    if "indemnify" in lower:
        risks.append("Indemnity clause — you take on extra liability.")
    return clauses, risks

# ------------------------------
# Hugging Face Q&A
# ------------------------------
def answer_question_cloud(question, context):
    API_URL_QA = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
    payload = {"inputs": {"question": question, "context": context}}
    response = requests.post(API_URL_QA, headers=HEADERS, json=payload)
    if response.status_code == 200:
        ans = response.json()
        if isinstance(ans, list):
            ans = ans[0]  # handle list responses
        return ans.get('answer', 'No answer found'), ans.get('score', 0)
    else:
        return "Error in QA", 0
