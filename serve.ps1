# Simple HTTP server for local testing
# Run this script and open http://localhost:8080 in your browser

Write-Host "Starting Aurora Portal local server..." -ForegroundColor Cyan
Write-Host "URL: http://localhost:8080" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

# Start Python HTTP server
python -m http.server 8080
