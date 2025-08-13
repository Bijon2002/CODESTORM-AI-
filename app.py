import streamlit as st
from read_pdf import read_pdf, chunk_text_by_lines
from ai_summary import summarize_text
from dotenv import load_dotenv
import concurrent.futures

load_dotenv()

# --- Page Config ---
st.set_page_config(
    page_title="📄 PDF Contract Summarizer",
    layout="wide",
    page_icon="📄"
)

# --- Custom CSS (Dark Blue + Neon) ---
st.markdown("""
<style>
.stApp {background: #0A0F2C; color: #E0E0E0; font-family: 'Segoe UI', sans-serif;}
.header {background: linear-gradient(90deg,#0D47A1,#1976D2);color:white;padding:1.5rem;border-radius:0 0 15px 15px;text-align:center;box-shadow:0 4px 10px rgba(0,0,0,0.3);margin-bottom:2rem;}
.stFileUploader > div {border:2px dashed #1976D2 !important;border-radius:12px;background:rgba(10,15,44,0.4) !important;color:#E0E0E0;transition:all 0.3s ease;}
.stFileUploader > div:hover {box-shadow:0 0 10px #1976D2;}
.stButton > button {background: linear-gradient(90deg,#0D47A1,#1976D2) !important;color:white !important;border:none !important;padding:0.8rem 1.8rem !important;border-radius:12px !important;font-weight:600 !important;transition: all 0.3s ease !important;box-shadow:0 0 5px #1976D2;}
.stButton > button:hover {transform: scale(1.05) !important; box-shadow:0 0 15px #1976D2;}
.summary-box {background:#0D1B3A; border-left:4px solid #00BFFF; padding:1rem; border-radius:12px; margin:0.5rem 0; color:#E0E0E0; box-shadow:0 0 10px rgba(0,191,255,0.4);}
.preview-box {background:#0D1B3A; padding:1rem; border-radius:12px; border-left:4px solid #58D68D; margin:1rem 0; color:#E0E0E0; box-shadow:0 0 10px rgba(88,214,141,0.3); max-height:300px; overflow:auto;}
.footer {background: linear-gradient(90deg,#0D47A1,#1976D2); color:white; padding:1rem; border-radius:15px 15px 0 0; text-align:center; margin-top:2rem; box-shadow:0 4px 10px rgba(0,0,0,0.3);}
.highlight {background-color:#FF00FF;color:#0A0F2C;font-weight:bold;}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="header">
<h1>📄 PDF Contract Summarizer</h1>
<p>Upload your PDF and get a concise AI summary of key points, obligations, and risks.</p>
</div>
""", unsafe_allow_html=True)

# --- Model selection ---
model_option = st.selectbox("Choose summarization mode:", ["Free Local Model (CPU)", "Hugging Face API"])
use_hf_api = model_option == "Hugging Face API"

# --- PDF Upload ---
uploaded_file = st.file_uploader("Upload PDF", type="pdf")
search_term_pdf = st.text_input("🔍 Find in PDF")

if uploaded_file:
    full_text = read_pdf(uploaded_file)
    st.success(f"✅ PDF loaded. First 500 chars:\n\n{full_text[:500]}")

    # --- PDF Preview with scrolling ---
    preview_text = full_text
    if search_term_pdf:
        preview_text = preview_text.replace(search_term_pdf, f"<span class='highlight'>{search_term_pdf}</span>")
    st.markdown(f"<div class='preview-box'>{preview_text}</div>", unsafe_allow_html=True)

    # --- Summarization ---
    if st.button("Generate Summary"):
        with st.spinner("⏳ Summarizing..."):

            # --- Parallel passage-wise summarization (15 lines each) ---
            chunks = list(chunk_text_by_lines(full_text, lines_per_chunk=15))
            final_summary = []
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(summarize_text, chunk, use_hf_api) for chunk in chunks]
                for future in concurrent.futures.as_completed(futures):
                    final_summary.append(future.result())

            summary_text = "\n\n".join(final_summary)

            # --- Find in Summary appears only after summarization ---
            search_term_summary = st.text_input("🔍 Find in Summary")
            summary_display = summary_text
            if search_term_summary:
                summary_display = summary_display.replace(
                    search_term_summary,
                    f"<span class='highlight'>{search_term_summary}</span>"
                )

            # --- Display summary without scrolling ---
            st.subheader("📝 AI Summary")
            st.markdown(f"<div class='summary-box'>{summary_display}</div>", unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
<div class="footer">
<p>Made with ❤️ by Team Bijon | Dark Blue Neon Theme | HCI Compliant</p>
</div>
""", unsafe_allow_html=True)
