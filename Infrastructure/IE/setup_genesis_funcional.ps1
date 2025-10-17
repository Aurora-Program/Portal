# 🚀 Setup Rápido - Genesis Funcional v1.3.3
# Ejecutar: .\setup_genesis_funcional.ps1

Write-Host "`n" -NoNewline
Write-Host "🌌 GENESIS FUNCIONAL v1.3.3 - SETUP AUTOMÁTICO" -ForegroundColor Cyan -BackgroundColor Black
Write-Host ("="*60) -ForegroundColor Cyan

# 1. Verificar Python
Write-Host "`n📋 [1/4] Verificando Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ Python instalado: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "  ❌ Python NO encontrado. Instala Python 3.8+ desde python.org" -ForegroundColor Red
    exit 1
}

# 2. Verificar/Instalar dependencias
Write-Host "`n📦 [2/4] Verificando dependencias..." -ForegroundColor Yellow

$dependencias = @("sentence-transformers", "numpy")
$instaladas = @()
$faltantes = @()

foreach ($dep in $dependencias) {
    $check = python -c "import $($dep.Replace('-','_'))" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ $dep instalado" -ForegroundColor Green
        $instaladas += $dep
    } else {
        Write-Host "  ⚠️  $dep NO instalado" -ForegroundColor Yellow
        $faltantes += $dep
    }
}

if ($faltantes.Count -gt 0) {
    Write-Host "`n📥 Instalando dependencias faltantes..." -ForegroundColor Yellow
    foreach ($dep in $faltantes) {
        Write-Host "  📦 Instalando $dep..." -ForegroundColor Cyan
        pip install $dep --quiet
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✅ $dep instalado exitosamente" -ForegroundColor Green
        } else {
            Write-Host "  ❌ Error instalando $dep" -ForegroundColor Red
        }
    }
}

# 3. Verificar archivos
Write-Host "`n📂 [3/4] Verificando archivos funcionales..." -ForegroundColor Yellow

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
        Write-Host "  ✅ $archivo" -ForegroundColor Green
        $archivosOK++
    } else {
        Write-Host "  ❌ $archivo (faltante)" -ForegroundColor Red
    }
}

if ($archivosOK -eq $archivos.Count) {
    Write-Host "`n  ✅ Todos los archivos presentes ($archivosOK/$($archivos.Count))" -ForegroundColor Green
} else {
    Write-Host "`n  ⚠️  Faltan archivos ($archivosOK/$($archivos.Count))" -ForegroundColor Yellow
}

# 4. Test rápido
Write-Host "`n🧪 [4/4] Test rápido de importación..." -ForegroundColor Yellow

$testImport = @"
try:
    from genesis_autopoiesis_funcional import GenesisAutopoiseisFuncional
    from tensor_ffe_funcional import TensorFFE
    print('✅ Imports exitosos')
except Exception as e:
    print(f'❌ Error: {e}')
"@

$resultado = $testImport | python 2>&1
$color = if ($resultado -match 'OK|exitoso') { 'Green' } else { 'Red' }
Write-Host "  $resultado" -ForegroundColor $color

# Resumen
Write-Host "`n" -NoNewline
Write-Host ("="*60) -ForegroundColor Cyan
Write-Host "📊 RESUMEN DE SETUP" -ForegroundColor Cyan
Write-Host ("="*60) -ForegroundColor Cyan

Write-Host "`n✅ Setup completado!" -ForegroundColor Green
Write-Host "`nPróximos pasos:" -ForegroundColor Yellow
Write-Host "  1. Ejecutar tests:  " -NoNewline -ForegroundColor White
Write-Host "python test_genesis_comparacion.py" -ForegroundColor Cyan
Write-Host "  2. Demo completo:   " -NoNewline -ForegroundColor White
Write-Host "python genesis_autopoiesis_funcional.py" -ForegroundColor Cyan
Write-Host "  3. Demo interactivo:" -NoNewline -ForegroundColor White
Write-Host ".\demo_genesis_interactivo.ps1" -ForegroundColor Cyan

Write-Host "`n📖 Documentación completa: GUIA_PRUEBAS_GENESIS_FUNCIONAL.md" -ForegroundColor Gray
Write-Host "`n"
