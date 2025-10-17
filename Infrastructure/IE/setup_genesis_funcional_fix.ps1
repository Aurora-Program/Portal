# Setup Rapido - Genesis Funcional v1.3.3
# Ejecutar: powershell -ep bypass .\setup_genesis_funcional_fix.ps1

Write-Host "`n"
Write-Host "GENESIS FUNCIONAL v1.3.3 - SETUP AUTOMATICO" -ForegroundColor Cyan -BackgroundColor Black
Write-Host ("="*60) -ForegroundColor Cyan

# 1. Verificar Python
Write-Host "`n[1/4] Verificando Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  OK Python instalado: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "  ERROR Python NO encontrado. Instala Python 3.8+ desde python.org" -ForegroundColor Red
    exit 1
}

# 2. Verificar/Instalar dependencias
Write-Host "`n[2/4] Verificando dependencias..." -ForegroundColor Yellow

$dependencias = @("sentence-transformers", "numpy")
$instaladas = @()
$faltantes = @()

foreach ($dep in $dependencias) {
    $importName = $dep.Replace('-','_')
    $null = python -c "import $importName" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  OK $dep instalado" -ForegroundColor Green
        $instaladas += $dep
    } else {
        Write-Host "  WARN $dep NO instalado" -ForegroundColor Yellow
        $faltantes += $dep
    }
}

if ($faltantes.Count -gt 0) {
    Write-Host "`nInstalando dependencias faltantes..." -ForegroundColor Yellow
    foreach ($dep in $faltantes) {
        Write-Host "  Instalando $dep..." -ForegroundColor Cyan
        $null = pip install $dep --quiet 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  OK $dep instalado exitosamente" -ForegroundColor Green
        } else {
            Write-Host "  ERROR instalando $dep" -ForegroundColor Red
        }
    }
}

# 3. Verificar archivos
Write-Host "`n[3/4] Verificando archivos funcionales..." -ForegroundColor Yellow

$archivos = @(
    "genesis_autopoiesis_funcional.py",
    "test_genesis_comparacion.py",
    "tensor_ffe_funcional.py",
    "transcender_funcional.py",
    "evolver_funcional.py",
    "armonizador_funcional.py"
)

$archivosOK = 0
foreach ($archivo in $archivos) {
    if (Test-Path $archivo) {
        Write-Host "  OK $archivo" -ForegroundColor Green
        $archivosOK++
    } else {
        Write-Host "  FALTA $archivo" -ForegroundColor Red
    }
}

if ($archivosOK -eq $archivos.Count) {
    Write-Host "`n  OK Todos los archivos presentes ($archivosOK/$($archivos.Count))" -ForegroundColor Green
} else {
    Write-Host "`n  WARN Faltan archivos ($archivosOK/$($archivos.Count))" -ForegroundColor Yellow
}

# 4. Test rapido
Write-Host "`n[4/4] Test rapido de importacion..." -ForegroundColor Yellow

$testCode = @"
try:
    from genesis_autopoiesis_funcional import GenesisAutopoiseisFuncional
    from tensor_ffe_funcional import TensorFFE
    print('OK Imports exitosos')
except Exception as e:
    print('ERROR: ' + str(e))
"@

$resultado = $testCode | python 2>&1
if ($resultado -match 'OK') {
    Write-Host "  $resultado" -ForegroundColor Green
} else {
    Write-Host "  $resultado" -ForegroundColor Red
}

# Resumen
Write-Host "`n"
Write-Host ("="*60) -ForegroundColor Cyan
Write-Host "RESUMEN DE SETUP" -ForegroundColor Cyan
Write-Host ("="*60) -ForegroundColor Cyan

Write-Host "`nSetup completado!" -ForegroundColor Green
Write-Host "`nProximos pasos:" -ForegroundColor Yellow
Write-Host "  1. Ejecutar tests:  " -NoNewline -ForegroundColor White
Write-Host "python test_genesis_comparacion.py" -ForegroundColor Cyan
Write-Host "  2. Demo completo:   " -NoNewline -ForegroundColor White
Write-Host "python genesis_autopoiesis_funcional.py" -ForegroundColor Cyan
Write-Host "  3. Demo interactivo:" -NoNewline -ForegroundColor White
Write-Host "powershell -ep bypass .\demo_genesis_interactivo.ps1" -ForegroundColor Cyan

Write-Host "`nDocumentacion completa: GUIA_PRUEBAS_GENESIS_FUNCIONAL.md" -ForegroundColor Gray
Write-Host "`n"
