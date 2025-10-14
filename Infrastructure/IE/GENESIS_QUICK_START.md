# 🚀 Genesis L3 Integration - Quick Start

**Para:** Dev Team  
**Objetivo:** Iniciar implementación de Genesis en Layer 3  
**Tiempo estimado:** 30 minutos setup inicial  

---

## ⚡ Inicio Inmediato (Hoy)

### 🔴 **Prioridad 1: Resolver CORS (5 minutos)**

**Problema:** Discovery Server retorna 403 Forbidden en OPTIONS requests.

**Solución rápida:**

```powershell
# Opción 1: Via AWS Console (recomendado)
# 1. Ir a: https://console.aws.amazon.com/apigateway
# 2. Buscar: aurora-p2p-discovery-dev
# 3. Para cada recurso (/register, /discover, /heartbeat):
#    - Clic derecho → Actions → Enable CORS
#    - Enable CORS → Yes, replace existing values
# 4. Deploy API en stage "dev"

# Opción 2: Re-deploy con script (alternativa)
cd Infrastructure\P2P
.\deploy.ps1
```

**Verificación:**

```powershell
# Test CORS
curl -X OPTIONS https://portal.auroraprogram.org/dev/register `
  -H "Origin: http://localhost:8001" `
  -H "Access-Control-Request-Method: POST" `
  -v

# Debe retornar 200 OK con headers:
# Access-Control-Allow-Origin: *
# Access-Control-Allow-Methods: POST,GET,OPTIONS
```

---

### 🔴 **Prioridad 2: Configurar Genesis Repo (10 minutos)**

**Ubicación Genesis:** Necesitas el repo de Genesis localmente.

```powershell
# Si Genesis está en C:\Users\p_m_a\Aurora\Genesis
cd C:\Users\p_m_a\Aurora

# Verificar que existe
ls Genesis

# Debe mostrar:
# - src/
# - Cargo.toml
# - tests/
# - README.md
```

**Si NO existe Genesis:**

```powershell
# Opción A: Clonar si está en GitHub
git clone https://github.com/Aurora-Program/Genesis.git
cd Genesis

# Opción B: Copiar desde backup/otra ubicación
# (ajustar path según tu caso)
```

**Instalar dependencias Rust:**

```powershell
# Verificar Rust instalado
rustc --version
# Si no: https://rustup.rs/

# Agregar target WASM
rustup target add wasm32-unknown-unknown

# Instalar wasm-bindgen
cargo install wasm-bindgen-cli

# Verificar
wasm-bindgen --version
```

---

### 🔴 **Prioridad 3: Compilar Genesis a WASM (15 minutos)**

**Paso 1: Preparar Cargo.toml**

```powershell
cd C:\Users\p_m_a\Aurora\Genesis
```

Editar `Cargo.toml`:

```toml
[package]
name = "genesis-core"
version = "0.3.1"

[lib]
crate-type = ["cdylib", "rlib"]  # ← Agregar esto

[dependencies]
# Dependencias existentes...

# Agregar para WASM:
wasm-bindgen = "0.2"
serde-wasm-bindgen = "0.6"
js-sys = "0.3"

[dependencies.web-sys]
version = "0.3"
features = ["console"]
```

**Paso 2: Crear wrapper WASM**

```powershell
# Crear archivo src/wasm_bindings.rs
```

Contenido:

```rust
// src/wasm_bindings.rs
use wasm_bindgen::prelude::*;
use serde::{Deserialize, Serialize};

// Re-export estructuras principales
use crate::{GenesisEngine, TurnResult, Coherence, Synthesis};

#[wasm_bindgen]
pub struct GenesisWASM {
    engine: GenesisEngine,
    model_id: String,
}

#[wasm_bindgen]
impl GenesisWASM {
    #[wasm_bindgen(constructor)]
    pub fn new(model_id: String, space_id: String) -> Result<GenesisWASM, JsValue> {
        // Inicializar engine
        let engine = GenesisEngine::new(&space_id)
            .map_err(|e| JsValue::from_str(&e))?;
        
        web_sys::console::log_1(&format!("✅ Genesis initialized: {}", model_id).into());
        
        Ok(GenesisWASM { engine, model_id })
    }
    
    #[wasm_bindgen]
    pub async fn process_turn(
        &self,
        user_text: String,
        model_text: String,
    ) -> Result<JsValue, JsValue> {
        // Procesar con Genesis
        let result = self.engine.process_turn(&user_text, &model_text)
            .map_err(|e| JsValue::from_str(&e))?;
        
        // Convertir a JsValue
        serde_wasm_bindgen::to_value(&result)
            .map_err(|e| JsValue::from_str(&e.to_string()))
    }
    
    #[wasm_bindgen]
    pub fn get_model_id(&self) -> String {
        self.model_id.clone()
    }
}
```

**Paso 3: Agregar a lib.rs**

```rust
// src/lib.rs (agregar al inicio)
#[cfg(target_arch = "wasm32")]
pub mod wasm_bindings;

#[cfg(target_arch = "wasm32")]
pub use wasm_bindings::*;
```

**Paso 4: Compilar**

```powershell
# Build WASM
cargo build --target wasm32-unknown-unknown --release

# Debería crear:
# target/wasm32-unknown-unknown/release/genesis_core.wasm
```

**Paso 5: Generar bindings JavaScript**

```powershell
# Crear directorio de salida
mkdir -Force wasm-bindings

# Generar bindings
wasm-bindgen target/wasm32-unknown-unknown/release/genesis_core.wasm `
    --out-dir wasm-bindings `
    --typescript `
    --target web

# Verificar archivos generados:
ls wasm-bindings

# Debe mostrar:
# - genesis_core_bg.wasm
# - genesis_core.js
# - genesis_core.d.ts
```

