from fastapi import FastAPI, UploadFile, File, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os
from pathlib import Path
from typing import Optional

from connectivity_analyzer.application.use_cases import GenerateConnectivityReportUseCase
from connectivity_analyzer.infrastructure.repositories import LogFileConnectivityRepository

# Configuración de Flowise
FLOWISE_URL = os.getenv('FLOWISE_URL', 'https://flowise-1032065525651.us-central1.run.app')
FLOWISE_CHATFLOW_ID = os.getenv('FLOWISE_CHATFLOW_ID', 'd23c2a87-c9d8-44ca-af28-cf0ea39da43f')

def get_signal_level(rsrp: float, sinr: float) -> str:
    """Determina el nivel de señal basado en RSRP y SINR."""
    if rsrp > -90 and sinr > 20:
        return 'Excelente'
    if rsrp > -100 and sinr > 13:
        return 'Buena'
    if rsrp > -110 and sinr > 5:
        return 'Aceptable'
    if rsrp > -120 and sinr > 0:
        return 'Mala'
    return 'Muy mala'

def calculate_csq(rsrp: float) -> int:
    """
    Calcula el CSQ (Channel Signal Quality) basado en RSRP.
    El CSQ es un valor entre 0 y 31, donde:
    - 0: Sin señal
    - 1-10: Señal muy débil
    - 11-20: Señal débil
    - 21-25: Señal buena
    - 26-31: Señal excelente
    """
    # RSRP típicamente va de -140 dBm a -44 dBm
    # Normalizamos a un rango de 0-31
    if rsrp <= -140:
        return 0
    elif rsrp >= -44:
        return 31
    else:
        # Fórmula: (RSRP + 140) * (31/96)
        return int((rsrp + 140) * (31/96))

app = FastAPI(
    title="Connectivity Analyzer",
    description="A web application to analyze cellular connectivity logs",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Templates
templates = Jinja2Templates(directory="src/connectivity_analyzer/interfaces/web/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the home page with the upload form."""
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request,
            "flowise_url": FLOWISE_URL,
            "flowise_chatflow_id": FLOWISE_CHATFLOW_ID
        }
    )

@app.get("/analyze")
async def analyze_get():
    """Redirect GET requests to the home page."""
    return RedirectResponse(url="/")

@app.post("/analyze")
async def analyze_log(
    request: Request,
    log_text: Optional[str] = Form(None),
    log_file: Optional[UploadFile] = File(None)
):
    """
    Analyze a log file or text.
    
    Args:
        request: The FastAPI request object
        log_text: Optional text content of the log
        log_file: Optional uploaded log file
        
    Returns:
        HTML response with analysis results or error message
    """
    try:
        if not log_text and not log_file:
            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "error": "Please provide either log text or a log file",
                    "flowise_url": FLOWISE_URL,
                    "flowise_chatflow_id": FLOWISE_CHATFLOW_ID
                }
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
            
            # Calculate signal level
            report['signal_level'] = get_signal_level(
                report['signal_quality']['rsrp']['mean'],
                report['signal_quality']['sinr']['mean']
            )
            
            # Calculate CSQ
            report['csq'] = calculate_csq(report['signal_quality']['rsrp']['mean'])
            
            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "report": report,
                    "success": True,
                    "flowise_url": FLOWISE_URL,
                    "flowise_chatflow_id": FLOWISE_CHATFLOW_ID
                }
            )
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    except FileNotFoundError as e:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": f"File not found: {str(e)}",
                "flowise_url": FLOWISE_URL,
                "flowise_chatflow_id": FLOWISE_CHATFLOW_ID
            }
        )
    except ValueError as e:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": f"Invalid data: {str(e)}",
                "flowise_url": FLOWISE_URL,
                "flowise_chatflow_id": FLOWISE_CHATFLOW_ID
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": f"Error analyzing log: {str(e)}",
                "flowise_url": FLOWISE_URL,
                "flowise_chatflow_id": FLOWISE_CHATFLOW_ID
            }
        )

@app.exception_handler(405)
async def method_not_allowed_handler(request: Request, exc: HTTPException):
    """Handle 405 Method Not Allowed errors by redirecting to home page."""
    return RedirectResponse(url="/") 