# ProcureFlow AI — Full Setup Script
Write-Host "=== ProcureFlow AI Setup ===" -ForegroundColor Cyan
Write-Host ""

# Backend setup
Write-Host "[1/3] Setting up backend..." -ForegroundColor Yellow
Set-Location $PSScriptRoot\..\backend

if (-not (Test-Path .env)) {
    Copy-Item .env.example .env
    Write-Host "  .env created from .env.example" -ForegroundColor Green
}

if (-not (Test-Path .venv)) {
    Write-Host "  Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
}

Write-Host "  Installing Python packages..." -ForegroundColor Yellow
.venv\Scripts\python.exe -m pip install -r requirements.txt --quiet
Write-Host "  Backend ready." -ForegroundColor Green

# Database setup
Write-Host ""
Write-Host "[2/3] Setting up database..." -ForegroundColor Yellow
.venv\Scripts\python.exe setup_db.py 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "  setup_db failed (tables may already exist). Running seed..." -ForegroundColor Yellow
}
.venv\Scripts\python.exe seed_sql.py 2>$null
Write-Host "  Database seeded." -ForegroundColor Green

# Frontend setup
Write-Host ""
Write-Host "[3/3] Setting up frontend..." -ForegroundColor Yellow
Set-Location $PSScriptRoot\..\frontend

if (-not (Test-Path .env.local)) {
    Copy-Item .env.local.example .env.local
    Write-Host "  .env.local created" -ForegroundColor Green
}

if (-not (Test-Path node_modules)) {
    Write-Host "  Installing Node packages..." -ForegroundColor Yellow
    npm install
}

Write-Host ""
Write-Host "=== Setup complete ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "To run the app:" -ForegroundColor White
Write-Host "  Terminal 1: .\scripts\run-backend.ps1" -ForegroundColor Gray
Write-Host "  Terminal 2: .\scripts\run-frontend.ps1" -ForegroundColor Gray
Write-Host ""
Write-Host "Login: admin@procureflow.ai / Admin@123" -ForegroundColor White