**Paso 6: Copiar a Portal**

```powershell
# Crear directorio en Portal
cd C:\Users\p_m_a\Aurora\Portal\Portal
mkdir -Force wasm-client\pkg\genesis

# Copiar bindings
Copy-Item C:\Users\p_m_a\Aurora\Genesis\wasm-bindings\* `
    -Destination .\wasm-client\pkg\genesis\ `
    -Force

# Verificar
ls wasm-client\pkg\genesis
```

---

## ✅ Checklist Post-Setup

Después de estos 3 pasos, verificar:

```powershell
# 1. CORS resuelto
curl https://portal.auroraprogram.org/dev/discover

# 2. Genesis compilado
ls C:\Users\p_m_a\Aurora\Genesis\wasm-bindings\genesis_core_bg.wasm

# 3. Bindings copiados a Portal
ls C:\Users\p_m_a\Aurora\Portal\Portal\wasm-client\pkg\genesis\genesis_core.js

# 4. Tamaño WASM
(Get-Item wasm-client\pkg\genesis\genesis_core_bg.wasm).Length / 1MB
# Debe ser < 5MB
```

---

## 🧪 Test Rápido

Crear archivo de prueba:

```powershell
cd C:\Users\p_m_a\Aurora\Portal\Portal
```

**test-genesis.html:**

```html
<!DOCTYPE html>
<html>
<head>
    <title>Genesis WASM Test</title>
</head>
<body>
    <h1>Genesis WASM Test</h1>
    <button id="test-btn">Test Genesis</button>
    <pre id="output"></pre>
    
    <script type="module">
        import init, { GenesisWASM } from './wasm-client/pkg/genesis/genesis_core.js';
        
        document.getElementById('test-btn').addEventListener('click', async () => {
            const output = document.getElementById('output');
            
            try {
                // Inicializar WASM
                await init();
                output.textContent += '✅ WASM initialized\n';
                
                // Crear Genesis
                const genesis = new GenesisWASM(
                    "0xTEST123",
                    "test_space"
                );
                output.textContent += '✅ Genesis created\n';
                
                // Test process_turn
                const result = await genesis.process_turn(
                    "Test user input",
                    "Test model response"
                );
                
                output.textContent += '✅ Process turn succeeded\n';
                output.textContent += JSON.stringify(result, null, 2);
                
            } catch (error) {
                output.textContent += '❌ Error: ' + error.message;
            }
        });
    </script>
</body>
</html>
```

**Ejecutar test:**

```powershell
# Iniciar servidor local
python -m http.server 8001

# Abrir en navegador
start http://localhost:8001/test-genesis.html

# Click "Test Genesis" → debe ver:
# ✅ WASM initialized
# ✅ Genesis created
# ✅ Process turn succeeded
# { "coherence": { "C_meta": 0.xx, ... } }
```

---

## 📋 Próximos Pasos (Después de Setup)

Una vez completado el setup inicial:

1. **Generar Model ID** (1 día)
   - Script Python para hash del ModelPack
   - Subir a IPFS
   - Documentar en MODEL_REGISTRY.md

2. **Deploy Smart Contract** (2 días)
   - Crear AuroraRegistry.sol
   - Deploy a Sepolia testnet
   - Registrar Genesis model_id

3. **Integrar en aurora-chat.html** (3 días)
   - Importar Genesis WASM
   - Función initGenesis()
   - Panel de coherencia en UI
   - Tests de integración

Ver **GENESIS_ROADMAP.md** para roadmap completo.

---

## 🆘 Troubleshooting

### Error: "CORS still failing"

```powershell
# Verificar headers en Lambda
cd Infrastructure\P2P
code cloudformation.yaml

# Buscar líneas 140-142:
# 'Access-Control-Allow-Origin': '*'
# Si no están, agregarlas y re-deploy

.\deploy.ps1
```

### Error: "wasm-bindgen not found"

```powershell
cargo install wasm-bindgen-cli --force
```

### Error: "Genesis crate not found"

```powershell
# Verificar path
cd C:\Users\p_m_a\Aurora\Genesis
cargo build

# Si falla, verificar Cargo.toml existe
```

### Error: "WASM file too large (>5MB)"

```powershell
# Optimizar con wasm-opt
cargo install wasm-opt

wasm-opt target/wasm32-unknown-unknown/release/genesis_core.wasm `
    -O3 -o genesis_core_optimized.wasm

# Usar optimized version
wasm-bindgen genesis_core_optimized.wasm ...
```

---

## 📞 Contacto

- **Roadmap completo:** `Infrastructure/IE/GENESIS_ROADMAP.md`
- **Arquitectura:** `Infrastructure/IE/GENESIS_L3_INTEGRATION.md`
- **Issues:** GitHub Issues (si aplica)

---

## ⏱️ Timeline Esperado

| Tarea | Tiempo | Status |
|-------|--------|--------|
| Resolver CORS | 5 min | ⏳ |
| Setup Genesis Repo | 10 min | ⏳ |
| Compilar a WASM | 15 min | ⏳ |
| **Total Setup** | **30 min** | ⏳ |
| | | |
| Test Rápido | 10 min | 🔜 |
| Generar Model ID | 1 día | 🔜 |
| Deploy Contracts | 2 días | 🔜 |
| Integración Full | 3 días | 🔜 |

---

## 🎯 Objetivo de Hoy

Al final de hoy, deberías tener:

✅ CORS resuelto → P2P funcionando  
✅ Genesis compilado a WASM  
✅ Bindings en Portal  
✅ Test básico passing  

**Próxima sesión:** Generar Model ID y registrar en blockchain.

---

🐹 **Aurora Portal** - *Building the future through ethical intelligence.*

**Última actualización:** 2025-10-14  
**Versión:** 1.0
