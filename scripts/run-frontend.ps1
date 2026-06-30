# Run ProcureFlow Frontend (Next.js)
Set-Location $PSScriptRoot\..\frontend

if (-not (Test-Path .env.local)) {
    Write-Host "Creating .env.local from .env.local.example..." -ForegroundColor Yellow
    Copy-Item .env.local.example .env.local
}

if (-not (Test-Path node_modules)) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    npm install
}

Write-Host "Starting frontend on http://localhost:3000" -ForegroundColor Green
npm run dev
