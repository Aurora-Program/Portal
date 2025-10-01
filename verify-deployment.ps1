# Script de verificación de deployment Aurora Portal
# Verifica que el WASM esté compilado y los archivos tengan la estructura correcta

[CmdletBinding()]
param(
    [Parameter(Mandatory=$false)]
    [string]$BucketName = "",
    
    [Parameter(Mandatory=$false)]
    [switch]$LocalOnly = $false
)

$ErrorActionPreference = "Continue"

Write-Host "`n🔍 Aurora Portal - Verificación de Deployment" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Gray

# 1. Verificar estructura local
Write-Host "`n📁 Verificando estructura de archivos locales..." -ForegroundColor Yellow

$errors = @()
$warnings = @()

# Verificar archivos críticos
$criticalFiles = @(
    "index.html",
    "js/aurora-portal.js",
    "assets/aurora-portal-logo.png"
)

foreach ($file in $criticalFiles) {
    if (Test-Path $file) {
        Write-Host "  ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $file - NO ENCONTRADO" -ForegroundColor Red
        $errors += $file
    }
}

# Verificar que WASM esté compilado
Write-Host "`n🦀 Verificando compilación WASM..." -ForegroundColor Yellow

$wasmPkgPath = "wasm-client/pkg"
if (Test-Path $wasmPkgPath) {
    Write-Host "  ✅ Directorio pkg/ existe" -ForegroundColor Green
    
    $wasmFiles = @(
        "aurora_wasm_client.js",
        "aurora_wasm_client_bg.wasm",
        "aurora_wasm_client.d.ts"
    )
    
    foreach ($file in $wasmFiles) {
        $fullPath = Join-Path $wasmPkgPath $file
        if (Test-Path $fullPath) {
            $size = (Get-Item $fullPath).Length
            $sizeKB = [math]::Round($size / 1KB, 2)
            Write-Host "  ✅ $file ($sizeKB KB)" -ForegroundColor Green
        } else {
            Write-Host "  ❌ $file - NO ENCONTRADO" -ForegroundColor Red
            $errors += "$wasmPkgPath/$file"
        }
    }
} else {
    Write-Host "  ❌ Directorio pkg/ NO EXISTE" -ForegroundColor Red
    Write-Host "     Ejecuta: cd wasm-client && wasm-pack build --target web --release" -ForegroundColor Yellow
    $errors += "wasm-client/pkg/"
}

# Verificar import en aurora-portal.js
Write-Host "`n🔗 Verificando rutas de import..." -ForegroundColor Yellow

$jsContent = Get-Content "js/aurora-portal.js" -Raw
if ($jsContent -match "from\s+['\`"]\.\.\/wasm-client\/pkg\/aurora_wasm_client\.js['\`"]") {
    Write-Host "  ✅ Ruta de import correcta: ../wasm-client/pkg/aurora_wasm_client.js" -ForegroundColor Green
} elseif ($jsContent -match "from\s+['\`"]\.\/wasm-client\/pkg\/aurora_wasm_client\.js['\`"]") {
    Write-Host "  ⚠️  Ruta de import incorrecta: ./wasm-client/pkg/..." -ForegroundColor Yellow
    Write-Host "     Debería ser: ../wasm-client/pkg/..." -ForegroundColor Yellow
    $warnings += "Ruta de import incorrecta en js/aurora-portal.js"
} else {
    Write-Host "  ❌ No se encontró import de aurora_wasm_client.js" -ForegroundColor Red
    $errors += "Import statement en js/aurora-portal.js"
}

# Verificar workflow de GitHub Actions
Write-Host "`n⚙️  Verificando workflow de GitHub Actions..." -ForegroundColor Yellow

$workflowPath = ".github/workflows/main.yaml"
if (Test-Path $workflowPath) {
    $workflowContent = Get-Content $workflowPath -Raw
    
    $checks = @{
        "Checkout step" = "actions/checkout@v4"
        "Rust toolchain" = "dtolnay/rust-toolchain"
        "wasm-pack install" = "wasm-pack/installer"
        "WASM build" = "wasm-pack build"
        "Content-Type WASM" = "application/wasm"
    }
    
    foreach ($check in $checks.GetEnumerator()) {
        if ($workflowContent -match [regex]::Escape($check.Value)) {
            Write-Host "  ✅ $($check.Key)" -ForegroundColor Green
        } else {
            Write-Host "  ❌ $($check.Key) - NO ENCONTRADO" -ForegroundColor Red
            $errors += "Workflow: $($check.Key)"
        }
    }
} else {
    Write-Host "  ❌ Archivo workflow NO ENCONTRADO" -ForegroundColor Red
    $errors += $workflowPath
}

