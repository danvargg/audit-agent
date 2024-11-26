import os

from crewai import Agent, Task, Crew
# from langchain.tools import BaseTool
from crewai_tools import BaseTool
from typing import Optional
import PyPDF2
import re
from datetime import datetime

os.environ['OPENAI_MODEL_NAME'] = 'gpt-4o-mini'

class PDFReaderTool(BaseTool):
    name: str = "PDF Reader"
    description: str = "Reads and extracts text from PDF documents"

    def _run(self, file_path: str) -> str:
        print()
        print(file_path)
        print()
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        print(text[0:100])
        return text


# Create tools
pdf_reader = PDFReaderTool()

# Define agents
compliance_reviewer = Agent(
    role='ISO Compliance Reviewer',
    goal='Thoroughly review SOPs against ISO 13485:2016 standards and identify non-compliance issues',
    backstory="""You are an experienced ISO auditor specialized in medical device quality 
    management systems. You have extensive knowledge of ISO 13485:2016 requirements and 
    can identify gaps between procedures and standards.""",
    tools=[pdf_reader],
    verbose=True
)

report_generator = Agent(
    role='Audit Report Generator',
    goal='Generate comprehensive audit reports based on compliance findings',
    backstory="""You are a skilled technical writer with expertise in creating clear, 
    detailed audit reports. You understand medical device quality systems and can 
    effectively communicate findings in a standardized format.""",
    tools=[pdf_reader],
    verbose=True
)


def create_audit_crew(sop_path: str, iso_standard_path: str, report_template_path: str) -> None:
    # Task 1: Review SOP against ISO standard
    review_task = Task(
        description=f"""
        1. Read the SOP from {sop_path}
        2. Read the ISO standard from {iso_standard_path}
        3. Compare the SOP against relevant ISO 13485:2016 requirements
        4. Identify any non-conformities or gaps
        5. Provide detailed findings including:
           - Specific clause references from ISO 13485:2016
           - Description of the non-conformity
           - Evidence from the SOP
        """,
        agent=compliance_reviewer,
    expected_output="A detailed list of findings with clause references, descriptions, and evidence."
    )

    # Task 2: Generate audit report
    report_task = Task(
        description=f"""
        1. Read the audit report template from {report_template_path}
        2. Review the compliance findings from the previous task
        3. Generate a formal audit report following the template structure
        4. Include:
           - Executive summary
           - Detailed findings with references
           - Risk assessment for each finding
           - Recommendations for corrective actions
        """,
        agent=report_generator,
    expected_output="A formal audit report with an executive summary, detailed findings, risk assessment, and recommendations."
    )

    # Create and run the crew
    crew = Crew(
        agents=[compliance_reviewer, report_generator],
        tasks=[review_task, report_task],
        verbose=True
    )

    return crew.kickoff()


def main():
    # File paths should be provided by the user
    sop_path = "QP03 Rev 9.0 Design Control.pdf"
    iso_standard_path = "ISO-13485-2016.pdf"
    report_template_path = "Internal Audit Report Design and Development Process - June 2024.pdf"

    result = create_audit_crew(sop_path, iso_standard_path, report_template_path)

    # Save the results to a file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"audit_report_{timestamp}.md", "w") as f:
        f.write(str(result))


if __name__ == "__main__":
    main()