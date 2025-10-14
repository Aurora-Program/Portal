# 🔧 Solución Error 403 CORS en API Gateway

## Problema
```
Request URL: https://portal.auroraprogram.org/dev/discover?archetype=User
Request Method: OPTIONS
Status Code: 403 Forbidden
```

El API Gateway está rechazando las peticiones OPTIONS (CORS preflight).

## ✅ Solución 1: Habilitar CORS en API Gateway (AWS Console)

### Pasos:

1. **Ir a AWS Console:**
   - https://console.aws.amazon.com/apigateway

2. **Seleccionar tu API:**
   - Buscar: `aurora-p2p-discovery-dev`

3. **Para CADA recurso (/register, /discover, /heartbeat):**
   
   a) Click en el recurso (ejemplo: `/discover`)
   
   b) Click en "Actions" → "Enable CORS"
   
   c) Configurar:
   ```
   Access-Control-Allow-Origin: *
   Access-Control-Allow-Headers: Content-Type,X-Amz-Date,Authorization,X-Api-Key,Accept
   Access-Control-Allow-Methods: GET,POST,OPTIONS
   Access-Control-Allow-Credentials: false
   ```
   
   d) Click "Enable CORS and replace existing CORS headers"
   
   e) Confirmar

4. **Deploy API:**
   - Actions → Deploy API
   - Stage: `dev`
   - Click "Deploy"

5. **Esperar 30 segundos** y probar

## ✅ Solución 2: Actualizar vía CloudFormation

Agregar configuración explícita de CORS al API Gateway:

```yaml
# En cloudformation.yaml, agregar a cada método:

DiscoverMethod:
  Type: AWS::ApiGateway::Method
  Properties:
    # ... configuración existente ...
    MethodResponses:
      - StatusCode: 200
        ResponseParameters:
          method.response.header.Access-Control-Allow-Origin: true
          method.response.header.Access-Control-Allow-Headers: true
          method.response.header.Access-Control-Allow-Methods: true

# Y agregar método OPTIONS para cada recurso:

DiscoverOptionsMethod:
  Type: AWS::ApiGateway::Method
  Properties:
    AuthorizationType: NONE
    RestApiId: !Ref RestApi
    ResourceId: !Ref DiscoverResource
    HttpMethod: OPTIONS
    Integration:
      Type: MOCK
      IntegrationResponses:
        - StatusCode: 200
          ResponseParameters:
            method.response.header.Access-Control-Allow-Headers: "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,Accept'"
            method.response.header.Access-Control-Allow-Methods: "'GET,POST,OPTIONS'"
            method.response.header.Access-Control-Allow-Origin: "'*'"
          ResponseTemplates:
            application/json: ''
      RequestTemplates:
        application/json: '{"statusCode": 200}'
    MethodResponses:
      - StatusCode: 200
        ResponseParameters:
          method.response.header.Access-Control-Allow-Headers: true
          method.response.header.Access-Control-Allow-Methods: true
          method.response.header.Access-Control-Allow-Origin: true
```

Luego redesplegar:
```powershell
cd Infrastructure\P2P
.\deploy.ps1
```

## ✅ Solución 3: Usar proxy CORS (temporal)

En `aurora-chat.html`, cambiar:

```javascript
// Usar proxy público (temporal)
const DISCOVERY_SERVER_URL = 'https://cors-anywhere.herokuapp.com/https://portal.auroraprogram.org/dev';
```

**Nota:** Este proxy público tiene límite de rate.

## ✅ Solución 4: Crear proxy local

Crear servidor Node.js simple:

```javascript
// cors-proxy.js
const express = require('express');
const cors = require('cors');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();

app.use(cors());

app.use('/api', createProxyMiddleware({
  target: 'https://portal.auroraprogram.org/dev',
  changeOrigin: true,
  pathRewrite: {
    '^/api': ''
  }
}));

app.listen(8082, () => {
  console.log('CORS Proxy running on http://localhost:8082');
});
```

Ejecutar:
```bash
npm install express cors http-proxy-middleware
node cors-proxy.js
```

Cambiar URL en frontend:
```javascript
const DISCOVERY_SERVER_URL = 'http://localhost:8082/api';
```

## 🔍 Verificar que CORS está funcionando

### Test con curl:

```bash
# Test OPTIONS (preflight)
curl -X OPTIONS \
  -H "Origin: http://localhost:8001" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -v \
  https://portal.auroraprogram.org/dev/register

# Debe devolver:
# HTTP/2 200
# access-control-allow-origin: *
# access-control-allow-methods: GET,POST,OPTIONS
# access-control-allow-headers: Content-Type,...
```

### Test con JavaScript (consola del navegador):

```javascript
fetch('https://portal.auroraprogram.org/dev/health', {
  method: 'GET',
  mode: 'cors',
  headers: { 'Content-Type': 'application/json' }
})
.then(r => r.json())
.then(d => console.log('✅ CORS OK:', d))
.catch(e => console.error('❌ CORS Error:', e));
```

## 📊 Diagnosticar problema

### 1. Ver headers de respuesta:

En Chrome DevTools:
- Network tab
- Click en request OPTIONS
- Ver "Response Headers"
- Debe tener:
  ```
  access-control-allow-origin: *
  access-control-allow-methods: GET,POST,OPTIONS
  access-control-allow-headers: Content-Type,...
  ```

### 2. Ver logs de Lambda:

```powershell
aws logs tail /aws/lambda/aurora-discovery-dev --follow
```

Si ves requests OPTIONS llegando pero devolviendo 403, es problema de API Gateway, no Lambda.

### 3. Ver configuración actual:

```powershell
aws apigateway get-rest-apis --query 'items[?name==`aurora-p2p-discovery-dev`]'
```

## 🎯 Recomendación

**MEJOR SOLUCIÓN:** Usar Solución 1 (AWS Console) porque es rápida (5 minutos) y no requiere cambiar código.

**ORDEN DE PREFERENCIA:**
1. Solución 1 (AWS Console) - 5 min ⭐
2. Solución 4 (Proxy local) - 10 min si necesitas desarrollo
3. Solución 2 (CloudFormation) - 30 min, más robusto para producción
4. Solución 3 (Proxy público) - Solo para testing rápido

## ✅ Después de arreglar

Una vez CORS funcione, deberías ver en la consola:

```
✅ WASM Module cargado
✅ Peer registrado: {peer_id: "peer_abc123", ...}
💓 Heartbeat enviado
✅ Heartbeat iniciado (30s interval)
✅ Encontrados 2 peers
```

---

**Estado actual:** CORS bloqueado en API Gateway
**Acción requerida:** Habilitar CORS en AWS Console (Solución 1)
