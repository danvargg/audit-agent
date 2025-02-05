# audit-agent

## chat-gpt results

| QP 03 Rev 9.0                         | Finding                                                                                       | ISO 13485:2016 Reference |
|---------------------------------------|---------------------------------------------------------------------------------------------|---------------------------|
| 7.1 Design and Development Planning   | No clear `trigger conditions` for updating the design and development plan.                   | 7.3.2                     |
| 7.3 Design Input Requirements         | No explicit mention of a traceability matrix linking design inputs to verification steps.    | 7.3.3                     |
| 7.3.6 Design Verification             | Design verification process lacks clear traceability between design inputs and outputs.      | 7.3.6                     |
| 7.3.7 Design Validation               | No explicit requirement for usability validation in `real or simulated conditions`.            | 7.3.7                     |
| 7.3.8 Design Transfer                 | No clear verification process for ensuring design outputs are ready for production.          | 7.3.8                     |


Which one would work best for an agent that is going to be used to perform iso audits on a company's documents
ChatGPT said:
ChatGPT
For an AI agent performing ISO audits on a company’s documents, the best approach would be a multi-agent system leveraging Retrieval-Augmented Generation (RAG), Chain of Thought (CoT), and function calling.

Why?
RAG ensures the AI only responds based on ISO compliance documents.
CoT improves the AI’s ability to analyze and reason through audit requirements.
Multi-Agent Approach allows for document parsing, auditing, and verification.
Function Calling enables structured API calls for fetching compliance guidelines.

# Best Architecture for an ISO Audit AI Agent
## 1. Multi-Agent System Using OpenAI's GPT-4o
You should use CrewAI or AutoGen to create an ISO Audit AI with different specialized agents:

Agent Type	Function
Document Parsing Agent	Extracts relevant ISO-related text from documents (OCR if needed)
ISO Compliance Agent	Checks extracted text against ISO standards using RAG
Audit Reporting Agent	Generates a detailed audit report based on findings
Verification Agent	Ensures compliance interpretations are accurate

# 2.Use Retrieval-Augmented Generation (RAG)
Since ISO audits rely on specific compliance documents, the AI must reference ISO standards rather than hallucinate responses.

You can use:

FAISS, Weaviate, Pinecone, or ChromaDB as a vector database.
LlamaIndex or LangChain for document retrieval.
Implementation of RAG for ISO Audits
Ingest company’s documents (ISO policies, procedures).
Chunk the text and embed it into a vector database.
Retrieve relevant sections dynamically during the audit.
Use GPT-4o to analyze compliance based on retrieved context.

```python
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader

# Load and embed documents
loader = PyPDFLoader("iso_audit_document.pdf")
documents = loader.load()

# Create vector store
vector_store = FAISS.from_documents(documents, OpenAIEmbeddings())

# Retrieve relevant text for audit query
query = "What are the ISO 27001 compliance requirements for data security?"
docs = vector_store.similarity_search(query)

for doc in docs:
    print(doc.page_content)
```
- Ensures accuracy by retrieving actual ISO sections.
- Prevents hallucination by restricting responses to retrieved text.

# 3. Implement Chain-of-Thought (CoT) Reasoning
Use structured prompts for step-by-step audit reasoning.

Example: CoT Prompt for ISO Audit
```text
You are an AI ISO Auditor. Use the following step-by-step reasoning to analyze compliance:

1. Identify the section of the company’s document relevant to the ISO standard.
2. Compare the section with ISO [Insert Standard Number] compliance requirements.
3. Highlight any gaps or non-compliance issues.
4. Suggest corrective actions.
5. Provide a risk assessment score from 1 to 5.

Company Document Extract: {retrieved_text}

ISO Compliance Requirement: {iso_standard_text}

Think step by step:
```

Forces the AI to break down compliance issues.
Ensures logical auditing without missing key points.

# 4. Multi-Agent System for ISO Audit
Using CrewAI or AutoGen, you can create a multi-agent workflow.

Example: CrewAI Agents for ISO Auditing
```python
from crewai import Agent, Task, Crew
import openai

openai.api_key = "your_openai_api_key"

# ISO Document Parsing Agent
doc_parser = Agent(
    role="ISO Document Parsing Agent",
    goal="Extract relevant sections from company documents for compliance checking.",
    model="gpt-4o",
)

# ISO Compliance Checking Agent
iso_audit = Agent(
    role="ISO Compliance Auditor",
    goal="Analyze extracted text against ISO 27001 compliance requirements.",
    model="gpt-4o",
)

# Audit Reporting Agent
reporting_agent = Agent(
    role="Audit Report Generator",
    goal="Summarize findings into an ISO audit report, highlighting compliance gaps and recommendations.",
    model="gpt-4o",
)

# Task Definitions
task1 = Task(description="Extract company document data for ISO compliance checking.", agent=doc_parser)
task2 = Task(description="Compare extracted data with ISO 27001 standards and check for compliance gaps.", agent=iso_audit)
task3 = Task(description="Generate a compliance report with recommendations.", agent=reporting_agent)

# Define Crew
iso_audit_crew = Crew(agents=[doc_parser, iso_audit, reporting_agent], tasks=[task1, task2, task3])

# Run the multi-agent audit process
audit_report = iso_audit_crew.kickoff()
print(audit_report)
```

Each agent performs a specialized task.
Automates the entire audit workflow.
Ensures structured auditing with minimal manual intervention.

# 5. Function Calling for Structured Audit Queries
To fetch ISO compliance rules dynamically, use OpenAI’s function calling.

Example: Defining an ISO Compliance Function
```python
import openai

functions = [
    {
        "name": "get_iso_compliance",
        "description": "Retrieve ISO compliance standards for a given requirement",
        "parameters": {"iso_standard": "string", "requirement": "string"}
    }
]

def get_iso_compliance(iso_standard, requirement):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You are an ISO compliance expert."},
                  {"role": "user", "content": f"Find the compliance requirements for {requirement} in {iso_standard}"}],
        functions=functions
    )
    return response["choices"][0]["message"]["content"]

# Example usage
print(get_iso_compliance("ISO 27001", "data encryption"))
```
