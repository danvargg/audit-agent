# Automatic ISO Compliance Analysis

![Python](https://img.shields.io/badge/-Python-000000?style=flat&logo=Python)
![Pandas](https://img.shields.io/badge/-Pandas-000000?style=flat&logo=Pandas)
![OpenAI](https://img.shields.io/badge/-OpenAI-000000?style=flat&logo=OpenAI)
![Streamlit](https://img.shields.io/badge/-Streamlit-000000?style=flat&logo=Streamlit)

> This a generalized version of the project. The specific code, architecture, and data are property of the client and 
cannot be fully shared.

A solution designed to automate the process of analyzing company documentation for compliance with ISO 13485:2016 standards. 
It uses OpenAI's language models to generate structured audit reports based on extracted document content.

<img width=100% height=100%  src="https://github.com/danvargg/audit-agent/blob/main/img/ui.png">

## Business Problem
The tool addresses the need for efficient and accurate compliance auditing in the medical device industry. It reduces 
manual effort, ensures adherence to standards, and provides actionable insights for improving documentation.

## Implementation

- PDF Text Extraction: Extracts text from PDF documents using PyPDF2.
- Automated Audit Reports: Leverages OpenAI's GPT models to generate detailed audit findings.
- ISO 13485:2016 Compliance: Strictly adheres to the ISO 13485:2016 standard for medical devices.
- Structured Reporting: Provides findings in a clear and professional format, including:
  - Document section
  - Finding description
  - Standard reference
  - Reason for non-conformity
  - Recommendations for improvement 

## Business Results
The solution streamlines the compliance auditing process, enabling businesses to:  
- Save time and resources.
- Ensure documentation meets regulatory requirements.
- Identify and address non-conformities effectively.
