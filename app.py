import streamlit as st
import PyPDF2
from ai_summary import summarize_text_plain, detect_key_points, chunk_text, answer_question_cloud

st.set_page_config(page_title="📜 Contract Simplifier & Q&A", page_icon="📄", layout="wide")

# --- Custom CSS ---
st.markdown("""
<style>
/* App background & font */
.stApp {
    background: #0A0F2C;
    color: #E0E0E0;
    font-family: 'Segoe UI', sans-serif;
}

/* Glowing header with animated GIF background */
.header {
    background: url('https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3bWZ6cnRvamwyanJrMjVkdDVuNWtjcGZ5cTc0dGVjaWlvNjVsbnFuMyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/40DRc0W00UbgQ/giphy.gif') no-repeat center center;
    background-size: cover;
    padding: 2rem;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}
.header h1 {
    font-size: 3rem;
    font-weight: bold;
    color: white;
    text-shadow: 0 0 10px #00BFFF, 0 0 20px #00BFFF, 0 0 30px #00BFFF;
    margin:0;
}

/* File uploader & text area (no hover effect) */
.stFileUploader > div, .stTextArea > div {
    border:2px dashed #00BFFF !important;
    border-radius:12px;
    background: rgba(10,15,44,0.4) !important;
    color:#E0E0E0;
    transition: none !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg,#00BFFF,#1976D2) !important;
    color:#fff !important;
    border:none !important;
    padding:0.8rem 1.8rem !important;
    border-radius:12px !important;
    font-weight:600 !important;
    box-shadow:0 0 5px #00BFFF;
}
.stButton > button:hover {
    transform: scale(1.05) !important;
    box-shadow:0 0 15px #00BFFF;
}

/* Tabs */
[data-baseweb="tab-list"] button {
    color:#00BFFF !important;
    font-weight:600;
}

/* Summary & text boxes */
.stMarkdown, .stText {
    background:#0D1B3A;
    border-left:4px solid #00BFFF;
    padding:1rem;
    border-radius:12px;
    margin:0.5rem 0;
    color:#E0E0E0;
    box-shadow:0 0 10px rgba(0,191,255,0.4);
    max-height:400px;
    overflow:auto;
}

/* Footer */
.footer {
    background: linear-gradient(90deg,#0D47A1,#1976D2);
    color:white;
    padding:0.8rem 1rem;
    border-radius:12px 12px 0 0;
    text-align:center;
    box-shadow:0 4px 10px rgba(0,0,0,0.3);
    margin-top:2rem;
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<div class="header"><h1>📜 Contract Simplifier & Q&A</h1></div>', unsafe_allow_html=True)

# ------------------------------
# Input method
# ------------------------------
input_option = st.radio("Choose input method:", ["Paste Text", "Upload File"], horizontal=True)
contract_text = ""

if input_option == "Paste Text":
    contract_text = st.text_area("Paste your contract text here:", height=200)
else:
    uploaded_file = st.file_uploader("Upload a contract file (.txt or .pdf)", type=["txt", "pdf"])
    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            reader = PyPDF2.PdfReader(uploaded_file)
            contract_text = "".join([page.extract_text() + "\n" for page in reader.pages])
        else:
            contract_text = uploaded_file.read().decode("utf-8")

# ------------------------------
# Session state
# ------------------------------
if "summary" not in st.session_state: st.session_state.summary = ""
if "clauses" not in st.session_state: st.session_state.clauses = []
if "risks" not in st.session_state: st.session_state.risks = []

# ------------------------------
# Analyze Button
# ------------------------------
if st.button("🔍 Analyze Contract"):
    if not contract_text.strip():
        st.error("Please enter or upload contract text.")
    else:
        with st.spinner("⏳ Summarizing and analyzing contract..."):
            # Use cloud summarization for speed
            st.session_state.summary = summarize_text_plain(contract_text)
            st.session_state.clauses, st.session_state.risks = detect_key_points(contract_text)
            st.success("✅ Analysis complete!")

# ------------------------------
# Tabs
# ------------------------------
tabs = st.tabs(["📄 Summary", "📑 Clauses & Risks", "❓ Q&A"])

# 1️⃣ Summary
with tabs[0]:
    st.subheader("Simplified Summary")
    if st.session_state.summary:
        st.write(st.session_state.summary)
    else:
        st.info("Click 🔍 Analyze Contract to generate summary.")

# 2️⃣ Clauses & Risks
with tabs[1]:
    st.markdown("### Key Clauses")
    if st.session_state.clauses:
        for c in st.session_state.clauses:
            st.success(f"✅ {c}")
    else:
        st.info("Click 🔍 Analyze Contract to detect clauses.")

    st.markdown("### Potential Risks")
    if st.session_state.risks:
        for r in st.session_state.risks:
            st.error(f"⚠️ {r}")
    else:
        st.info("Click 🔍 Analyze Contract to detect risks.")

# 3️⃣ Q&A
with tabs[2]:
    question = st.text_input("Ask a question about this contract:", key="qa_input")
    if st.button("💬 Get Answer", key="qa_btn"):
        if not st.session_state.summary:
            st.warning("Please analyze the contract first.")
        elif question.strip():
            with st.spinner("💡 Getting answer..."):
                answer, score = answer_question_cloud(question, st.session_state.summary)
                st.markdown(f"**Answer:** {answer}")
                st.markdown(f"**Confidence:** {score*100:.2f}%")
                if score < 0.6:
                    st.warning("Low confidence — consider consulting a lawyer.")

# --- Footer ---
st.markdown('<p class="footer">Designed & Developed by Team BIJON ⚡ </p>', unsafe_allow_html=True)
