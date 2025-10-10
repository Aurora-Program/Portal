# Aurora IE API Gateway Starter
# =============================

Write-Host "🐹 Aurora IE API Gateway" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (!(Test-Path "venv")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Start API
Write-Host ""
Write-Host "🚀 Starting Aurora IE API Gateway..." -ForegroundColor Green
Write-Host "📡 API will be available at: http://localhost:8080" -ForegroundColor Green
Write-Host "📚 Docs available at: http://localhost:8080/docs" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Run uvicorn
python -m uvicorn aurora_api:app --host 0.0.0.0 --port 8080 --reload
