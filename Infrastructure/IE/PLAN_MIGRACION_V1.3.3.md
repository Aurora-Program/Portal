# 🧹 PLAN DE MIGRACIÓN Y LIMPIEZA - Aurora v1.3.3 Funcional

## FECHA: 17 de Octubre de 2025

---

## 📋 ARCHIVOS A REEMPLAZAR (Originales → Funcionales)

### Core Modules (5 archivos)
| Original                    | Funcional                        | Estado    |
|-----------------------------|----------------------------------|-----------|
| `armonizador.py`            | `armonizador_funcional.py`       | ✅ Listo  |
| `transcender.py`            | `transcender_funcional.py`       | ✅ Listo  |
| `evolver.py`                | `evolver_funcional.py`           | ✅ Listo  |
| `tensor_ffe.py`             | `tensor_ffe_funcional.py`        | ✅ Listo  |
| `genesis_autopoiesis.py`    | `genesis_autopoiesis_funcional.py` | ✅ Listo  |

---

## 🗑️ ARCHIVOS A ELIMINAR (Obsoletos/Duplicados)

### 1. Versiones Antiguas/Optimizadas (no funcionales)
- [ ] `armonizador_optimizado.py` (reemplazado por funcional)

### 2. Tests Antiguos (ya validados)
- [ ] `test_armonizador.py` (antiguo)
- [ ] `test_simple.py` (básico)
- [ ] `test_genesis_integration.py` (antiguo)
- [ ] `test_genesis_fase6_7.py` (fase específica)
- [ ] `test_integracion_armonizador.py` (antiguo)
- [ ] `test_extender_simple.py` (básico)
- [ ] `test_pepino.py` (ejemplo)
- [ ] `test_recursive_network.py` (no necesario)
- [ ] `test_relator_tensor.py` (específico)
- [ ] `test_rotacion_fibonacci.py` (específico)

**MANTENER:**
- ✅ `test_genesis_comparacion.py` (validación principal)
- ✅ `test_benchmark_armonizador.py` (performance)
- ✅ `test_evolver_comparacion.py` (validación)
- ✅ `test_tensorffe_comparacion.py` (validación)

### 3. Documentación Antigua/Redundante
- [ ] `ARMONIZADOR_DOCUMENTATION.md` (versión antigua)
- [ ] `ARMONIZADOR_RESUMEN.md` (versión antigua)
- [ ] `BENCHMARK_CARD.md` (antiguo)
- [ ] `BENCHMARK_REVIEW.md` (antiguo)
- [ ] `BENCHMARK_TEMPLATE.md` (template)
- [ ] `COMPARATIVA_FIBONACCI.md` (redundante)
- [ ] `COMPLETITUD_SISTEMA.md` (antiguo)
- [ ] `EVOLVER_FUNCIONAL_V1.3.1.txt` (versión antigua)
- [ ] `GENESIS_ARCHITECTURE.md` (redundante)
- [ ] `GENESIS_AURORA_INTEGRATION.md` (redundante)
- [ ] `GENESIS_L3_INTEGRATION.md` (redundante)
- [ ] `GENESIS_QUICK_START.md` (redundante)
- [ ] `GENESIS_ROADMAP.md` (completado)
- [ ] `GENESIS_V1.1_FINAL_REPORT.md` (versión antigua)
- [ ] `GENESIS_V1.2_FASE6_ARREGLADA.md` (versión antigua)
- [ ] `GENESIS_V1.2_RESUMEN_EJECUTIVO.md` (versión antigua)
- [ ] `GENESIS_V1.2_VISUAL_SUMMARY.txt` (versión antigua)
- [ ] `GENESIS_V1.3_FUNCIONAL_PURO.txt` (versión antigua)
- [ ] `GOVERNANCE_IMPLEMENTATION.md` (no implementado)
- [ ] `INDEX.md` (redundante)
- [ ] `INDEX_COMPLETE.md` (redundante)
- [ ] `INTEGRACION_ARMONIZADOR.md` (redundante)
- [ ] `MAPEO_MANUAL_AURORA.md` (redundante)
- [ ] `MODULOS_FUNCIONALES_RESUMEN.txt` (redundante)
- [ ] `PEPINO_ARCHETYPE.md` (ejemplo)
- [ ] `PROGRESO_GENESIS_V1.1.md` (versión antigua)
- [ ] `PROYECTO_GENESIS.md` (redundante con README)
- [ ] `RECURSIVE_NETWORK_ARCHITECTURE.md` (redundante)
- [ ] `RESUMEN_3_PASOS.md` (proceso antiguo)
- [ ] `RESUMEN_4_PASOS_COMPLETO.md` (proceso antiguo)
- [ ] `ROTACION_FIBONACCI.md` (redundante)
- [ ] `SHARING_GUIDE.md` (no necesario)
- [ ] `TENSORFFE_FUNCIONAL_V1.3.2.txt` (versión antigua)

