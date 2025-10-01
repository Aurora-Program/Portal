# Aurora Portal - Seguridad de Identidad: Solución Implementada

## Problema Identificado ✅

La clave privada está en localStorage, lo que tiene riesgos:
- Se pierde si borras cookies/datos del navegador
- Se pierde si cambias de dispositivo
- Vulnerable a XSS

## Solución Implementada (Phase 0.5)

### 1. **Export/Import Manual** ✅ (YA IMPLEMENTADO)
- Botón "Export Identity" descarga JSON con clave pública
- **FALTA**: Import para restaurar identidad

### 2. **Passkey (WebAuthn)** 🚧 (EN PROGRESO)
- Código creado en `wasm-client/src/passkey.rs`
- Usa Windows Hello / Touch ID / Face ID
- Clave nunca sale del dispositivo
- Requiere más testing

## Roadmap de Seguridad

### Phase 1 (Esta semana)
- [x] Export identidad (público + privado encriptado)
- [ ] Import identidad desde archivo
- [ ] Advertencia en UI sobre riesgo de localStorage
- [ ] Auto-backup a navegador cuando cambias

### Phase 2 (Próximas 2 semanas)
- [ ] Passkey como opción principal
- [ ] Selector de método (Passkey vs LocalStorage)
- [ ] Migración de LocalStorage → Passkey
- [ ] Multi-device sync via IPFS encriptado

### Phase 3 (1-2 meses)
- [ ] Recovery seeds (BIP39 compatible)
- [ ] Social recovery (N-of-M recovery con amigos)
- [ ] Hardware wallet integration (Ledger, Trezor)
- [ ] Encrypted cloud backup (opcional)

## Recomendaciones Inmediatas

**Para el usuario (AHORA):**
1. **Click en "Export Identity"** → Descarga el JSON
2. **Guarda ese archivo** en lugar seguro (USB, password manager)
3. Si pierdes tu localStorage, tendrás que regenerar (por ahora)

**Para desarrollo (PRÓXIMO):**
- Implementar import para restaurar desde JSON
- Añadir warning visible en UI
- Probar passkey en todos los navegadores

## Comparación de Métodos

| Método | Seguridad | UX | Portabilidad | Estado |
|--------|-----------|----|--------------| -------|
| **localStorage** | ⚠️ Baja | ✅ Simple | ❌ No | ✅ Actual |
| **Passkey** | ✅✅✅ Alta | ✅ Muy buena | ⚠️ Por dispositivo | 🚧 Código listo |
| **Export/Import** | ⚠️ Media | ⚠️ Manual | ✅ Sí | ✅ Partial |
| **Hardware Wallet** | ✅✅✅ Máxima | ⚠️ Compleja | ✅ Sí | ❌ Futuro |

## Decisión Arquitectónica

**Para Aurora Portal Phase 0:**
- Mantener localStorage como default (simplicidad)
- Añadir export COMPLETO (incluir clave privada encriptada)
- Añadir import para restaurar
- Documentar los riesgos claramente

**Para Phase 1 (producción):**
- Passkey como método recomendado
- localStorage como fallback
- Cloud backup opcional (encriptado end-to-end)

¿Proceder con esto?
