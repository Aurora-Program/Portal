"""
Aurora IE API Gateway
=====================

API única que actúa como interfaz entre el usuario autenticado y toda la red Aurora.
Después de la autenticación P2P, este API gateway maneja:
- Tokenización y sesión
- Acceso al IE Aurora (core.py)
- Operaciones de tensores
- Comunicación con peers
- Knowledge Base queries

Author: Aurora Alliance
License: Apache-2.0
Version: 1.0.0
"""

from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import jwt
import secrets
import hashlib
import time
from datetime import datetime, timedelta
import logging

# Import Aurora core
import sys
import os

# Agregar directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core import (
    FractalTensor,
    Trigate,
    FractalKnowledgeBase,
    Evolver,
    Extender,
    Transcender,
    Armonizador,
    pattern0_create_fractal_cluster
)

# Import Adaptive Economics (Gobernanza por Modelos)
from adaptive_economics import (
    AdaptiveEconomicsCoordinator,
    NetworkState,
    MERIT_CONFIG,
    MIND_CONFIG,
    TRUST_CONFIG,
    TRUST_REWARDS
)

# ===============================================================================
# CONFIGURATION
# ===============================================================================

# Secret key for JWT - en producción esto debe estar en variables de entorno
JWT_SECRET = secrets.token_hex(32)
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

# Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("aurora.api")

# ===============================================================================
# FASTAPI APP
# ===============================================================================

app = FastAPI(
    title="Aurora IE API Gateway",
    description="API Gateway para acceso a la Inteligencia Aurora",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción: especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===============================================================================
# IN-MEMORY STORES (en producción usar Redis/DB)
# ===============================================================================

# Sesiones activas: {token: session_data}
active_sessions: Dict[str, Dict[str, Any]] = {}

# Knowledge Bases por usuario: {user_id: FractalKnowledgeBase}
user_kbs: Dict[str, FractalKnowledgeBase] = {}

# Metrics
metrics = {
    "total_requests": 0,
    "active_sessions": 0,
    "tensor_operations": 0,
    "kb_queries": 0
}

# ADAPTIVE ECONOMICS COORDINATOR
# Sistema de gobernanza donde los usuarios entrenan modelos que votan sobre políticas
economics_coordinator = AdaptiveEconomicsCoordinator()

# Modelos de usuarios: {user_id: model_id}
user_models: Dict[str, str] = {}

# ===============================================================================
# MODELS
# ===============================================================================

class AuthRequest(BaseModel):
    """Request de autenticación desde P2P"""
    peer_id: str = Field(..., description="ID del peer P2P")
    did: Optional[str] = Field(None, description="DID (si usa Passkey)")
    signature: Optional[str] = Field(None, description="Firma de autenticación")
    archetypes: List[str] = Field(default_factory=list, description="Arquetipos del agente")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata adicional")

class AuthResponse(BaseModel):
    """Response de autenticación con token"""
    success: bool
    token: str
    expires_at: str
    user_id: str
    session_id: str
    message: str

class TensorCreate(BaseModel):
    """Request para crear tensor"""
    nivel_3: Optional[List[List[int]]] = Field(None, description="Nivel 3 del tensor")
    random: bool = Field(False, description="Generar tensor aleatorio")
    space_id: str = Field("default", description="ID del espacio lógico")

class TensorQuery(BaseModel):
    """Query para buscar tensors"""
    space_id: str = Field("default", description="Espacio lógico")
    archetype_name: Optional[str] = Field(None, description="Nombre del arquetipo")
    Ms_query: Optional[List[int]] = Field(None, description="Vector Ms para búsqueda")

class TensorSynthesis(BaseModel):
    """Request para síntesis de tensors"""
    tensor_a_key: str = Field(..., description="Key del tensor A")
    tensor_b_key: str = Field(..., description="Key del tensor B")
    space_id: str = Field("default", description="Espacio lógico")

class ExtendQuery(BaseModel):
    """Query para extensión fractal"""
    ss_query: List[int] = Field(..., description="Vector Ss para extensión")
    space_id: str = Field("default", description="Espacio lógico")
    use_recursive: bool = Field(False, description="Usar red recursiva de deducción")

class CollaborativeTask(BaseModel):
    """Tarea colaborativa entre peers"""
    task_type: str = Field(..., description="Tipo de tarea (synthesis, training, etc)")
    peer_ids: List[str] = Field(..., description="IDs de peers involucrados")
    data: Dict[str, Any] = Field(..., description="Datos de la tarea")

# ===============================================================================
# GOVERNANCE MODELS (Adaptive Economics)
# ===============================================================================

class TrainModelRequest(BaseModel):
    """Request para entrenar modelo de usuario con una interacción"""
    interaccion: Dict[str, Any] = Field(..., description="Datos de la interacción")

class VotePolicyRequest(BaseModel):
    """Request para votar sobre una política económica"""
    politica: str = Field(..., description="Nombre de la política")
    valor_propuesto: float = Field(..., description="Valor propuesto para la política")

class NetworkStateReport(BaseModel):
    """Reporte de estado de la red (para procesar bloques)"""
    nodos_activos: int
    latencia_promedio_ms: float
    operaciones_por_hora: int
    coherencia_promedio: float
    fees_acumuladas: Dict[str, float]

class ComputeRewardRequest(BaseModel):
    """Request para recompensa por cómputo"""
    tipo_operacion: str = Field(..., description="Tipo de operación (pattern0, extend_recursive, etc)")
    complejidad: float = Field(..., description="Complejidad fractal (0.0 a 1.0)")
    coherencia: float = Field(..., description="Coherencia del resultado")
    es_colaborativa: bool = Field(False, description="Si es colaboración multi-peer")

class TrustInteractionRequest(BaseModel):
    """Request para validar interacción humana y emitir TRUST"""
    tipo: str = Field(..., description="Tipo de interacción (mentoria_completada, etc)")
    peer_b: str = Field(..., description="ID del otro peer")
    firma_a: str = Field(..., description="Firma del peer A")
    firma_b: str = Field(..., description="Firma del peer B")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata adicional")

# ===============================================================================
# AUTHENTICATION & SESSION MANAGEMENT
# ===============================================================================

def create_token(user_id: str, peer_id: str, archetypes: List[str]) -> tuple[str, datetime]:
    """Crea un JWT token para el usuario"""
    expiration = datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    
    payload = {
        "user_id": user_id,
        "peer_id": peer_id,
        "archetypes": archetypes,
        "exp": expiration,
        "iat": datetime.utcnow(),
        "session_id": secrets.token_hex(16)
    }
    
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token, expiration

def verify_token(token: str) -> Dict[str, Any]:
    """Verifica y decodifica el JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

async def get_current_user(authorization: str = Header(None)):
    """Dependency para obtener usuario actual desde token"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token no proporcionado")
    
    token = authorization.split(" ")[1]
    payload = verify_token(token)
    
    # Verificar que la sesión esté activa
    if token not in active_sessions:
        raise HTTPException(status_code=401, detail="Sesión no válida")
    
    return payload

