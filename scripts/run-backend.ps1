# Run ProcureFlow Backend (FastAPI)
Set-Location $PSScriptRoot\..\backend

if (-not (Test-Path .env)) {
    Write-Host "Creating .env from .env.example..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "Edit .env with your DATABASE_URL before running." -ForegroundColor Red
    exit 1
}

if (-not (Test-Path .venv)) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
}

Write-Host "Starting backend on http://localhost:8000" -ForegroundColor Green
Write-Host "API docs at http://localhost:8000/api/docs" -ForegroundColor Green
.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
