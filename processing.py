import PyPDF2

# def extract_text_from_pdf(pdf_path):
#     with open(pdf_path, "rb") as f:
#         reader = PyPDF2.PdfReader(f)
#         text = ""
#         for page in reader.pages:
#             text += page.extract_text() + "\n"
#     return text

# def parse_llm_output(output: str) -> pd.DataFrame:
#     output = output.strip('`').strip()
#     data_dict = json.loads(output)
#     data = [(item_code, ', '.join(codes)) for item_code, codes in data_dict.items()]
#     df = pd.DataFrame(data, columns=["ItemCode", "Extracted Codes"])
#     return df