def get_user_kb(user_id: str) -> FractalKnowledgeBase:
    """Obtiene o crea la Knowledge Base del usuario"""
    if user_id not in user_kbs:
        user_kbs[user_id] = FractalKnowledgeBase()
        logger.info(f"Created new KB for user {user_id}")
    return user_kbs[user_id]

# ===============================================================================
# AUTHENTICATION ENDPOINTS
# ===============================================================================

@app.post("/api/v1/auth/login", response_model=AuthResponse)
async def login(auth_req: AuthRequest):
    """
    Autenticación después del handshake P2P.
    Genera un token JWT para acceso al API.
    """
    metrics["total_requests"] += 1
    
    # Generar user_id basado en peer_id y DID (si existe)
    if auth_req.did:
        user_id = hashlib.sha256(f"{auth_req.did}:{auth_req.peer_id}".encode()).hexdigest()[:16]
    else:
        user_id = hashlib.sha256(auth_req.peer_id.encode()).hexdigest()[:16]
    
    # Crear token
    token, expiration = create_token(user_id, auth_req.peer_id, auth_req.archetypes)
    session_id = secrets.token_hex(16)
    
    # Guardar sesión
    active_sessions[token] = {
        "user_id": user_id,
        "peer_id": auth_req.peer_id,
        "archetypes": auth_req.archetypes,
        "created_at": datetime.utcnow().isoformat(),
        "expires_at": expiration.isoformat(),
        "session_id": session_id,
        "metadata": auth_req.metadata
    }
    
    metrics["active_sessions"] = len(active_sessions)
    
    # Inicializar Knowledge Base del usuario
    get_user_kb(user_id)
    
    logger.info(f"🐹 User {user_id} authenticated with peer_id {auth_req.peer_id}")
    
    return AuthResponse(
        success=True,
        token=token,
        expires_at=expiration.isoformat(),
        user_id=user_id,
        session_id=session_id,
        message=f"Welcome to Aurora Network, {auth_req.peer_id}! 🐹"
    )

