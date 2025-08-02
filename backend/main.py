from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
import io
import os
from typing import Dict, Any
import json

from analysis import perform_statistical_analysis
from pdf_generator import generate_pdf_report

app = FastAPI(title="Statly API", description="API for statistical analysis of Excel files")

# Monta i file statici del frontend
frontend_dir = os.path.join(os.path.dirname(__file__), "../frontend")
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

# CORS per permettere al frontend di comunicare con il backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In produzione specificare l'URL del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def serve_frontend():
    """
    Serve la pagina principale del frontend
    """
    frontend_path = os.path.join(os.path.dirname(__file__), "../frontend/index.html")
    return FileResponse(frontend_path)

@app.get("/styles.css")
async def serve_css():
    """
    Serve il file CSS
    """
    css_path = os.path.join(os.path.dirname(__file__), "../frontend/styles.css")
    return FileResponse(css_path, media_type="text/css")

@app.get("/script.js")
async def serve_js():
    """
    Serve il file JavaScript
    """
    js_path = os.path.join(os.path.dirname(__file__), "../frontend/script.js")
    return FileResponse(js_path, media_type="application/javascript")

@app.get("/api/")
async def api_root():
    return {"message": "Statly API - Ready for statistical analysis!"}

@app.post("/api/upload-excel")
async def upload_excel_file(file: UploadFile = File(...)):
    """
    Endpoint per caricare un file Excel e ottenere un'anteprima dei dati
    """
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="File deve essere Excel (.xlsx o .xls)")
    
    try:
        # Leggi il file Excel
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        
        # Verifica che il file non sia vuoto
        if df.empty:
            raise HTTPException(status_code=400, detail="Il file Excel è vuoto")
        
        # Restituisci informazioni base sul dataset
        return {
            "success": True,
            "filename": file.filename,
            "rows": int(len(df)),
            "columns": int(len(df.columns)),
            "column_names": df.columns.tolist(),
            "data_types": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "preview": df.head(5).fillna("").to_dict('records'),  # Prime 5 righe, sostituisce NaN con stringa vuota
            "has_missing_values": bool(df.isnull().any().any())
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore nel processare il file: {str(e)}")

@app.post("/api/analyze")
async def analyze_data(file: UploadFile = File(...)):
    """
    Endpoint per eseguire l'analisi statistica completa del file Excel
    """
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="File deve essere Excel (.xlsx o .xls)")
    
    try:
        # Leggi il file Excel
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        
        if df.empty:
            raise HTTPException(status_code=400, detail="Il file Excel è vuoto")
        
        # Esegui l'analisi statistica
        analysis_results = perform_statistical_analysis(df)
        
        return {
            "success": True,
            "filename": file.filename,
            "analysis": analysis_results
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore nell'analisi: {str(e)}")

@app.post("/api/generate-report")
async def generate_report(file: UploadFile = File(...)):
    """
    Endpoint per generare e scaricare il report PDF completo
    """
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="File deve essere Excel (.xlsx o .xls)")
    
    try:
        # Leggi il file Excel
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        
        if df.empty:
            raise HTTPException(status_code=400, detail="Il file Excel è vuoto")
        
        # Esegui l'analisi
        analysis_results = perform_statistical_analysis(df)
        
        # Genera il PDF
        pdf_path = generate_pdf_report(df, analysis_results, file.filename)
        
        # Restituisci il file PDF
        return FileResponse(
            pdf_path,
            media_type='application/pdf',
            filename=f"statly_report_{file.filename.split('.')[0]}.pdf"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore nella generazione del report: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
