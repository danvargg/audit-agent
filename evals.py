import PyPDF2
from openai import OpenAI
import pandas as pd


# --- Reused Functions ---
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


# --- Set Up Your ISO Standard and Document Texts ---
standard_pdf_path = "ISO-13485-2016.pdf"
STANDARD_TEXT = extract_text_from_pdf(standard_pdf_path)

document_path = "QP03 Rev 9.0 Design Control.pdf"
DOCUMENT_TEXT = extract_text_from_pdf(document_path)

# --- Configuration Variables ---
DOCUMENT = "QP03 Rev 9.0 Design Control"
DOCUMENT_TOPIC = "Design Control Procedures"
ANALYSIS_TOPIC = "design control compliance"
ANALYSIS_SECTION = "Section 7.3 (Design and Development Control)"
# Recommended model; here we assume using Anthropic's Claude variant.
MODEL = "claude-v1.2"  # Adjust as needed

# Initialize your client (update API keys or config as needed)
client = OpenAI()

# --- Evals: Define Test Cases ---
# Each test case includes:
# - a name (for logging)
# - document details
# - standard and document content (for testing you can use simplified strings)
# - expected_findings: a list of keywords/phrases that must appear in the output (e.g., clause numbers, specific text)
test_cases = [
    {
        "name": "Test Case 1 - Clear Non-Conformity",
        "document_title": "Test Document 1",
        "document_topic": "Quality Procedure",
        "analysis_topic": "Procedure non-compliance",
        "analysis_section": "Section 1.2",
        "standard_text": "ISO Clause 7.3: The organization shall maintain documented procedures for design control.",
        "document_text": "The document does not mention any procedures for design control, thus not fulfilling clause 7.3.",
        "expected_findings": ["Section 1.2", "Clause 7.3", "design control", "documented procedures"]
    },
    {
        "name": "Test Case 2 - Fully Compliant",
        "document_title": "Test Document 2",
        "document_topic": "Quality Management",
        "analysis_topic": "Compliance check",
        "analysis_section": "Section 4.1",
        "standard_text": "ISO Clause 4.1: The organization shall establish a quality management system.",
        "document_text": "The document details a comprehensive quality management system that complies with all requirements of Clause 4.1.",
        "expected_findings": []  # Expecting no non-conformities reported
    }
]


# --- Function to Build the Prompt and Run a Test Case ---
def run_test_case(test_case):
    messages = [
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
                f"Document Title: '{test_case['document_title']}'\n"
                f"Document Topic: {test_case['document_topic']}\n"
                f"Analysis Topic: {test_case['analysis_topic']}\n"
                f"Analysis Section: {test_case['analysis_section']}\n\n"
                "Standard Content (extracted from PDF):\n\n"
                f"{test_case['standard_text']}\n\n"
                "Document Content:\n\n"
                f"{test_case['document_text']}"
            )
        }
    ]

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.0,
        top_p=0.9,
        n=1,
        messages=messages
    )
    model_output = response.choices[0].message.content
    return model_output


# --- Evaluation Functions ---
def evaluate_output(model_output, expected_findings):
    """
    A simple evaluation that checks whether each expected keyword/phrase appears in the model output.
    Returns a list of found expected findings, and computes basic precision and recall.
    """
    found = []
    for expected in expected_findings:
        if expected.lower() in model_output.lower():
            found.append(expected)
    # For this basic example, assume:
    # - Precision = (Number of expected findings found) / (Total expected findings)
    # - Recall = same as precision because we only check if expected phrases are present.
    precision = len(found) / len(expected_findings) if expected_findings else 1.0
    recall = precision
    return found, precision, recall


def evaluate_test_cases(test_cases):
    results = []
    for test in test_cases:
        print(f"Running {test['name']} ...")
        output = run_test_case(test)
        found, precision, recall = evaluate_output(output, test["expected_findings"])
        results.append({
            "test_name": test["name"],
            "output": output,
            "expected_findings": test["expected_findings"],
            "found": found,
            "precision": precision,
            "recall": recall
        })
    return results


# --- Main Script for Running Evals ---
if __name__ == "__main__":
    test_results = evaluate_test_cases(test_cases)
    # Print a summary of results for each test case
    for result in test_results:
        print("=" * 50)
        print("Test Name:", result["test_name"])
        print("Expected Findings:", result["expected_findings"])
        print("Found Findings:", result["found"])
        print(f"Precision: {result['precision']:.2f}, Recall: {result['recall']:.2f}")
        print("Model Output:\n", result["output"])
        print("=" * 50)