@app.post("/api/v1/auth/logout")
async def logout(current_user: Dict = Depends(get_current_user), authorization: str = Header(None)):
    """Cierra la sesión del usuario"""
    token = authorization.split(" ")[1]
    
    if token in active_sessions:
        del active_sessions[token]
        metrics["active_sessions"] = len(active_sessions)
        logger.info(f"User {current_user['user_id']} logged out")
        return {"success": True, "message": "Logged out successfully"}
    
    return {"success": False, "message": "Session not found"}

@app.get("/api/v1/auth/session")
async def get_session(current_user: Dict = Depends(get_current_user)):
    """Obtiene información de la sesión actual"""
    return {
        "success": True,
        "session": {
            "user_id": current_user["user_id"],
            "peer_id": current_user["peer_id"],
            "archetypes": current_user["archetypes"],
            "session_id": current_user["session_id"],
            "expires_at": datetime.fromtimestamp(current_user["exp"]).isoformat()
        }
    }

# ===============================================================================
# TENSOR OPERATIONS
# ===============================================================================

@app.post("/api/v1/tensors/create")
async def create_tensor(
    tensor_req: TensorCreate,
    current_user: Dict = Depends(get_current_user)
):
    """Crea un nuevo tensor fractal"""
    metrics["tensor_operations"] += 1
    
    try:
        if tensor_req.random:
            tensor = FractalTensor.random()
        else:
            tensor = FractalTensor(nivel_3=tensor_req.nivel_3 or [[0, 0, 0]])
        
        # Guardar en KB del usuario
        kb = get_user_kb(current_user["user_id"])
        tensor_key = f"tensor_{secrets.token_hex(8)}"
        
        # Almacenar
        tensor.metadata["created_by"] = current_user["user_id"]
        tensor.metadata["created_at"] = datetime.utcnow().isoformat()
        
        return {
            "success": True,
            "tensor_key": tensor_key,
            "tensor": {
                "nivel_3": tensor.nivel_3,
                "nivel_9": tensor.nivel_9 if hasattr(tensor, 'nivel_9') else None,
                "nivel_1": tensor.nivel_1 if hasattr(tensor, 'nivel_1') else None,
                "Ms": tensor.Ms if hasattr(tensor, 'Ms') else None,
                "Ss": tensor.Ss if hasattr(tensor, 'Ss') else None,
                "metadata": tensor.metadata
            }
        }
    except Exception as e:
        logger.error(f"Error creating tensor: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/tensors/synthesize")