**MANTENER:**
- ✅ `RESUMEN_FINAL_V1.3.3.md` (resumen actual)
- ✅ `GENESIS_FUNCIONAL_V1.3.3.txt` (documentación técnica)
- ✅ `GUIA_PRUEBAS_GENESIS_FUNCIONAL.md` (guía de testing)
- ✅ `ESTADO_PROYECTO.md` (estado actual)
- ✅ `README.md` (principal)
- ✅ `README_GENESIS.md` (específico Genesis)
- ✅ `README_AURORA_ENGINE.md` (específico Engine)
- ✅ `README_ADAPTIVE_ECONOMICS.md` (específico Economics)

### 4. Scripts de Ejemplo Antiguos
- [ ] `ejemplo_genesis.py` (antiguo)
- [ ] `demo_aurora.py` (antiguo)
- [ ] `example_usage.py` (antiguo)
- [ ] `paso1_analizar_arquetipos.py` (proceso viejo)
- [ ] `paso2_analizar_relatores.py` (proceso viejo)
- [ ] `paso3_razonamiento_estructural.py` (proceso viejo)
- [ ] `paso4_extender.py` (proceso viejo)
- [ ] `pepino_archetype.py` (ejemplo)

**MANTENER:**
- ✅ `genesis_aurora_client.py` (cliente actual)
- ✅ `monitor_genesis.py` (monitor)
- ✅ `show_genesis_results.py` (utilidad)

### 5. Archivos de Log/Output Antiguos
- [ ] `autopoiesis_log.txt` (log antiguo)
- [ ] `genesis_log.txt` (log antiguo)
- [ ] `paso1_fibonacci_output.txt` (output viejo)
- [ ] `paso1_output.txt` (output viejo)
- [ ] `paso2_output.txt` (output viejo)
- [ ] `paso4_output.txt` (output viejo)

### 6. JSON de Resultados Antiguos
- [ ] `analisis_arquetipos.json` (viejo)
- [ ] `analisis_relatores.json` (viejo)
- [ ] `benchmark_fractal_aurora.json` (viejo)
- [ ] `benchmark_results.json` (viejo)
- [ ] `genesis_autopoiesis_results.json` (viejo)
- [ ] `genesis_fase6_7_test.json` (viejo)
- [ ] `genesis_v1.1.json` (viejo)
- [ ] `paso3_razonamiento.json` (viejo)
- [ ] `paso4_extender.json` (viejo)
- [ ] `test_armonizador_results.json` (viejo)
- [ ] `test_extender_simple.json` (viejo)

### 7. Scripts PowerShell Antiguos
- [ ] `setup_genesis_funcional.ps1` (tiene errores, usar _fix)

**MANTENER:**
- ✅ `setup_genesis_funcional_fix.ps1` (setup funcional)
- ✅ `demo_genesis_interactivo.ps1` (demos)
- ✅ `start_api.ps1` (API starter)

---

## ✅ ARCHIVOS A MANTENER (Esenciales)

