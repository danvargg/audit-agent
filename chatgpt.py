import pandas as pd

# TODO:
# top_p: This parameter controls nucleus sampling. It specifies the cumulative probability threshold for token selection.
# The model considers only the smallest set of tokens whose cumulative probability is greater than or equal to top_p.
# For example, if top_p is set to 0.9, the model will consider only the tokens that together make up 90% of the probability
# mass. This helps in generating more coherent and contextually relevant responses

# n: This parameter specifies the number of completions to generate. If n is set to 3, the model will generate three
# different completions for the given prompt. This can be useful for getting multiple variations of the response and
# selecting the best one.

# Use OpenAI to analyze the document
response = openai.ChatCompletion.create(  # TODO: top_k, temp,
    model="gpt-4-turbo",
    temperature=0.0,
    # top_p=0.9,  # Adjust the top_p as needed
    # n=3,  # Number of completions to generate
    messages=[
    {"role": "system", "content": "You are an expert ISO 13485:2016 auditor."},
    {"role": "user", "content": (
        "Analyze the following document for non-conformities specifically related to design control as per ISO 13485:2016. "
        "The document is titled 'QP03 Rev 9.0 Design Control,' so focus only on clauses directly relevant to Section 7.3 (Design and Development Control). "
        "Do not include findings related to other sections of the standard.\n\n"
        "For each non-conformity identified, provide the following:\n"
        "1. Document Section: Reference the specific section or paragraph in the document.\n"
        "2. Finding: Clearly describe the issue or missing compliance element.\n"
        "3. ISO 13485:2016 Reference: Cite the relevant clause or subclause.\n"
        "4. Recommendation: Suggest how to address the issue, if possible.\n\n"
        "If information is unclear or missing, assume it is a potential non-conformity and specify what is missing. "
        "Do not infer or assume compliance where evidence is not explicitly provided.\n\n"
        f"{document_text}"
    )}
]


)

# Extract the response text
audit_findings = response["choices"][0]["message"]["content"]

# Convert response into a DataFrame
data = [line.split("|") for line in audit_findings.strip().split("\n")[1:]]
df = pd.DataFrame(data, columns=["Document Section", "Finding", "ISO Reference"])

# Save the findings table
df.to_csv("iso_audit_findings.csv", index=False)
print("Audit findings saved to iso_audit_findings.csv")
