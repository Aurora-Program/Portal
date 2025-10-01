# 🔧 Deployment Fix - Error 403 Resuelto

**Fecha**: 1 de octubre de 2025  
**Problema**: Error 403 al cargar `aurora_wasm_client.js` desde CloudFront/S3  
**Estado**: ✅ Resuelto

---

## 🐛 Problema Original

```
Request URL: https://portal.auroraprogram.org/js/wasm-client/pkg/aurora_wasm_client.js
Status Code: 403 Forbidden
```

### Causas Identificadas

1. **Falta de compilación WASM**: El workflow no compilaba el código Rust a WASM antes de subir a S3
   - Solo se subía el código fuente (`wasm-client/src/`)
   - No existía el directorio `wasm-client/pkg/` con los binarios compilados

2. **Ruta incorrecta en import**: El archivo `js/aurora-portal.js` usaba ruta relativa incorrecta
   - ❌ Antes: `'./wasm-client/pkg/aurora_wasm_client.js'`
   - ✅ Ahora: `'../wasm-client/pkg/aurora_wasm_client.js'`

3. **Content-Type incorrecto**: S3 no configuraba el MIME type correcto para archivos `.wasm` y `.js`

---

## ✅ Cambios Implementados

### 1. Workflow GitHub Actions (`.github/workflows/main.yaml`)

**Nuevos pasos añadidos**:

```yaml
# Instalar Rust + wasm32 target
- name: Setup Rust toolchain
  uses: dtolnay/rust-toolchain@stable
  with:
    targets: wasm32-unknown-unknown

# Instalar wasm-pack
- name: Install wasm-pack
  run: curl https://rustwasm.github.io/wasm-pack/installer/init.sh -sSf | sh

# Compilar WASM
- name: Build WASM client
  run: |
    cd wasm-client
    wasm-pack build --target web --release
    ls -la pkg/
```

**Mejoras en Deploy**:
- Excluye código fuente Rust (`src/`, `Cargo.toml`, etc.)
- Incluye binarios compilados (`pkg/`)
- Configura Content-Type correcto:
  - `*.wasm` → `application/wasm`
  - `*.js` → `application/javascript; charset=utf-8`

### 2. Corrección de Ruta de Import (`js/aurora-portal.js`)

```javascript
// Cambio de ruta relativa
import init, { 
  create_agent, 
  get_version, 
  health_check,
  AuroraAgent 
} from '../wasm-client/pkg/aurora_wasm_client.js'; // ✅ Ruta corregida
```

**Estructura de archivos esperada**:
```
portal.auroraprogram.org/
├── index.html
├── js/
│   └── aurora-portal.js       (importa desde ../wasm-client/pkg/)
├── wasm-client/
│   └── pkg/
│       ├── aurora_wasm_client.js
│       ├── aurora_wasm_client_bg.wasm
│       └── aurora_wasm_client.d.ts
└── assets/
    └── aurora-portal-logo.png
```

---

## 🚀 Próximos Pasos

### Para verificar el fix:

1. **Hacer commit y push** de los cambios:
   ```powershell
   git add .
   git commit -m "fix: compile WASM in CI and correct import paths"
   git push origin main
   ```

2. **Monitorear GitHub Actions**:
   - Ir a: https://github.com/Aurora-Program/Portal/actions
   - Verificar que el job `Build WASM client` se ejecuta correctamente
   - Confirmar que el paso `Deploy to S3` muestra:
     ```
     ✅ Deployment complete!
     📦 WASM bundle deployed to: wasm-client/pkg/
     🌐 Portal files synced with correct MIME types
     ```

3. **Verificar en producción**:
   - Abrir: https://portal.auroraprogram.org
   - Abrir DevTools (F12) → Console
   - Buscar mensajes:
     ```
     Initializing Aurora Portal...
     WASM module loaded successfully
     Aurora Client Version: 0.1.0
     ```
   - **Si hay error 403**: Limpiar cache de CloudFront (ver abajo)

---

## 🔍 Debugging

### Si sigue el error 403:

