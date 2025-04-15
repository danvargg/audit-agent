from io import BytesIO

import requests
import streamlit as st
from docx import Document

st.title("ISO 13485:2016 Compliance Analysis")

st.sidebar.header("Upload Files")
standard_file = st.sidebar.file_uploader("Upload ISO Standard", type=["pdf"])
document_file = st.sidebar.file_uploader("Upload Document", type=["pdf"])

if st.sidebar.button("Analyze"):
    if standard_file and document_file:
        with st.spinner("Analyzing..."):
            files = {
                "standard": ("standard.pdf", standard_file, "application/pdf"),
                "document": ("document.pdf", document_file, "application/pdf"),
            }
            response = requests.post("http://127.0.0.1:8000/analyze", files=files)

            if response.status_code == 200:
                findings = response.json().get("findings", "No findings returned.")
                st.success("Analysis Complete!")

                st.markdown("# Audit Findings")
                st.markdown(findings, unsafe_allow_html=True)


                def generate_word_doc(findings_text):  # TODO: refactor
                    doc = Document()
                    doc.add_heading("Audit Findings Report", level=1)
                    doc.add_paragraph(findings_text)
                    buffer = BytesIO()
                    doc.save(buffer)
                    buffer.seek(0)
                    return buffer


                word_doc = generate_word_doc(findings)
                st.download_button(
                    label="Download Findings as Word Document",
                    data=word_doc,
                    file_name="audit_findings.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
            else:
                st.error(f"Error: {response.json().get('error', 'Unknown error')}")
    else:
        st.warning("Please upload both files.")