async def synthesize_tensors(
    synthesis_req: TensorSynthesis,
    current_user: Dict = Depends(get_current_user)
):
    """Sintetiza dos tensores usando Trigate"""
    metrics["tensor_operations"] += 1
    
    try:
        # Crear tensores de ejemplo (en producción, recuperar de KB)
        tensor_a = FractalTensor.random()
        tensor_b = FractalTensor.random()
        
        # Usar Trigate para síntesis
        trigate = Trigate()
        M, S = trigate.synthesize(
            tensor_a.nivel_3[0] if tensor_a.nivel_3 else [0, 0, 0],
            tensor_b.nivel_3[0] if tensor_b.nivel_3 else [0, 0, 0]
        )
        
        # Crear tensor resultante
        result_tensor = FractalTensor(nivel_3=[M])
        result_tensor.Ms = M
        result_tensor.Ss = S
        
        return {
            "success": True,
            "result": {
                "M": M,
                "S": S,
                "tensor": {
                    "nivel_3": result_tensor.nivel_3,
                    "Ms": result_tensor.Ms,
                    "Ss": result_tensor.Ss
                }
            }
        }
    except Exception as e:
        logger.error(f"Error in synthesis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ===============================================================================
# KNOWLEDGE BASE OPERATIONS
# ===============================================================================

@app.post("/api/v1/kb/store")
async def store_archetype(
    archetype_name: str,
    tensor_data: Dict[str, Any],
    space_id: str = "default",
    current_user: Dict = Depends(get_current_user)
):
    """Almacena un arquetipo en la Knowledge Base"""
    metrics["kb_queries"] += 1
    
    try:
        kb = get_user_kb(current_user["user_id"])
        
        # Crear tensor desde data
        tensor = FractalTensor(nivel_3=tensor_data.get("nivel_3", [[0, 0, 0]]))
        if "Ms" in tensor_data:
            tensor.Ms = tensor_data["Ms"]
        if "Ss" in tensor_data:
            tensor.Ss = tensor_data["Ss"]
        
        # Almacenar
        kb.add_archetype(
            space_id=space_id,
            name=archetype_name,
            archetype_tensor=tensor,
            Ss=tensor.Ss if hasattr(tensor, 'Ss') and tensor.Ss else [0, 0, 0]
        )
        
        logger.info(f"Stored archetype '{archetype_name}' for user {current_user['user_id']}")
        
        return {
            "success": True,
            "message": f"Archetype '{archetype_name}' stored successfully",
            "space_id": space_id
        }
    except Exception as e:
        logger.error(f"Error storing archetype: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/kb/query")
async def query_archetype(
    query: TensorQuery,
    current_user: Dict = Depends(get_current_user)
):
    """Consulta arquetipos en la Knowledge Base"""
    metrics["kb_queries"] += 1
    
    try:
        kb = get_user_kb(current_user["user_id"])
        
        if query.archetype_name:
            archetype = kb.get_archetype(query.space_id, query.archetype_name)
            if not archetype:
                return {
                    "success": False,
                    "message": f"Archetype '{query.archetype_name}' not found"
                }
            
            return {
                "success": True,
                "archetype": {
                    "name": query.archetype_name,
                    "tensor": {
                        "nivel_3": archetype.nivel_3,
                        "Ms": archetype.Ms if hasattr(archetype, 'Ms') else None,
                        "Ss": archetype.Ss if hasattr(archetype, 'Ss') else None
                    }
                }
            }
        
        elif query.Ms_query:
            archetype = kb.get_archetype_by_ms(query.space_id, query.Ms_query)
            if not archetype:
                return {
                    "success": False,
                    "message": "No archetype found for given Ms"
                }
            
            return {
                "success": True,
                "archetype": {
                    "tensor": {
                        "nivel_3": archetype.nivel_3,
                        "Ms": archetype.Ms if hasattr(archetype, 'Ms') else None,
                        "Ss": archetype.Ss if hasattr(archetype, 'Ss') else None
                    }
                }
            }
        
        return {
            "success": False,
            "message": "Must provide either archetype_name or Ms_query"
        }
        
    except Exception as e:
        logger.error(f"Error querying KB: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ===============================================================================
# AURORA IE OPERATIONS
# ===============================================================================

@app.post("/api/v1/aurora/extend")
async def extend_fractal(
    extend_req: ExtendQuery,
    current_user: Dict = Depends(get_current_user)
):
    """Extiende un tensor usando Extender (reconstrucción fractal)"""
    metrics["tensor_operations"] += 1
    
    try:
        kb = get_user_kb(current_user["user_id"])
        extender = Extender(knowledge_base=kb)
        
        context = {"space_id": extend_req.space_id}
        
        if extend_req.use_recursive:
            result = extender.extend_fractal_recursive(extend_req.ss_query, context)
        else:
            result = extender.extend_fractal(extend_req.ss_query, context)
        
        return {
            "success": True,
            "result": {
                "method": result.get("reconstruction_method", "unknown"),
                "tensor": {
                    "nivel_3": result["reconstructed_tensor"].nivel_3,
                    "Ms": result["reconstructed_tensor"].Ms if hasattr(result["reconstructed_tensor"], 'Ms') else None,
                    "Ss": result["reconstructed_tensor"].Ss if hasattr(result["reconstructed_tensor"], 'Ss') else None
                },
                "log": result.get("log", []),
                "coherence": result.get("coherence"),
                "converged": result.get("converged")
            }
        }
    except Exception as e:
        logger.error(f"Error in extend operation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/aurora/pattern0")
async def create_pattern0_cluster(
    space_id: str = "default",
    num_tensors: int = 3,
    current_user: Dict = Depends(get_current_user)
):
    """Crea un cluster fractal usando Pattern 0 (ético)"""
    metrics["tensor_operations"] += 1
    
    try:
        tensors = pattern0_create_fractal_cluster(
            space_id=space_id,
            num_tensors=num_tensors
        )
        
        return {
            "success": True,
            "cluster": [
                {
                    "nivel_3": t.nivel_3,
                    "metadata": t.metadata
                }
                for t in tensors
            ],
            "message": f"Created ethical cluster with {len(tensors)} tensors"
        }
    except Exception as e:
        logger.error(f"Error creating Pattern 0 cluster: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ===============================================================================
# COLLABORATIVE OPERATIONS (P2P)
# ===============================================================================

@app.post("/api/v1/collab/task")
async def create_collaborative_task(
    task: CollaborativeTask,
    current_user: Dict = Depends(get_current_user)
):
    """
    Crea una tarea colaborativa entre peers.
    Esto se coordinará con el Discovery Server para contactar peers.
    """
    # TODO: Integrar con Discovery Server para enviar task a peers
    
    return {
        "success": True,
        "task_id": secrets.token_hex(8),
        "status": "pending",
        "message": "Collaborative task created. Waiting for peers to join.",
        "peers": task.peer_ids
    }

# ===============================================================================
# ADAPTIVE ECONOMICS & GOVERNANCE
# ===============================================================================

@app.post("/api/v1/governance/register_model")
async def register_user_model(current_user: Dict = Depends(get_current_user)):
    """
    Registra un modelo de IA para el usuario autenticado.
    Este modelo aprenderá de las interacciones del usuario y votará sobre políticas.
    
    🔑 CLAVE: Los usuarios entrenan modelos → los modelos votan → consenso emergente.
    """
    user_id = current_user["user_id"]
    peer_id = current_user["peer_id"]
    
    # Verificar si ya tiene modelo
    if user_id in user_models:
        return {
            "success": True,
            "model_id": user_models[user_id],
            "message": "Model already registered",
            "status": "existing"
        }
    
    # Registrar modelo nuevo
    model_id = economics_coordinator.registrar_modelo_usuario(peer_id)
    user_models[user_id] = model_id
    
    logger.info(f"🧠 User {user_id} registered model {model_id}")
    
    return {
        "success": True,
        "model_id": model_id,
        "message": "Model registered successfully. Start training it with interactions!",
        "status": "new"
    }

@app.post("/api/v1/governance/train")
async def train_user_model(
    request: TrainModelRequest,
    current_user: Dict = Depends(get_current_user)
):
    """
    Entrena el modelo del usuario con una interacción.
    El modelo aprende y puede proponer ajustes automáticos a políticas.
    
    Ejemplo de interacción:
    {
        "tipo": "mentoria",
        "calidad": 0.9,
        "duracion_horas": 8
    }
    """
    user_id = current_user["user_id"]
    
    # Verificar que tenga modelo
    if user_id not in user_models:
        raise HTTPException(status_code=400, detail="User must register model first")
    
    model_id = user_models[user_id]
    
    # Entrenar modelo
    economics_coordinator.entrenar_modelo_con_interaccion(model_id, request.interaccion)
    
    logger.info(f"🎓 Model {model_id} trained with interaction: {request.interaccion.get('tipo', 'unknown')}")
    
    return {
        "success": True,
        "model_id": model_id,
        "interaccion": request.interaccion,
        "message": "Model trained successfully. It may propose policy adjustments automatically."
    }

@app.post("/api/v1/governance/vote")
async def vote_on_policy(
    request: VotePolicyRequest,
    current_user: Dict = Depends(get_current_user)
):
    """
    El usuario hace que su modelo vote sobre una política económica.
    
    Políticas disponibles:
    - tasa_emision_base: % de emisión anual de MERIT/MIND
    - tasa_quema_fees: % de fees que se destruyen
    - umbral_minimo_nodos: Cuántos nodos mínimo para red saludable
    - umbral_latencia_ms: Latencia máxima aceptable
    - multiplicador_pattern0: Cuánto valen operaciones éticas
    - multiplicador_colaborativo: Bonus por colaboración
    """
    user_id = current_user["user_id"]
    
    # Verificar que tenga modelo
    if user_id not in user_models:
        raise HTTPException(status_code=400, detail="User must register model first")
    
    model_id = user_models[user_id]
    
    # Votar
    economics_coordinator.votar_politica(model_id, request.politica, request.valor_propuesto)
    
    # Obtener valor consensuado actual
    valor_actual = economics_coordinator.governance.obtener_politica_actual(request.politica)
    
    logger.info(f"🗳️  Model {model_id} voted: {request.politica} = {request.valor_propuesto}")
    
    return {
        "success": True,
        "politica": request.politica,
        "valor_votado": request.valor_propuesto,
        "valor_consensuado_actual": valor_actual,
        "message": "Vote registered. Consensus updated."
    }

@app.get("/api/v1/governance/policies/current")
async def get_current_policies(current_user: Dict = Depends(get_current_user)):
    """
    Obtiene las políticas económicas actuales (consensuadas por modelos).
    
    🔑 IMPORTANTE: Estos valores NO están hardcoded.
    Son el consenso emergente de todos los modelos entrenados por usuarios.
    """
    metricas = economics_coordinator.obtener_metricas()
    
    return {
        "success": True,
        "politicas": metricas["politicas_actuales"],
        "gobernanza": metricas["gobernanza"],
        "timestamp": datetime.utcnow().isoformat(),
        "message": "These values are learned, not hardcoded. They evolve with user models."
    }

@app.get("/api/v1/governance/policies/{nombre}/history")
async def get_policy_history(
    nombre: str,
    current_user: Dict = Depends(get_current_user)
):
    """
    Obtiene el histórico de evolución de una política.
    Permite ver cómo ha cambiado con el tiempo según los votos de modelos.
    """
    historico = economics_coordinator.obtener_evolucion_politica(nombre)
    
    if not historico:
        raise HTTPException(status_code=404, detail=f"Policy '{nombre}' not found")
    
    # Formatear histórico
    historico_formateado = [
        {"timestamp": ts.isoformat(), "valor": valor}
        for ts, valor in historico
    ]
    
    return {
        "success": True,
        "politica": nombre,
        "historico": historico_formateado,
        "valor_actual": historico[-1][1] if historico else 0,
        "num_cambios": len(historico)
    }

@app.post("/api/v1/governance/network/process_block")
async def process_network_block(
    report: NetworkStateReport,
    current_user: Dict = Depends(get_current_user)
):
    """
    Procesa un bloque de red con el estado actual.
    Usa políticas aprendidas (no hardcoded) para calcular emisiones/quemas.
    
    🔑 Este endpoint es para validadores/coordinadores de la red.
    """
    # Crear estado de red
    estado = NetworkState(
        timestamp=datetime.utcnow(),
        nodos_activos=report.nodos_activos,
        latencia_promedio_ms=report.latencia_promedio_ms,
        operaciones_por_hora=report.operaciones_por_hora,
        coherencia_promedio=report.coherencia_promedio,
        supply_merit=economics_coordinator.supplies["MERIT"],
        supply_mind=economics_coordinator.supplies["MIND"],
        supply_trust=economics_coordinator.supplies["TRUST"],
        fees_acumuladas=report.fees_acumuladas
    )
    
    # Procesar bloque con políticas aprendidas
    resultado = economics_coordinator.procesar_bloque(estado)
    
    logger.info(f"🔗 Block processed: MERIT +{resultado['emisiones']['MERIT']:.2f} -{resultado['quemas']['MERIT']:.2f}")
    
    return {
        "success": True,
        "resultado": {
            "timestamp": resultado["timestamp"].isoformat(),
            "emisiones": resultado["emisiones"],
            "quemas": resultado["quemas"],
            "supplies": resultado["supplies_actualizados"],
            "politicas_aplicadas": resultado["politicas_aplicadas"]
        },
        "message": "Block processed with learned policies (not hardcoded)"
    }

@app.post("/api/v1/governance/rewards/compute")
async def reward_compute_operation(
    request: ComputeRewardRequest,
    current_user: Dict = Depends(get_current_user)
):
    """
    Emite recompensa MIND por ejecutar una operación de cómputo.
    La cantidad se determina por políticas aprendidas (no hardcoded).
    """
    user_id = current_user["user_id"]
    
    # Calcular recompensa
    recompensa = economics_coordinator.emitir_recompensa_computo(
        tipo_operacion=request.tipo_operacion,
        complejidad=request.complejidad,
        coherencia=request.coherencia,
        es_colaborativa=request.es_colaborativa
    )
    
    logger.info(f"○ User {user_id} earned {recompensa:.2f} MIND for {request.tipo_operacion}")
    
    return {
        "success": True,
        "recompensa_mind": recompensa,
        "tipo_operacion": request.tipo_operacion,
        "complejidad": request.complejidad,
        "coherencia": request.coherencia,
        "es_colaborativa": request.es_colaborativa,
        "message": f"Earned {recompensa:.2f} ○ MIND"
    }

@app.post("/api/v1/governance/rewards/trust")
async def validate_trust_interaction(
    request: TrustInteractionRequest,
    current_user: Dict = Depends(get_current_user)
):
    """
    Valida una interacción humana y emite TRUST si cumple criterios éticos.
    
    TRUST solo se crea por:
    - Mentorías completadas
    - Colaboraciones multi-peer
    - Resolución de conflictos
    - Validación ética comunitaria
    
    Requiere firmas de ambos participantes y validación por Armonizador.
    """
    user_id = current_user["user_id"]
    peer_a = current_user["peer_id"]
    
    # Validar y emitir TRUST
    valida, cantidad = economics_coordinator.emitir_trust(
        tipo=request.tipo,
        peer_a=peer_a,
        peer_b=request.peer_b,
        firma_a=request.firma_a,
        firma_b=request.firma_b,
        metadata=request.metadata
    )
    
    if not valida:
        raise HTTPException(
            status_code=400,
            detail="Trust interaction rejected. Insufficient coherence or invalid signatures."
        )
    
    logger.info(f"U {peer_a} <-> {request.peer_b} earned {cantidad:.2f} TRUST for {request.tipo}")
    
    return {
        "success": True,
        "valida": valida,
        "recompensa_trust": cantidad,
        "tipo": request.tipo,
        "peer_a": peer_a,
        "peer_b": request.peer_b,
        "message": f"Earned {cantidad:.2f} U TRUST"
    }

@app.get("/api/v1/governance/supplies")
async def get_token_supplies(current_user: Dict = Depends(get_current_user)):
    """
    Obtiene los supplies actuales de los 3 tokens de Aurora.
    """
    return {
        "success": True,
        "supplies": economics_coordinator.supplies,
        "configs": {
            "MERIT": {
                "symbol": MERIT_CONFIG.symbol,
                "supply_inicial": MERIT_CONFIG.supply_inicial
            },
            "MIND": {
                "symbol": MIND_CONFIG.symbol,
                "supply_inicial": MIND_CONFIG.supply_inicial
            },
            "TRUST": {
                "symbol": TRUST_CONFIG.symbol,
                "supply_inicial": TRUST_CONFIG.supply_inicial,
                "rewards": TRUST_REWARDS
            }
        },
        "timestamp": datetime.utcnow().isoformat()
    }

# ===============================================================================
# METRICS & HEALTH
# ===============================================================================

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

@app.get("/api/v1/metrics")
async def get_metrics(current_user: Dict = Depends(get_current_user)):
    """Obtiene métricas del sistema (incluye gobernanza económica)"""
    econ_metrics = economics_coordinator.obtener_metricas()
    
    return {
        "success": True,
        "metrics": {
            **metrics,
            "timestamp": datetime.utcnow().isoformat(),
            "user_kbs": len(user_kbs),
            "user_models": len(user_models)
        },
        "economics": {
            "supplies": econ_metrics["supplies"],
            "gobernanza": econ_metrics["gobernanza"],
            "historial_bloques": econ_metrics["historial_bloques"]
        }
    }

# ===============================================================================
# STARTUP
# ===============================================================================

@app.on_event("startup")
async def startup_event():
    logger.info("🌟 Aurora IE API Gateway started!")
    logger.info(f"📡 Docs available at: /docs")
    logger.info(f"🔐 JWT Secret initialized")
    logger.info("🧠 Adaptive Economics Coordinator initialized")
    logger.info(f"💎 Token Supplies: MERIT={economics_coordinator.supplies['MERIT']:,.0f}, MIND={economics_coordinator.supplies['MIND']:,.0f}, TRUST={economics_coordinator.supplies['TRUST']:,.0f}")
    logger.info("🗳️  Governance system ready: Users can train models and vote on policies")
    logger.info("💡 Key: Policies are NOT hardcoded - they are learned by user models")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🐹 Aurora IE API Gateway shutting down...")

# ===============================================================================
# MAIN
# ===============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
