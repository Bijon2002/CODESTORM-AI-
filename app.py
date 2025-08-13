import streamlit as st
from read_pdf import read_pdf
from ai_summary import summarize_text

st.title("📄 PDF Contract Summarizer (Free HF Model)")
st.write("Upload your PDF and get a concise summary with key points, obligations, and risks.")

pdf_file = st.file_uploader("Upload PDF", type="pdf")

if pdf_file:
    with st.spinner("Reading PDF..."):
        pdf_text = read_pdf(pdf_file)
        st.write("✅ PDF loaded. First 500 chars:")
        st.write(pdf_text[:500])

    if st.button("Generate Summary"):
        with st.spinner("Summarizing with AI..."):
            summary = summarize_text(pdf_text)
            st.subheader("📝 AI Summary")
            st.write(summary)
