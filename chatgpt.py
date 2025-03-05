import PyPDF2
from openai import OpenAI
import pandas as pd


# from processing import pdf_to_text

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


# TODO:
# top_p: This parameter controls nucleus sampling. It specifies the cumulative probability threshold for token selection.
# The model considers only the smallest set of tokens whose cumulative probability is greater than or equal to top_p.
# For example, if top_p is set to 0.9, the model will consider only the tokens that together make up 90% of the probability
# mass. This helps in generating more coherent and contextually relevant responses

# n: This parameter specifies the number of completions to generate. If n is set to 3, the model will generate three
# different completions for the given prompt. This can be useful for getting multiple variations of the response and
# selecting the best one.

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
    # temperature=0.0,  # TODO: this model does not support temp 0.0
    # top_p=0.9,  # Adjust the top_p as needed
    # n=3,  # Number of completions to generate
    messages=[
        {
            "role": "user",
            "content": (
                "You are an expert auditor specialized in regulatory standards compliance. "
                "Your role is to critically analyze documents for non-conformities, ensuring your findings are accurate, reliable, "
                "and supported by the relevant clauses of the provided standard."
            )
        },
        {
            "role": "user",
            "content": (
                f"You are provided with a document titled '{DOCUMENT}', which covers {DOCUMENT_TOPIC}. "
                f"Your task is to review this document for potential non-conformities related to {ANALYSIS_TOPIC} as specified in the provided standard. "
                f"For this analysis, focus exclusively on sections of the document that pertain to {ANALYSIS_SECTION} and ignore any other areas.\n\n"
                "For every non-conformity you identify, please provide a structured response that includes:\n\n"
                "1. **Document Section**: Clearly indicate the specific section, paragraph, or clause from the document where the issue is found.\n"
                "2. **Finding**: Describe the issue or missing element in detail, explaining what is non-compliant.\n"
                "3. **Standard Reference**: Cite the exact clause or subclause from the provided standard that is not being met.\n"
                "4. **Reason**: Explain why this issue constitutes a non-conformity under the specified standard.\n"
                "5. **Recommendation**: Provide a practical recommendation for addressing or remedying the non-conformity, if applicable.\n\n"
                "If any critical information is unclear or absent in the document, note this as a potential non-conformity and specify what information is missing. "
                "Do not assume compliance without explicit evidence.\n\n"
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

    # Convert response into a DataFrame
    # data = [line.split("|") for line in audit_findings.strip().split("\n")[1:]]
    # df = pd.DataFrame(data, columns=["Document Section", "Finding", "ISO Reference"])
    #
    # # Save the findings table
    # df.to_csv("iso_audit_findings.csv", index=False)
    # print("Audit findings saved to iso_audit_findings.csv")


if __name__ == "__main__":
    main()
