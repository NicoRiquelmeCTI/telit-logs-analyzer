from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import tempfile
import os
from pathlib import Path
from typing import Optional

from connectivity_analyzer.application.use_cases import GenerateConnectivityReportUseCase
from connectivity_analyzer.infrastructure.repositories import LogFileConnectivityRepository

app = FastAPI(title="Connectivity Analyzer")

# Templates
templates = Jinja2Templates(directory="src/connectivity_analyzer/interfaces/web/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze")
async def analyze_log(
    request: Request,
    log_text: Optional[str] = Form(None),
    log_file: Optional[UploadFile] = File(None)
):
    try:
        if not log_text and not log_file:
            return templates.TemplateResponse(
                "index.html",
                {"request": request, "error": "Please provide either log text or a log file"}
            )

        # Create temporary file if text is provided
        if log_text:
            with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as temp_file:
                temp_file.write(log_text)
                temp_file_path = temp_file.name
        else:
            # Save uploaded file
            temp_file_path = f"temp_{log_file.filename}"
            with open(temp_file_path, "wb") as buffer:
                content = await log_file.read()
                buffer.write(content)

        try:
            # Initialize use case and repository
            repository = LogFileConnectivityRepository()
            use_case = GenerateConnectivityReportUseCase(repository)
            
            # Generate report
            report = use_case.execute(temp_file_path)
            
            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "report": report,
                    "success": True
                }
            )
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": f"Error analyzing log: {str(e)}"
            }
        ) 