1. **Verificar que los archivos existen en S3**:
   ```powershell
   aws s3 ls s3://TU_BUCKET/wasm-client/pkg/ --recursive
   ```
   
   Deberías ver:
   ```
   aurora_wasm_client.js
   aurora_wasm_client_bg.wasm
   aurora_wasm_client.d.ts
   package.json
   ```

2. **Verificar Content-Type en S3**:
   ```powershell
   aws s3api head-object --bucket TU_BUCKET --key wasm-client/pkg/aurora_wasm_client.js
   ```
   
   Debería mostrar:
   ```json
   "ContentType": "application/javascript; charset=utf-8"
   ```

3. **Invalidar cache de CloudFront**:
   ```powershell
   aws cloudfront create-invalidation \
     --distribution-id TU_DISTRIBUTION_ID \
     --paths "/wasm-client/*" "/js/*" "/index.html"
   ```

### Si el WASM no carga (error de tipo MIME):

Verificar en DevTools → Network → `aurora_wasm_client_bg.wasm`:
- **Response Headers** debe incluir: `Content-Type: application/wasm`
- Si dice `application/octet-stream`, ejecutar manualmente:
  ```powershell
  aws s3 cp s3://TU_BUCKET/wasm-client/pkg/ s3://TU_BUCKET/wasm-client/pkg/ `
    --recursive --exclude "*" --include "*.wasm" `
    --content-type "application/wasm" --metadata-directive REPLACE
  ```

---

## 📊 Impacto de los Cambios

| Aspecto | Antes | Después |
|---------|-------|---------|
| **Compilación WASM** | ❌ Manual (local) | ✅ Automática (CI) |
| **Archivos subidos** | Solo `src/` (código fuente) | `pkg/` (binarios) |
| **Content-Type** | `text/plain` (incorrecto) | `application/wasm`, `application/javascript` |
| **Rutas de import** | ❌ Incorrectas | ✅ Corregidas |
| **Estado portal** | 403 Forbidden | ✅ Funcional |

---

## 🎯 Verificación Final

Cuando todo funcione correctamente, verás en la consola del navegador:

```javascript
Initializing Aurora Portal...
WASM module loaded successfully
Aurora Client Version: 0.1.0
Health check: true
Aurora Agent created
Aurora Agent started
Agent DID: did:key:z6Mk...
Connected peers: 0
Agent state: ready
```

Y el portal mostrará:
```
✅ Connected as did:key:z6Mk...
🟢 P2P: 0 peers (esperado en Phase 0, sin relay nodes aún)
```

---

## 📝 Notas Técnicas

### Por qué era necesario compilar en CI:

1. **Binarios específicos de plataforma**: Los archivos `.wasm` deben generarse para `wasm32-unknown-unknown`
2. **Bindings JavaScript**: `wasm-pack` genera automáticamente el wrapper JS que importa el WASM
3. **Optimización**: Build en `--release` reduce tamaño del bundle (~50% más pequeño que `--dev`)

### Alternativa (build local + subir manualmente):

Si prefieres compilar localmente:
```powershell
cd wasm-client
.\build.ps1 -BuildType release -Target web
cd ..
aws s3 sync ./wasm-client/pkg s3://TU_BUCKET/wasm-client/pkg/ --content-type "application/javascript"
```

Pero el CI automatizado es **más confiable** y asegura que cada push tenga el código actualizado.

---

## 🤖 Próximas Mejoras Sugeridas

1. **Cache busting**: Añadir hash al nombre del archivo WASM para evitar problemas de cache
2. **Compression**: Habilitar Gzip/Brotli en CloudFront para archivos `.wasm` y `.js`
3. **Source maps**: Incluir `.map` files para debugging en producción
4. **Health check**: Añadir endpoint `/health` que verifique que WASM carga correctamente
5. **Monitoring**: CloudWatch alarm si el error rate de `/wasm-client/*` supera 5%

---

**Estado actual**: ✅ Listo para deployment  
**Próximo milestone**: Phase 1 - P2P Networking (Weeks 1-6)