### Core Production Code
1. `armonizador_funcional.py`
2. `transcender_funcional.py`
3. `evolver_funcional.py`
4. `tensor_ffe_funcional.py`
5. `genesis_autopoiesis_funcional.py`
6. `ffe_encoder.py` (alias)
7. `ffe_encoder_mcp.py` (MCP server)
8. `aurora_engine.py` (engine)
9. `aurora_api.py` (API)
10. `aurora_mcp_server.py` (MCP server)
11. `core.py` (core utilities)
12. `adaptive_economics.py` (economics)
13. `lora_ffe.py` (LoRA)
14. `extender.py` (extender)

### Testing & Validation
1. `test_genesis_comparacion.py` (principal)
2. `test_benchmark_armonizador.py` (performance)
3. `test_evolver_comparacion.py` (validación)
4. `test_tensorffe_comparacion.py` (validación)
5. `validate_system.py` (validación sistema)

### Documentation (Esencial)
1. `RESUMEN_FINAL_V1.3.3.md` (resumen ejecutivo)
2. `GENESIS_FUNCIONAL_V1.3.3.txt` (doc técnica)
3. `GUIA_PRUEBAS_GENESIS_FUNCIONAL.md` (testing)
4. `ESTADO_PROYECTO.md` (estado)
5. `README.md` (principal)
6. `README_GENESIS.md` (Genesis)
7. `README_AURORA_ENGINE.md` (Engine)
8. `README_ADAPTIVE_ECONOMICS.md` (Economics)

### Tools & Utilities
1. `setup_genesis_funcional_fix.ps1` (setup)
2. `demo_genesis_interactivo.ps1` (demos)
3. `start_api.ps1` (API)
4. `genesis_aurora_client.py` (client)
5. `monitor_genesis.py` (monitor)
6. `show_genesis_results.py` (results)
7. `requirements.txt` (dependencies)
8. `__init__.py` (package)

### API & Testing
1. `demo_api.py` (API demo)
2. `test_api.py` (API test)
3. `test_api_functional.py` (API functional test)
4. `quick_test_api.py` (API quick test)

### Benchmarking
1. `benchmark_genesis.py` (Genesis benchmark)
2. `benchmark_downstream.py` (downstream)
3. `benchmark_fractal_aurora.py` (fractal)

---

## 🔄 ACCIONES A EJECUTAR

### Fase 1: Backup
```bash
# Crear carpeta de backup
mkdir backup_v1.2
```

### Fase 2: Mover archivos obsoletos a backup
```bash
# Mover versiones antiguas, logs, docs obsoletas
```

### Fase 3: Renombrar archivos funcionales
```bash
# armonizador_funcional.py → armonizador.py
# transcender_funcional.py → transcender.py
# evolver_funcional.py → evolver.py
# tensor_ffe_funcional.py → tensor_ffe.py
# genesis_autopoiesis_funcional.py → genesis_autopoiesis.py
```

### Fase 4: Actualizar imports en archivos que usan los módulos
```python
# Buscar y reemplazar imports en:
# - aurora_engine.py
# - aurora_api.py
# - aurora_mcp_server.py
# - ffe_encoder_mcp.py
# - genesis_aurora_client.py
# - Tests
```

### Fase 5: Eliminar archivos backup después de validación
```bash
# rm -rf backup_v1.2
```

---

## 📊 RESUMEN DE LIMPIEZA

**Archivos actuales:** ~150  
**Archivos después:** ~40 (73% reducción)

**Categorías eliminadas:**
- 10 tests antiguos
- 35 documentos obsoletos
- 8 scripts de ejemplo viejos
- 5 logs antiguos
- 12 JSON de resultados viejos
- 1 script PowerShell con errores

**Categorías mantenidas:**
- 14 módulos core (producción)
- 5 tests de validación
- 8 documentos esenciales
- 8 herramientas y utilidades
- 4 scripts API/testing
- 3 benchmarks

---

## ⚠️ PRECAUCIONES

1. ✅ Crear backup completo antes de eliminar
2. ✅ Validar que los tests pasan después del renombrado
3. ✅ Actualizar todos los imports
4. ✅ Verificar que API/MCP funcionen
5. ✅ Mantener un commit de Git antes de limpiar

---

**¿Proceder con la migración?**
