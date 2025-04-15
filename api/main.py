from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse

from api.services import generate_audit_findings

app = FastAPI()


@app.get("/")
async def health_check():
    return {"status": "ok"}


@app.post("/analyze")
async def analyze_pdf(standard: UploadFile, document: UploadFile):
    try:
        audit_findings = generate_audit_findings(standard.file, document.file)
        return JSONResponse(content={"findings": audit_findings})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
