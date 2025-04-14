import PyPDF2
from openai import OpenAI

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            try:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                else:
                    print(f"Warning: Page {page} has no extractable text.")
            except Exception as e:
                print(f"Error extracting text from page {page}: {e}")
    return text


standard_pdf_path = "ISO-13485-2016.pdf"
STANDARD_TEXT = extract_text_from_pdf(standard_pdf_path)

document_path = "QP03 Rev 9.0 Design Control.pdf"
DOCUMENT_TEXT = extract_text_from_pdf(document_path)

# Other variables for your document analysis
DOCUMENT = "QP03 Rev 9.0 Design Control"
DOCUMENT_TOPIC = "Design Control Procedures"
ANALYSIS_TOPIC = "design control compliance"
ANALYSIS_SECTION = "Section 7.3 (Design and Development Control)"

MODEL = "gpt-4o-mini"


client = OpenAI()

response = client.chat.completions.create(  # TODO: top_k, temp, n
    model=MODEL,
    temperature=0.0,  # TODO: this model does not support temp 0.0
    top_p=0.9,  # Adjust the top_p as needed  # TODO: add evals
    n=1,  # Number of completions to generate
    messages=[
        {
            "role": "system",
            "content": (
                "You are a certified ISO 13485:2016 compliance auditor for medical devices. "
                "Your task is to review provided company documentation strictly against the ISO 13485:2016 standard.\n\n"
                "Guidelines:\n"
                "- **Strict Standard Adherence:** Only identify non-conformities that are clearly defined in the ISO 13485:2016 standard. Do not infer or add requirements beyond what is written in the standard.\n"
                "- **Conservative Approach:** If any evidence is ambiguous or partial, do not flag it as a non-conformity. Only report findings you are highly confident about.\n"
                "- **Structured Reporting:**\n"
                "    1. **Introduction:** Briefly summarize the review context.\n"
                "    2. **Findings:** For each non-conformity, include:\n"
                "         - **Document Section:** The exact section, paragraph, or clause where the issue is observed.\n"
                "         - **Finding:** Description of the deviation or missing element.\n"
                "         - **Standard Reference:** The exact clause or subclause from ISO 13485:2016 (with a quotation) that is not met.\n"
                "         - **Reason:** Why this issue constitutes a non-conformity.\n"
                "         - **Recommendation:** A practical recommendation to remedy the issue.\n"
                "    3. **Conclusion:** Summarize overall compliance and note if further human review is needed.\n"
                "- **Data Sources:** Base your analysis solely on the provided ISO standard text and the company document content.\n"
                "- **Tone:** Use clear, professional, and objective language suitable for a formal audit report.\n\n"
                "Now, using the provided ISO standard text and company document content, generate your audit report."
            )
        },
        {
            "role": "user",
            "content": (
                f"Document Title: '{DOCUMENT}'\n"
                f"Document Topic: {DOCUMENT_TOPIC}\n"
                f"Analysis Topic: {ANALYSIS_TOPIC}\n"
                f"Analysis Section: {ANALYSIS_SECTION}\n\n"
                "Standard Content (extracted from PDF):\n\n"
                f"{STANDARD_TEXT}\n\n"
                "Document Content:\n\n"
                f"{DOCUMENT_TEXT}"
            )
        }
    ]
)


def main():
    # Extract the response text
    audit_findings = response.choices[0].message.content

    print(audit_findings)
    # save audit_findings to txt
    with open(f"audit_findings_{MODEL}.md", "w") as f:
        f.write(audit_findings)

if __name__ == "__main__":
    main()
