from openai import OpenAI

from api.prompts import AUDIT_PROMPT

MODEL = "gpt-4o-mini"


def generate_audit_findings(standard_text, document_text):
    client = OpenAI()

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.0,
        top_p=0.9,
        n=1,
        messages=[
            {
                "role": "system",
                "content": AUDIT_PROMPT
            },
            {
                "role": "user",
                "content": (
                    "ISO Standard Content:\n\n"
                    f"{standard_text}\n\n"
                    "Document to be audited Content:\n\n"
                    f"{document_text}"
                )
            }
        ]
    )

    return response.choices[0].message.content
