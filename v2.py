"""
Below is a more concrete example that integrates the concepts from the previous explanation but uses LangChain and Chroma.
This example assumes you have:

LangChain installed: pip install langchain
Chroma installed: pip install chromadb
An OpenAI API key set as OPENAI_API_KEY in your environment (or you can pass it in code).
What this example does:

Load ISO Requirements:
We'll store ISO 13485 requirements as a Python list. Each requirement includes an ID and a textual description.

Load and Embed SOP Document:
We read an SOP text file, split it into chunks, embed these chunks using OpenAIEmbeddings, and store them in a Chroma
vector database.

Query the Vector Store for Each Requirement:
For each ISO requirement, we’ll use a similarity search on the SOP vector store to find the most relevant sections.

Use an LLM (OpenAI) to Assess Compliance:
We’ll feed the retrieved SOP chunks and the requirement into an LLM prompt, asking the model if the requirement is met.
The LLM provides reasoning and a conclusion.

Generate a Compliance Report:
We compile all the results into a simple report.

Note:
This is a conceptual example and may need adjustments depending on your exact file paths, model availability, and content.
The code should be close to executable if you have all dependencies and environment set up.
"""

import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Make sure you have your OpenAI API key set
# export OPENAI_API_KEY="your-key-here"

# ---------------------------
# 1. DEFINE ISO REQUIREMENTS
# ---------------------------
iso_requirements = [
    {
        "id": "ISO13485_7.3.2",
        "description": "The SOP must reference the risk management file (RMF) relevant to the device."
    },
    {
        "id": "ISO13485_7.5.1",
        "description": "The SOP must include a procedure for device sterilization validation."
    },
    {
        "id": "ISO13485_4.2.4",
        "description": "The SOP must have a controlled document reference and a revision history section."
    }
]

# ---------------------------
# 2. LOAD AND PREPARE THE SOP
# ---------------------------
sop_file_path = "sop_device_sterilization.txt"
with open(sop_file_path, "r") as f:
    sop_text = f.read()

# Split the SOP into chunks for embedding
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
    separators=["\n\n", "\n", " ", ""]
)
sop_chunks = text_splitter.split_text(sop_text)

# Create embeddings
embeddings = OpenAIEmbeddings()

# Create a Chroma vector store from the SOP chunks
vectorstore = Chroma.from_texts(texts=sop_chunks, embedding=embeddings, collection_name="sop_collection")

# ---------------------------
# 3. DEFINE PROMPT FOR LLM
# ---------------------------
prompt_template = """
You are an ISO 13485 compliance expert. You will be given an ISO requirement and relevant excerpts from an SOP.
Determine if the SOP meets the given ISO requirement fully, partially, or not at all.

Provide a brief reasoning. If not fully compliant, suggest what is missing or needs improvement.

ISO Requirement ({req_id}):
{requirement_description}

SOP Excerpts:
{context}

Your answer should include:
- Compliance level (Fully compliant / Partially compliant / Non-compliant)
- Reasoning
- If non-compliant or partial, what is missing?
"""

prompt = PromptTemplate(
    input_variables=["req_id", "requirement_description", "context"],
    template=prompt_template
)

llm = OpenAI(temperature=0)  # Using a deterministic setting for reproducibility
chain = LLMChain(llm=llm, prompt=prompt)

# ---------------------------
# 4. CHECK COMPLIANCE FOR EACH REQUIREMENT
# ---------------------------
audit_report = []

for req in iso_requirements:
    # Use similarity search to find relevant SOP sections
    similar_docs = vectorstore.similarity_search(req["description"], k=2)
    context = "\n---\n".join([doc.page_content for doc in similar_docs])

    # Run the LLM chain with the requirement and the found context
    response = chain.run(
        req_id=req["id"],
        requirement_description=req["description"],
        context=context
    )

    audit_entry = {
        "requirement_id": req["id"],
        "requirement_text": req["description"],
        "assessment": response.strip()
    }
    audit_report.append(audit_entry)

# ---------------------------
# 5. PRODUCE THE AUDIT REPORT
# ---------------------------
report_text = "=== ISO 13485 COMPLIANCE AUDIT REPORT ===\n\n"
for result in audit_report:
    report_text += f"Requirement ID: {result['requirement_id']}\n"
    report_text += f"Description: {result['requirement_text']}\n"
    report_text += f"Assessment:\n{result['assessment']}\n\n"

print(report_text)

# You can optionally save the report to a file:
with open("compliance_audit_report.txt", "w") as f:
    f.write(report_text)

"""
How This Works
Embeddings & Vector Store (Chroma):
The SOP is split into chunks and embedded. When we query with a requirement, similarity_search returns the most relevant 
SOP chunks. This ensures we give the LLM only the parts of the SOP likely related to the requirement.

LLM Reasoning (OpenAI):
The LLMChain takes the requirement and the SOP excerpts. The prompt asks the LLM to determine compliance. The LLM uses 
the provided excerpts to reason if the requirement is met.

No Simple Keyword Matching:
Even though this example doesn’t fully leverage complex semantic analysis internally, the vector search and the LLM’s 
reasoning capabilities allow for a more nuanced determination than simple keyword matching.

Adaptation:
In a real scenario, you might:

Add more requirements or a loop to handle all ISO clauses.
Improve the prompt to request structured JSON output.
Integrate more advanced logic or verification steps.
This example provides a baseline for using LangChain, Chroma, and an LLM to semantically check compliance of an SOP 
against ISO requirements.
"""