# Autenticación Descentralizada en Aurora Portal

## Resumen

Aurora Portal implementa autenticación **100% descentralizada** usando las APIs nativas del navegador (Web Crypto API / SubtleCrypto). No hay dependencias de terceros como MetaMask, WalletConnect, o servicios centralizados.

## Arquitectura

### 1. Generación de Identidad

Cuando un usuario accede por primera vez:

```
Usuario → Portal → Web Crypto API
                      ↓
              ECDSA P-256 Keypair
                      ↓
         ┌────────────┴────────────┐
         ↓                         ↓
    Private Key              Public Key (JWK)
   (no-extractable)               ↓
   almacenada en              SHA-256 hash
   navegador                       ↓
                         DID: did:aurora:ecdsa:{hash}
```

**Características:**
- Keypair ECDSA P-256 (estándar NIST, amplio soporte)
- Clave privada **no-extractable** (máxima seguridad)
- Clave pública exportada en formato JWK (JSON Web Key)
- DID derivado del hash SHA-256 de la clave pública

### 2. Almacenamiento

```
┌─────────────────────────────────────┐
│ localStorage: "aurora_identity"     │
│                                     │
│ {                                   │
│   "did": "did:aurora:ecdsa:...",   │
│   "public_key_jwk": "{...}"        │
│ }                                   │
│                                     │
│ Nota: La clave privada NUNCA       │
│ sale del navegador                  │
└─────────────────────────────────────┘
```

**Persistencia:**
- Público: localStorage (DID + clave pública)
- Privado: Browser's CryptoKey store (clave privada protegida)

### 3. Firma de Mensajes

```
Message → ECDSA Sign (SHA-256) → Signature
              ↑
         Private Key
    (accedida vía SubtleCrypto)
```

**Proceso:**
1. Usuario quiere firmar un mensaje/transacción
2. Browser pide confirmación (opcional: implementar UI)
3. SubtleCrypto.sign() usa la clave privada sin exponerla
4. Retorna firma digital (DER encoded)

### 4. Verificación de Firmas

```
Message + Signature + Public Key JWK
              ↓
    SubtleCrypto.verify()
              ↓
         true/false
```

**Características:**
- Cualquiera puede verificar con la clave pública
- No requiere acceso a la clave privada
- Verificación criptográficamente segura

## Formato DID

```
did:aurora:ecdsa:<identifier>
│   │      │     │
│   │      │     └─ 20 primeros bytes del SHA-256(public_key_jwk)
│   │      └─────── Algoritmo de firma (ecdsa)
│   └────────────── Método (aurora)
└────────────────── Esquema DID (W3C standard)
```

**Ejemplo:**
```
did:aurora:ecdsa:1a2b3c4d5e6f7890abcdef1234567890abcdef12
```

## Ventajas vs Alternativas

### vs MetaMask/WalletConnect:
✅ Sin dependencias externas
✅ Sin necesidad de extensión del navegador
✅ Usuario no necesita ya tener wallet
✅ No hay "sign in with Ethereum" popup
❌ Pero: No hay integración directa con DeFi existente

### vs Ed25519 (libp2p tradicional):
✅ Compatible con WASM sin problemas de getrandom
✅ APIs nativas del browser (bien optimizadas)
✅ Soportado universalmente (Chrome, Firefox, Safari, Edge)
❌ Pero: Firmas ECDSA más grandes que Ed25519 (64-72 bytes vs 64 bytes)

### vs OAuth/JWT (centralizado):
✅ 100% descentralizado (sin servidor de auth)
✅ Usuario controla sus claves
✅ Compatible con blockchain sin modificaciones
✅ No hay single point of failure

## Seguridad

### Amenazas Mitigadas:

1. **Extracción de clave privada**: 
   - Clave marcada como `extractable: false`
   - Solo accesible vía SubtleCrypto API

2. **XSS (Cross-Site Scripting)**:
   - Clave privada no en memoria JavaScript
   - Firma requiere llamada explícita a SubtleCrypto

3. **Man-in-the-Middle**:
   - Portal servido via HTTPS (CloudFront)
   - Firmas verificables independientemente

4. **Phishing**:
   - DID único por usuario
   - Verificación de firma en blockchain/P2P

### Consideraciones:

⚠️ **localStorage puede ser limpiado**: 
- Solución: Exportar/Importar identidad
- Futura: Backup encriptado en IPFS

⚠️ **Sin recuperación de cuenta**:
- No hay "forgot password"
- Usuario debe hacer backup de su identidad
- Futura: Recovery seeds (BIP39 compatible)

⚠️ **Dispositivo comprometido**:
- Si el browser está comprometido, la clave puede ser usada
- Solución: Hardware security keys (WebAuthn integration - Phase 2)

## Roadmap

### Phase 0 (Actual) ✅
- Generación de identidad ECDSA
- Almacenamiento en localStorage
- DIDs básicos

### Phase 1 (Próximas 2 semanas)
- [ ] Implementar firma real con SubtleCrypto
- [ ] Verificación de firmas P2P
- [ ] Exportar/Importar identidad (JSON)
- [ ] UI para gestión de identidad

### Phase 2 (1-2 meses)
- [ ] Multi-device sync (IPFS encrypted backup)
- [ ] Recovery seeds (BIP39)
- [ ] WebAuthn integration (hardware keys)
- [ ] Delegated signing (multi-sig)

### Phase 3 (3-6 meses)
- [ ] Zero-knowledge proofs (zk-SNARKs)
- [ ] Credential issuance/verification
- [ ] DID Document management
- [ ] Interoperabilidad con otros sistemas DID

## Ejemplo de Uso

```javascript
// En el navegador:

// 1. Inicializar portal (genera/carga identidad)
const portal = new AuroraPortal();
await portal.initialize();

// 2. Obtener DID del usuario
const userDid = portal.agent.get_did();
console.log('User DID:', userDid);
// → "did:aurora:ecdsa:1a2b3c..."

// 3. Firmar un mensaje (futura implementación)
const message = "Register model: QmABC123...";
const signature = await portal.agent.sign(message);

// 4. Otro peer verifica la firma
const isValid = await verify_signature(
    userDid,
    message,
    signature
);
console.log('Signature valid:', isValid);
```

## Referencias

- [W3C DID Specification](https://www.w3.org/TR/did-core/)
- [Web Crypto API (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/Web_Crypto_API)
- [ECDSA P-256 (NIST)](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-4.pdf)
- [JSON Web Key (RFC 7517)](https://tools.ietf.org/html/rfc7517)

## Contribuir

Si encuentras un problema de seguridad, por favor NO abras un issue público. Contacta a security@auroraprogram.org

Para contribuciones generales, ver [CONTRIBUTING.md](../CONTRIBUTING.md)
