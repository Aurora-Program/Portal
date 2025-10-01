# Build script for Aurora WASM Client (PowerShell)

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet('dev', 'release')]
    [string]$BuildType = 'dev',
    
    [Parameter(Mandatory=$false)]
    [ValidateSet('web', 'bundler', 'nodejs')]
    [string]$Target = 'web'
)

Write-Host "Building Aurora WASM Client..." -ForegroundColor Cyan
Write-Host "Build type: $BuildType" -ForegroundColor Yellow
Write-Host "Target: $Target" -ForegroundColor Yellow

# Check if wasm-pack is installed
if (-not (Get-Command wasm-pack -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: wasm-pack is not installed!" -ForegroundColor Red
    Write-Host "Install it with: cargo install wasm-pack" -ForegroundColor Yellow
    exit 1
}

# Navigate to wasm-client directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Build command
$buildArgs = @('build', '--target', $Target)

if ($BuildType -eq 'release') {
    $buildArgs += '--release'
} else {
    $buildArgs += '--dev'
}

Write-Host "`nExecuting: wasm-pack $($buildArgs -join ' ')" -ForegroundColor Gray
Write-Host ""

# Run build
& wasm-pack @buildArgs

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nBuild successful!" -ForegroundColor Green
    Write-Host "Output directory: $scriptPath\pkg" -ForegroundColor Cyan
    
    # Show file sizes
    if (Test-Path "pkg") {
        Write-Host "`nGenerated files:" -ForegroundColor Cyan
        Get-ChildItem "pkg" | Where-Object { $_.Extension -in '.wasm', '.js', '.ts' } | ForEach-Object {
            $size = [Math]::Round($_.Length / 1KB, 2)
            Write-Host "  $($_.Name) - ${size} KB" -ForegroundColor Gray
        }
    }
    
    # Optimize WASM if release build
    if ($BuildType -eq 'release') {
        Write-Host "`nOptimizing WASM with wasm-opt..." -ForegroundColor Cyan
        
        if (Get-Command wasm-opt -ErrorAction SilentlyContinue) {
            $wasmFile = Get-ChildItem "pkg\*.wasm" | Select-Object -First 1
            if ($wasmFile) {
                & wasm-opt -Oz -o "$($wasmFile.FullName).opt" $wasmFile.FullName
                if ($LASTEXITCODE -eq 0) {
                    Move-Item "$($wasmFile.FullName).opt" $wasmFile.FullName -Force
                    $newSize = [Math]::Round($wasmFile.Length / 1KB, 2)
                    Write-Host "Optimized WASM size: ${newSize} KB" -ForegroundColor Green
                }
            }
        } else {
            Write-Host "wasm-opt not found. Skipping optimization." -ForegroundColor Yellow
            Write-Host "Install Binaryen for better optimization: https://github.com/WebAssembly/binaryen" -ForegroundColor Gray
        }
    }
    
    Write-Host "`nNext steps:" -ForegroundColor Cyan
    Write-Host "  1. Test locally: python -m http.server 8000" -ForegroundColor Gray
    Write-Host "  2. Deploy to S3: aws s3 sync pkg/ s3://your-bucket/wasm/" -ForegroundColor Gray
    Write-Host "  3. Update index.html to load the WASM module" -ForegroundColor Gray
    
} else {
    Write-Host "`nBuild failed!" -ForegroundColor Red
    exit 1
}