# Verificación de S3 (opcional)
if (-not $LocalOnly -and $BucketName) {
    Write-Host "`n☁️  Verificando archivos en S3..." -ForegroundColor Yellow
    
    try {
        # Verificar que aws CLI esté disponible
        $awsVersion = aws --version 2>&1
        Write-Host "  ℹ️  AWS CLI: $awsVersion" -ForegroundColor Gray
        
        # Listar archivos en pkg/
        Write-Host "`n  Archivos en s3://$BucketName/wasm-client/pkg/:" -ForegroundColor Gray
        $s3Files = aws s3 ls "s3://$BucketName/wasm-client/pkg/" 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host $s3Files -ForegroundColor Gray
            
            # Verificar Content-Type del archivo JS
            Write-Host "`n  Verificando Content-Type de aurora_wasm_client.js..." -ForegroundColor Gray
            $headObject = aws s3api head-object --bucket $BucketName --key "wasm-client/pkg/aurora_wasm_client.js" 2>&1 | ConvertFrom-Json
            
            if ($headObject.ContentType -match "javascript") {
                Write-Host "  ✅ Content-Type: $($headObject.ContentType)" -ForegroundColor Green
            } else {
                Write-Host "  ⚠️  Content-Type: $($headObject.ContentType)" -ForegroundColor Yellow
                $warnings += "Content-Type incorrecto en S3"
            }
            
            # Verificar Content-Type del archivo WASM
            Write-Host "`n  Verificando Content-Type de aurora_wasm_client_bg.wasm..." -ForegroundColor Gray
            $headObjectWasm = aws s3api head-object --bucket $BucketName --key "wasm-client/pkg/aurora_wasm_client_bg.wasm" 2>&1 | ConvertFrom-Json
            
            if ($headObjectWasm.ContentType -eq "application/wasm") {
                Write-Host "  ✅ Content-Type: $($headObjectWasm.ContentType)" -ForegroundColor Green
            } else {
                Write-Host "  ⚠️  Content-Type: $($headObjectWasm.ContentType)" -ForegroundColor Yellow
                $warnings += "Content-Type incorrecto para .wasm en S3"
            }
        } else {
            Write-Host "  ⚠️  No se pudieron listar archivos en S3" -ForegroundColor Yellow
            Write-Host "     Error: $s3Files" -ForegroundColor Gray
            $warnings += "No se pudo verificar S3"
        }
        
    } catch {
        Write-Host "  ⚠️  Error al verificar S3: $_" -ForegroundColor Yellow
        $warnings += "Error en verificación de S3"
    }
}

# Resumen
Write-Host "`n" + ("=" * 60) -ForegroundColor Gray
Write-Host "📊 RESUMEN DE VERIFICACIÓN" -ForegroundColor Cyan

if ($errors.Count -eq 0 -and $warnings.Count -eq 0) {
    Write-Host "`n✅ TODO CORRECTO - Listo para deployment!" -ForegroundColor Green
    Write-Host "`nPróximos pasos:" -ForegroundColor Cyan
    Write-Host "  1. git add ." -ForegroundColor Gray
    Write-Host "  2. git commit -m 'fix: compile WASM in CI and correct import paths'" -ForegroundColor Gray
    Write-Host "  3. git push origin main" -ForegroundColor Gray
    Write-Host "  4. Monitorear GitHub Actions en: https://github.com/Aurora-Program/Portal/actions" -ForegroundColor Gray
    exit 0
} else {
    if ($errors.Count -gt 0) {
        Write-Host "`n❌ ERRORES ENCONTRADOS ($($errors.Count)):" -ForegroundColor Red
        foreach ($err in $errors) {
            Write-Host "  • $err" -ForegroundColor Red
        }
    }
    
    if ($warnings.Count -gt 0) {
        Write-Host "`n⚠️  ADVERTENCIAS ($($warnings.Count)):" -ForegroundColor Yellow
        foreach ($warn in $warnings) {
            Write-Host "  • $warn" -ForegroundColor Yellow
        }
    }
    
    Write-Host "`n🔧 RECOMENDACIONES:" -ForegroundColor Cyan
    if (-not (Test-Path "wasm-client/pkg")) {
        Write-Host "  1. Compilar WASM:" -ForegroundColor Yellow
        Write-Host "     cd wasm-client" -ForegroundColor Gray
        Write-Host "     .\build.ps1 -BuildType release -Target web" -ForegroundColor Gray
    }
    if ($warnings -match "import") {
        Write-Host "  2. Corregir ruta de import en js/aurora-portal.js" -ForegroundColor Yellow
    }
    if ($warnings -match "Content-Type") {
        Write-Host "  3. Ejecutar paso de Content-Type en workflow o manualmente" -ForegroundColor Yellow
    }
    
    exit 1
}
