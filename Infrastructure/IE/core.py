
"""
NO FOR USE JUST FOR REFERENCE IT WILL BE IMPORTED AS A MODULE 

Aurora Trinity-3: Fractal, Ethical, Free Electronic Intelligence
===============================================================

A complete implementation of Aurora's ternary logic architecture featuring:
- Trigate operations with O(1) LUT-based inference, learning, and deduction
- Fractal Tensor structures with hierarchical 3-9-27 organization  
- Knowledge Base with multiverse logical space management
- Armonizador for coherence validation and harmonization
- Extender for fractal reconstruction and pattern extension
- Transcender for hierarchical synthesis operations

Author: Aurora Alliance
License: Apache-2.0 + CC-BY-4.0
Version: 1.0.0
"""
from __future__ import annotations

from typing import List, Dict, Any, Tuple, Optional, Union
import hashlib
import random
import itertools
import logging
import math


# ===============================================================================
# CONSTANTS AND UTILITIES
# ===============================================================================

class RecursiveNetworkConfig:
    """
    Configuración para la red recursiva de deducción Aurora.
    
    Aurora funciona como una red neuronal simbólica donde:
    - Cada nivel (1, 9, 3) valida coherencia con niveles superiores/inferiores
    - Los NULLs se propagan hacia arriba (forward) y se resuelven hacia abajo (backward)
    - La red converge iterativamente hacia un estado coherente
    """
    MAX_ITERATIONS = 10  # Máximo de ciclos de deducción recursiva
    COHERENCE_THRESHOLD = 0.95  # 95% de valores resueltos = convergencia
    NULL_TOLERANCE = True  # Aurora tolera NULLs parciales
    BIDIRECTIONAL_FLOW = True  # Forward (síntesis) + Backward (deducción)

PHI = 0.6180339887  # Golden ratio for Pattern 0 generation

class CoherenceError(Exception):
    """Raised for violations of the Absolute Coherence Principle."""
    pass

# Logger setup
logger = logging.getLogger("aurora.trinity")
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(levelname)s][%(name)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

# ===============================================================================
# TERNARY LOGIC FOUNDATION
# ===============================================================================

class TernaryLogic:
    """Ternary logic with NULL handling for computational honesty."""
    NULL = None

    @staticmethod
    def ternary_xor(a, b):
        """XOR with NULL propagation."""
        if a is TernaryLogic.NULL or b is TernaryLogic.NULL:
            return TernaryLogic.NULL
        return a ^ b

    @staticmethod
    def ternary_xnor(a, b):
        """XNOR with NULL propagation."""
        if a is TernaryLogic.NULL or b is TernaryLogic.NULL:
            return TernaryLogic.NULL
        return 1 - (a ^ b)

# ===============================================================================
# TRIGATE: FUNDAMENTAL LOGIC MODULE
# ===============================================================================

class Trigate:
    """
    Fundamental Aurora logic module implementing ternary operations.
    
    Supports three operational modes:
    1. Inference: A + B + M -> R (given inputs and control, compute result)
    2. Learning: A + B + R -> M (given inputs and result, learn control)
    3. Deduction: M + R + A -> B (given control, result, and one input, deduce other)
    
    All operations are O(1) using precomputed lookup tables (LUTs).
    """
    
    _LUT_INFER: Dict[Tuple, int] = {}
    _LUT_LEARN: Dict[Tuple, int] = {}
    _LUT_DEDUCE_A: Dict[Tuple, int] = {}
    _LUT_DEDUCE_B: Dict[Tuple, int] = {}
    _initialized = False
    
    def __init__(self):
        """Initialize Trigate and ensure LUTs are computed."""
        if not Trigate._initialized:
            Trigate._initialize_luts()
    
    @classmethod
    def _initialize_luts(cls):
        """Initialize all lookup tables for O(1) operations."""
        print("Initializing Trigate LUTs...")
        states = [0, 1, TernaryLogic.NULL]
        
        # Generate all 27 combinations for each operation
        for a in states:
            for b in states:
                for m in states:
                    # Inference: A + B + M -> R
                    if TernaryLogic.NULL in (a, b, m):
                        r = TernaryLogic.NULL
                    else:
                        r = a ^ b if m == 1 else 1 - (a ^ b)
                    cls._LUT_INFER[(a, b, m)] = r
                    
                for r in states:
                    # Learning: A + B + R -> M
                    if TernaryLogic.NULL in (a, b, r):
                        m = TernaryLogic.NULL
                    else:
                        m = 1 if (a ^ b) == r else 0
                    cls._LUT_LEARN[(a, b, r)] = m
                    
                    # Deduction A: M + R + B -> A
                    if TernaryLogic.NULL in (m, r, b):
                        a_result = TernaryLogic.NULL
                    else:
                        a_result = b ^ r if m == 1 else 1 - (b ^ r)
                    cls._LUT_DEDUCE_A[(m, r, b)] = a_result
                    
                    # Deduction B: M + R + A -> B
                    if TernaryLogic.NULL in (m, r, a):
                        b_result = TernaryLogic.NULL
                    else:
                        b_result = a ^ r if m == 1 else 1 - (a ^ r)
                    cls._LUT_DEDUCE_B[(m, r, a)] = b_result
        
        cls._initialized = True
        print(f"Trigate LUTs initialized: {len(cls._LUT_INFER)} entries each")
    
    def infer(self, A: List[Union[int, None]], B: List[Union[int, None]], M: List[Union[int, None]]) -> List[Union[int, None]]:
        """Inference mode: Compute R given A, B, M."""
        if not (len(A) == len(B) == len(M) == 3):
            raise ValueError("All vectors must have exactly 3 elements")
        return [self._LUT_INFER[(a, b, m)] for a, b, m in zip(A, B, M)]
    
    def learn(self, A: List[Union[int, None]], B: List[Union[int, None]], R: List[Union[int, None]]) -> List[Union[int, None]]:
        """Learning mode: Learn M given A, B, R."""
        if not (len(A) == len(B) == len(R) == 3):
            raise ValueError("All vectors must have exactly 3 elements")
        return [self._LUT_LEARN[(a, b, r)] for a, b, r in zip(A, B, R)]
    
    def deduce_a(self, M: List[Union[int, None]], R: List[Union[int, None]], B: List[Union[int, None]]) -> List[Union[int, None]]:
        """Deduction mode: Deduce A given M, R, B."""
        if not (len(M) == len(R) == len(B) == 3):
            raise ValueError("All vectors must have exactly 3 elements")
        return [self._LUT_DEDUCE_A[(m, r, b)] for m, r, b in zip(M, R, B)]
    
    def deduce_b(self, M: List[Union[int, None]], R: List[Union[int, None]], A: List[Union[int, None]]) -> List[Union[int, None]]:
        """Deduction mode: Deduce B given M, R, A."""
        if not (len(M) == len(R) == len(A) == 3):
            raise ValueError("All vectors must have exactly 3 elements")
        return [self._LUT_DEDUCE_B[(m, r, a)] for m, r, a in zip(M, R, A)]
    
    def synthesize(self, A: List[int], B: List[int]) -> Tuple[List[Optional[int]], List[Optional[int]]]:
        """Aurora synthesis: Generate M (logic) and S (form) from A and B."""
        M = [TernaryLogic.ternary_xor(a, b) for a, b in zip(A, B)]
        S = [TernaryLogic.ternary_xnor(a, b) for a, b in zip(A, B)]
        return M, S

    def recursive_synthesis(self, vectors: List[List[int]]) -> Tuple[List[Optional[int]], List[List[Optional[int]]]]:
        """Sequentially reduce a list of ternary vectors."""
        if len(vectors) < 2:
            raise ValueError("At least 2 vectors required")

        history: List[List[Optional[int]]] = []
        current = vectors[0]

        for nxt in vectors[1:]:
            current, _ = self.synthesize(current, nxt)
            history.append(current)

        return current, history

# ===============================================================================
# FRACTAL TENSOR ARCHITECTURE
# ===============================================================================

class FractalTensor:
    """
    Aurora's fundamental data structure with hierarchical 3-9-27 organization.
    Supports fractal scaling and semantic coherence validation.
    """
    
    def __init__(self, nivel_3=None, Ms=None, Ss=None, MetaM=None):
        """Initialize fractal tensor with 3-level hierarchy."""
        self.nivel_3 = nivel_3 or [[0, 0, 0]]  # Finest detail level
        self.metadata = {}
        
        # Auto-generate hierarchical levels
        self._generate_hierarchy()

        self.Ms = Ms if Ms is not None else (self.nivel_3[0] if self.nivel_3 else [0,0,0])
        self.Ss = Ss
        self.MetaM = MetaM
    
    def _generate_hierarchy(self):
        """
        Generate nivel_9 and nivel_1 from nivel_3.
        Tolera NULLs tratándolos como 0 para cálculos de resumen.
        """
        # Nivel 9: group 3 vectors from nivel_3
        if len(self.nivel_3) >= 3:
            self.nivel_9 = [self.nivel_3[i:i+3] for i in range(0, len(self.nivel_3), 3)]
        else:
            self.nivel_9 = [self.nivel_3]
        
        # Nivel 1: summary vector from nivel_3[0]
        # Tolerante a NULLs: None se trata como 0
        if self.nivel_3:
            root = self.nivel_3[0]
            # Sumar solo valores no-NULL (None = 0)
            sum_val = sum(v if v is not None else 0 for v in root)
            self.nivel_1 = [sum_val % 8, len(self.nivel_3), hash(str(root)) % 8]
        else:
            self.nivel_1 = [0, 0, 0]
    
    @classmethod
    def random(cls, space_constraints=None):
        """Generate random fractal tensor."""
        nivel_3 = [[random.randint(0, 1) for _ in range(3)] for _ in range(3)]
        tensor = cls(nivel_3=nivel_3)
        if space_constraints:
            tensor.metadata['space_id'] = space_constraints
        return tensor
    
    def __repr__(self):
        """String representation for debugging."""
        return f"FT(root={self.nivel_3[:3]}, mid={self.nivel_9[0] if self.nivel_9 else '...'}, detail={self.nivel_1})"

# ===============================================================================
# KNOWLEDGE BASE SYSTEM
# ===============================================================================

class _SingleUniverseKB:
    """Knowledge base for a single logical space."""
    
    def __init__(self):
        self.storage = {}
        self.name_index = {}
        self.ss_index = {}
        self.ms_index = {}
    
    def add_archetype(self, archetype_tensor: FractalTensor, Ss: list, name: Optional[str] = None, **kwargs) -> bool:
        """Add archetype to this universe, validating coherence."""
        if not hasattr(archetype_tensor, 'Ms') or not hasattr(archetype_tensor, 'MetaM'):
             raise ValueError("Archetype must have Ms and MetaM attributes for coherence validation.")

        # Principle of Absolute Coherence: Ms -> MetaM must be unique
        self._validate_coherence(archetype_tensor.Ms, archetype_tensor.MetaM)

        key = tuple(Ss)
        self.storage[key] = archetype_tensor
        self.ss_index[key] = archetype_tensor
        
        ms_key = tuple(archetype_tensor.Ms)
        self.ms_index[ms_key] = archetype_tensor

        if name:
            self.name_index[name] = archetype_tensor
        
        return True

    def _validate_coherence(self, Ms, MetaM):
        """Principio de Coherencia Absoluta: Ms → MetaM único"""
        existing = self.get_archetype_by_ms(Ms)
        if existing and hasattr(existing, 'MetaM') and existing.MetaM != MetaM:
            raise CoherenceError(f"Coherence violation: MetaM distinct for Ms {Ms}. Existing: {existing.MetaM}, New: {MetaM}")
        return True

    def get_archetype_by_ms(self, Ms_query: List[int]) -> Optional[FractalTensor]:
        """Find archetype by Ms vector."""
        key = tuple(Ms_query)
        return self.ms_index.get(key)
    
    def find_archetype_by_name(self, name: str) -> Optional[FractalTensor]:
        """Find archetype by name."""
        return self.name_index.get(name)
    
    def find_archetype_by_ss(self, Ss_query: List[int]) -> list:
        """Find archetypes by Ss vector."""
        key = tuple(Ss_query)
        result = self.ss_index.get(key)
        return [result] if result else []

class FractalKnowledgeBase:
    """Multi-universe knowledge base manager."""
    
    def __init__(self):
        self.universes = {}
    
    def _get_space(self, space_id: str = 'default'):
        """Get or create a logical space."""
        if space_id not in self.universes:
            self.universes[space_id] = _SingleUniverseKB()
        return self.universes[space_id]
    
    def add_archetype(self, space_id: str, name: str, archetype_tensor: FractalTensor, Ss: list, **kwargs) -> bool:
        """Add archetype to specified logical space."""
        return self._get_space(space_id).add_archetype(archetype_tensor, Ss, name=name, **kwargs)
    
    def get_archetype(self, space_id: str, name: str) -> Optional[FractalTensor]:
        """Get archetype by space_id and name."""
        return self._get_space(space_id).find_archetype_by_name(name)

    def get_archetype_by_ms(self, space_id: str, Ms_query: List[int]) -> Optional[FractalTensor]:
        """Find archetype by Ms in a specific space."""
        return self._get_space(space_id).get_archetype_by_ms(Ms_query)

# ===============================================================================
# PROCESSING MODULES
# ===============================================================================

class Transcender:
    """
    Componente de síntesis que implementa la síntesis jerárquica
    de Tensores Fractales completos.
    """
    
    def __init__(self, fractal_vector: Optional[List[int]] = None):
        self.trigate = Trigate()
        self.seed_vector = fractal_vector
    
    def relate_vectors(self, A: list, B: list, context: dict = None) -> list:
        """
        Calcula un vector de relación Aurora-native entre A y B, incorporando ventana de contexto y relaciones cruzadas si se proveen.
        """
        if len(A) != len(B):
            return [0, 0, 0]
        diff_vector = []
        for i in range(len(A)):
            a_val = A[i] if A[i] is not None else 0
            b_val = B[i] if B[i] is not None else 0
            diff = b_val - a_val
            # Normalize to ternary: 1 if diff > 0, 0 if diff == 0, None if diff < 0
            if diff > 0:
                diff_vector.append(1)
            elif diff == 0:
                diff_vector.append(0)
            else:
                diff_vector.append(None)
        
        # Aurora-native: ventana de contexto y relaciones cruzadas
        if context and 'prev' in context and 'next' in context:
            v_prev = context['prev']
            v_next = context['next']
            rel_cross = []
            for vp, vn in zip(v_prev, v_next):
                vp_val = vp if vp is not None else 0
                vn_val = vn if vn is not None else 0
                diff_cross = vp_val - vn_val
                if diff_cross > 0:
                    rel_cross.append(1)
                elif diff_cross == 0:
                    rel_cross.append(0)
                else:
                    rel_cross.append(None)
            # Concatenar: [diff_vector, rel_cross, A, B]
            return list(diff_vector) + list(rel_cross) + list(A) + list(B)
        return diff_vector

    def compute_vector_trio(self, A: List[int], B: List[int], C: List[int]) -> Dict[str, Any]:
        """Procesa un trío de vectores simples (operación base)."""
        M_AB, _ = self.trigate.synthesize(A, B)
        M_BC, _ = self.trigate.synthesize(B, C)
        M_CA, _ = self.trigate.synthesize(C, A)
        M_emergent, _ = self.trigate.synthesize(M_AB, M_BC)
        M_intermediate, _ = self.trigate.synthesize(M_emergent, M_CA)
        MetaM = [TernaryLogic.ternary_xor(a, b) for a, b in zip(M_intermediate, M_emergent)]
        return {'M_emergent': M_emergent, 'MetaM': MetaM, 'Ms': M_emergent, 'Ss': MetaM}

    def deep_learning(
        self,
        A: List[int],
        B: List[int],
        C: List[int],
        M_emergent: Optional[List[int]] = None
    ) -> Dict[str, Any]:
        """
        Calcula M_emergent y MetaM tal como exige el modelo Trinity-3.
        Genera R_hipotesis = Trigate.infer(A, B, M_emergent).
        """
        trio = self.compute_vector_trio(A, B, C)

        # Si el caller no aporta M_emergent, usa el calculado.
        if M_emergent is None:
            M_emergent = trio["M_emergent"]

        R_hipotesis = self.trigate.infer(A, B, M_emergent)

        return {
            "M_emergent": M_emergent,
            "MetaM": trio["MetaM"],
            "R_hipotesis": R_hipotesis,
        }

    def compute_full_fractal(self, A: 'FractalTensor', B: 'FractalTensor', C: 'FractalTensor', kb: 'FractalKnowledgeBase' = None, space_id: str = "default") -> 'FractalTensor':
        """
        Sintetiza tres tensores fractales en uno, de manera jerárquica y elegante.
        Prioriza una raíz de entrada válida por encima de la síntesis.
        """
        from copy import deepcopy
        
        # Create output tensor with basic structure
        out = FractalTensor(nivel_3=[[0, 0, 0]])
        
        # Ensure all tensors have proper structure
        if not hasattr(A, 'nivel_3') or not A.nivel_3:
            A.nivel_3 = [[0, 0, 0]]
        if not hasattr(B, 'nivel_3') or not B.nivel_3:
            B.nivel_3 = [[0, 0, 0]]
        if not hasattr(C, 'nivel_3') or not C.nivel_3:
            C.nivel_3 = [[0, 0, 0]]

        def synthesize_trio(vectors: list) -> list:
            # Only use first 3 elements of each vector
            while len(vectors) < 3:
                vectors.append([0, 0, 0])
            trimmed = [v[:3] if isinstance(v, (list, tuple)) else [0,0,0] for v in vectors[:3]]
            r = self.compute_vector_trio(*trimmed)
            m_emergent = r.get('M_emergent', [0, 0, 0])
            return [bit if bit is not None else 0 for bit in m_emergent[:3]]

        # Extract vectors for synthesis
        A_vec = A.nivel_3[0] if A.nivel_3 else [0, 0, 0]
        B_vec = B.nivel_3[0] if B.nivel_3 else [0, 0, 0]
        C_vec = C.nivel_3[0] if C.nivel_3 else [0, 0, 0]
        
        # Compute emergent properties
        result = self.compute_vector_trio(A_vec, B_vec, C_vec)
        
        # Set output tensor properties
        out.nivel_3 = [result["M_emergent"]]
        out.Ms = result["M_emergent"]
        out.Ss = result.get("Ss", result["MetaM"])
        out.MetaM = result["MetaM"]
        
        # ✅ NUEVO: Conectar con Evolver y KB
        if kb:
            evolver = Evolver()
            archetype = evolver.compute_fractal_archetype([A, B, C])
            
            # Ensure archetype has MetaM for validation
            if not hasattr(archetype, 'MetaM') or archetype.MetaM is None:
                archetype.MetaM = out.MetaM

            try:
                # The KB's add_archetype now handles coherence validation
                kb.add_archetype(
                    space_id, 
                    f"archetype_{hash(str(archetype.Ms))}", 
                    archetype, 
                    archetype.Ss if hasattr(archetype, 'Ss') and archetype.Ss is not None else archetype.Ms
                )
                logger.info(f"Archetype {archetype.Ms} stored in KB.")
            except CoherenceError as e:
                logger.warning(f"Cognitive Cycle: {e}")
            except Exception as e:
                logger.error(f"Cognitive Cycle: Failed to store archetype in KB: {e}")

        return out

class Evolver:
    """
    Motor de visión fractal unificada para Arquetipos, Dinámicas y Relatores.
    """
    
    def __init__(self):
        self.base_transcender = Transcender()

    def _perform_full_tensor_synthesis(self, tensors: List[FractalTensor]) -> FractalTensor:
        """
        Motor de síntesis fractal: reduce una lista de tensores a uno solo.
        """
        if not tensors:
            return FractalTensor(nivel_3=[[0, 0, 0]])
        
        current_level_tensors = list(tensors)
        while len(current_level_tensors) > 1:
            next_level_tensors = []
            for i in range(0, len(current_level_tensors), 3):
                trio = current_level_tensors[i:i+3]
                while len(trio) < 3:
                    trio.append(FractalTensor(nivel_3=[[0, 0, 0]]))
                synthesized_tensor = self.base_transcender.compute_full_fractal(*trio)
                next_level_tensors.append(synthesized_tensor)
            current_level_tensors = next_level_tensors
            
        return current_level_tensors[0]

    def compute_fractal_archetype(self, tensor_family: List[FractalTensor]) -> FractalTensor:
        """Perspectiva de ARQUETIPO: Destila la esencia de una familia de conceptos."""
        if len(tensor_family) < 2:
            import warnings
            warnings.warn("Se requieren al menos 2 tensores para computar un arquetipo.")
            return FractalTensor(nivel_3=[[0, 0, 0]]) if not tensor_family else tensor_family[0]
        return self._perform_full_tensor_synthesis(tensor_family)

class RecursiveDeductionNetwork:
    """
    Red recursiva de deducción: resuelve NULLs propagando coherencia
    entre niveles fractales (1 ↔ 9 ↔ 3).
    
    Arquitectura:
    1. FORWARD PASS: Propaga datos incompletos hacia arriba (síntesis)
    2. COHERENCE CHECK: Valida consistencia entre niveles
    3. BACKWARD PASS: Resuelve NULLs usando contexto superior (deducción)
    4. ITERATE: Repite hasta convergencia o max_iterations
    """
    
    def __init__(self, kb: FractalKnowledgeBase, config: RecursiveNetworkConfig = None):
        self.kb = kb
        self.config = config or RecursiveNetworkConfig()
        self.transcender = Transcender()
        self.trigate = Trigate()
        self.armonizador = Armonizador(knowledge_base=kb)
        
    def _count_nulls(self, tensor: FractalTensor) -> Tuple[int, int]:
        """Cuenta NULLs en todos los niveles del tensor."""
        total_elements = 0
        null_count = 0
        
        for vec in tensor.nivel_3:
            for val in vec:
                total_elements += 1
                if val is None:
                    null_count += 1
        
        return null_count, total_elements
    
    def _coherence_score(self, tensor: FractalTensor) -> float:
        """
        Calcula coherencia entre niveles:
        - nivel_3 (detalle) vs nivel_9 (síntesis) vs nivel_1 (resumen)
        """
        null_count, total = self._count_nulls(tensor)
        
        # Score base: proporción de valores resueltos
        resolution_score = (total - null_count) / total if total > 0 else 0.0
        
        # Penalización por inconsistencia entre niveles
        if hasattr(tensor, 'nivel_1') and tensor.nivel_1 and tensor.nivel_3:
            expected_sum = tensor.nivel_1[0]
            actual_sum = sum(v if v is not None else 0 for v in tensor.nivel_3[0]) % 8
            level_consistency = 1.0 if expected_sum == actual_sum else 0.8
        else:
            level_consistency = 1.0
        
        return resolution_score * level_consistency
    
    def forward_propagate(self, tensor: FractalTensor) -> FractalTensor:
        """
        FORWARD PASS: Propaga datos incompletos hacia arriba.
        Los NULLs se mantienen, la síntesis trabaja con valores conocidos.
        """
        logger.info(f"Forward pass: propagating {tensor.nivel_3[0]} upward")
        
        # Regenerar jerarquía respetando NULLs
        tensor._generate_hierarchy()
        
        return tensor
    
    def backward_deduce(self, tensor: FractalTensor, space_id: str) -> FractalTensor:
        """
        BACKWARD PASS: Resuelve NULLs usando arquetipos y contexto superior.
        """
        logger.info(f"Backward pass: deducing NULLs in {tensor.nivel_3[0]}")
        
        root = tensor.nivel_3[0] if tensor.nivel_3 else [None, None, None]
        
        # 1. Buscar arquetipo similar en KB
        archetype = None
        universe = self.kb._get_space(space_id)
        
        # Buscar arquetipos con patrón similar (NULLs como wildcards)
        for key, candidate in universe.storage.items():
            if not hasattr(candidate, 'nivel_3') or not candidate.nivel_3:
                continue
            
            candidate_root = candidate.nivel_3[0]
            match = True
            
            # Match donde no haya NULL en query
            for i, val in enumerate(root):
                if val is not None and i < len(candidate_root):
                    if candidate_root[i] != val:
                        match = False
                        break
            
            if match:
                archetype = candidate
                break
        
        # 2. Rellenar NULLs usando arquetipo
        if archetype:
            archetype_root = archetype.nivel_3[0]
            deduced_root = []
            
            for i in range(3):
                if i < len(root) and root[i] is not None:
                    deduced_root.append(root[i])
                elif i < len(archetype_root):
                    logger.debug(f"Deduced position {i}: NULL -> {archetype_root[i]} (from archetype)")
                    deduced_root.append(archetype_root[i])
                else:
                    deduced_root.append(0)  # Fallback
            
            tensor.nivel_3[0] = deduced_root
        
        # 3. Armonizar para garantizar coherencia
        harmonized = self.armonizador.harmonize(
            tensor.nivel_3[0], 
            archetype=archetype,
            space_id=space_id
        )
        tensor.nivel_3[0] = harmonized["output"]
        
        return tensor
    
    def recursive_solve(
        self, 
        incomplete_tensor: FractalTensor, 
        space_id: str = "default"
    ) -> Dict[str, Any]:
        """
        Orquestador principal: resuelve tensor incompleto mediante
        propagación recursiva bidireccional.
        
        Returns:
            {
                'resolved_tensor': FractalTensor,
                'iterations': int,
                'final_coherence': float,
                'converged': bool,
                'trace': List[str]
            }
        """
        trace = [f"Starting recursive deduction in space '{space_id}'"]
        tensor = incomplete_tensor
        
        for iteration in range(self.config.MAX_ITERATIONS):
            # 1. Forward: propagar hacia arriba
            tensor = self.forward_propagate(tensor)
            
            # 2. Medir coherencia
            coherence = self._coherence_score(tensor)
            trace.append(f"Iteration {iteration+1}: coherence={coherence:.2f}")
            
            # 3. Check convergencia
            if coherence >= self.config.COHERENCE_THRESHOLD:
                trace.append(f"✅ Converged at iteration {iteration+1}")
                return {
                    'resolved_tensor': tensor,
                    'iterations': iteration + 1,
                    'final_coherence': coherence,
                    'converged': True,
                    'trace': trace
                }
            
            # 4. Backward: deducir NULLs
            tensor = self.backward_deduce(tensor, space_id)
        
        # No convergió en MAX_ITERATIONS
        final_coherence = self._coherence_score(tensor)
        trace.append(f"⚠️ Max iterations reached. Final coherence={final_coherence:.2f}")
        
        return {
            'resolved_tensor': tensor,
            'iterations': self.config.MAX_ITERATIONS,
            'final_coherence': final_coherence,
            'converged': False,
            'trace': trace
        }


class Extender:
    """
    Orquestador Aurora refactorizado con expertos como métodos internos para
    simplificar el alcance y la gestión de estado.

    Opera como de forma inversa a Evolver, extendiendo el conocimiento fractal
    a partir de consultas simples y contexto, utilizando expertos para validar, 
    utiliza trigate de form inversa al transcender.
    
    Ahora integra RecursiveDeductionNetwork para resolver NULLs iterativamente.
    """
    
    def __init__(self, knowledge_base: FractalKnowledgeBase):
        self.kb = knowledge_base
        self.transcender = Transcender()
        self._lut_tables = {}
        self.armonizador = Armonizador(knowledge_base=self.kb)
        self.recursive_network = RecursiveDeductionNetwork(kb=self.kb)

    def fractal_reconstruct(self, Ms, MetaM, space_id):
        """Reconstruye desde Ms + MetaM usando deducción inversa en cascada."""
        logger.info(f"Fractal reconstruction started for Ms={Ms} in space='{space_id}'")
        trigate = Trigate()

        # 1. Deducir M_intermediate desde Ms y MetaM
        M_intermediate = [TernaryLogic.ternary_xor(m, mm) for m, mm in zip(Ms, MetaM)]

        # 2. Deducir M_AB y M_BC desde M_intermediate (heurística: asumir simetría)
        # M_intermediate = M_AB ^ M_BC. Para deducir, necesitamos una base.
        # Usamos la LUT de deducción asumiendo que M_BC es el vector neutro [0,0,0]
        # y que la "regla" es 1 (XOR).
        M_AB = trigate.deduce_a(M=[1,1,1], R=M_intermediate, B=[0,0,0])
        M_BC = [0,0,0] # Base de la heurística

        # 3. Deducir A, B, C desde M_AB y M_BC
        # A, B from M_AB
        A = trigate.deduce_a(M=[1,1,1], R=M_AB, B=[0,0,0]) # Heurística: B base es [0,0,0]
        B = trigate.deduce_b(M=[1,1,1], R=M_AB, A=A)
        
        # B, C from M_BC
        C = trigate.deduce_b(M=[1,1,1], R=M_BC, A=B)

        # 4. Crear tensores reconstruidos
        # Por ahora, creamos tensores simples. Una implementación completa reconstruiría todos los niveles.
        tensor_A = FractalTensor(nivel_3=[A])
        tensor_B = FractalTensor(nivel_3=[B])
        tensor_C = FractalTensor(nivel_3=[C])

        logger.info("Fractal reconstruction complete.")
        return [tensor_A, tensor_B, tensor_C]

    def _validate_archetype(self, ss_query: list, space_id: str) -> Tuple[bool, Optional[FractalTensor]]:
        """Experto Arquetipo como método."""
        universe = self.kb._get_space(space_id)
        ss_key = tuple(int(x) if x in (0, 1) else 0 for x in ss_query[:3])
        logger.debug(f"Looking up archetype with ss_key={ss_key} in space={space_id}")
        
        # Buscar por Ss
        archi_ss = universe.find_archetype_by_ss(list(ss_key))
        if archi_ss:
            logger.debug(f"Found archetype by Ss: {archi_ss}")
            return True, archi_ss[0] if isinstance(archi_ss, list) else archi_ss
        
        # Fallback: buscar por nombre si hay algún patrón
        for name in universe.name_index.keys():
            if str(ss_key) in name:
                archetype = universe.find_archetype_by_name(name)
                if archetype:
                    logger.debug(f"Found archetype by name pattern: {archetype}")
                    return True, archetype
        
        logger.debug("No archetype found")
        return False, None

    def _project_dynamics(self, ss_query: list, space_id: str) -> Tuple[bool, Optional[FractalTensor]]:
        """Experto Dinámica como método."""
        universe = self.kb._get_space(space_id)
        best, best_sim = None, -1.0
        
        # Buscar en todos los arquetipos almacenados
        for key, archetype in universe.storage.items():
            if hasattr(archetype, 'nivel_3') and archetype.nivel_3:
                archetype_ss = archetype.nivel_3[0]
                sim = sum(1 for a, b in zip(archetype_ss, ss_query) if a == b) / len(ss_query)
                if sim > best_sim:
                    best_sim, best = sim, archetype
        
        if best and best_sim > 0.7:
            return True, best
        return False, None

    def _contextualize_relations(self, ss_query: list, space_id: str) -> Tuple[bool, Optional[FractalTensor]]:
        """Experto Relator como método."""
        universe = self.kb._get_space(space_id)
        if not universe.storage:
            logger.debug("No archetypes in universe")
            return False, None
        
        best, best_score = None, float('-inf')
        for key, archetype in universe.storage.items():
            if not hasattr(archetype, 'nivel_3') or not archetype.nivel_3:
                continue
            
            archetype_ss = archetype.nivel_3[0]
            rel = self.transcender.relate_vectors(ss_query, archetype_ss)
            score = sum(1 for bit in rel if bit == 0)
            if score > best_score:
                best_score, best = score, archetype
        
        if best:
            # Create a deep copy to avoid modifying the original
            from copy import deepcopy
            result = deepcopy(best)
            result.nivel_3[0] = list(ss_query[:3])  # Explicitly preserve root
            logger.debug(f"Contextualized with score={best_score}, root preserved={result.nivel_3[0]}")
            return True, result
        
        logger.debug("No relational match found")
        return False, None

    def lookup_lut(self, space_id: str, ss_query: list) -> Optional[FractalTensor]:
        """Lookup in LUT tables."""
        lut_key = f"{space_id}:{tuple(ss_query)}"
        return self._lut_tables.get(lut_key)

    def extend_fractal_recursive(self, input_ss, contexto: dict) -> dict:
        """
        Extensión Aurora con deducción recursiva de NULLs.
        
        Usa RecursiveDeductionNetwork para resolver tensores incompletos
        mediante propagación bidireccional entre niveles fractales.
        """
        space_id = contexto.get('space_id', 'default')
        
        # Crear tensor desde input
        if hasattr(input_ss, 'nivel_3'):
            tensor = input_ss
        else:
            # Normalizar query a vector ternario con NULLs
            ss_query = input_ss if isinstance(input_ss, (list, tuple)) else [0, 0, 0]
            tensor = FractalTensor(nivel_3=[list(ss_query)])
        
        # Resolver NULLs mediante red recursiva
        result = self.recursive_network.recursive_solve(tensor, space_id)
        
        return {
            'reconstructed_tensor': result['resolved_tensor'],
            'reconstruction_method': f"recursive_deduction (iter={result['iterations']})",
            'coherence': result['final_coherence'],
            'converged': result['converged'],
            'log': result['trace']
        }
    
    def extend_fractal(self, input_ss, contexto: dict) -> dict:
        """
        Orquestador Principal.
        
        Si el input tiene NULLs, usa deducción recursiva.
        Si no, usa el método estándar de arquetipos.
        """
        log = [f"Extensión Aurora: espacio '{contexto.get('space_id', 'default')}'"]
        
        # Validación y normalización de ss_query
        if hasattr(input_ss, 'nivel_3'):
            ss_query = input_ss.nivel_3[0] if input_ss.nivel_3 else [0, 0, 0]
        else:
            ss_query = input_ss
        
        # Detectar NULLs → usar red recursiva
        if isinstance(ss_query, (list, tuple)) and None in ss_query:
            null_count = sum(1 for x in ss_query if x is None)
            log.append(f"🔍 Detected {null_count} NULLs → using recursive deduction network")
            return self.extend_fractal_recursive(input_ss, contexto)
        
        # Normalizar a un vector ternario de longitud 3
        if not isinstance(ss_query, (list, tuple)):
            log.append("⚠️ Entrada inválida, usando vector neutro [0,0,0]")
            ss_query = [0, 0, 0]
        else:
            ss_query = [
                None if x is None else int(x) if x in (0, 1) else 0
                for x in list(ss_query)[:3]
            ] + [0] * (3 - len(ss_query))
        
        space_id = contexto.get('space_id', 'default')
        
        STEPS = [
            lambda q, s: (self.lookup_lut(s, q) is not None, self.lookup_lut(s, q)),
            self._validate_archetype,
            self._project_dynamics,
            self._contextualize_relations
        ]
        METHODS = [
            "reconstrucción por LUT",
            "reconstrucción por arquetipo (axioma)",
            "proyección por dinámica (raíz preservada)",
            "contextualización por relator (raíz preservada)"
        ]
        
        for step, method in zip(STEPS, METHODS):
            ok, tensor = step(ss_query, space_id)
            if ok and tensor is not None:
                log.append(f"✅ {method}.")
                
                # Si tensor es lista, seleccionar el más cercano
                if isinstance(tensor, list):
                    tensor = tensor[0] if tensor else FractalTensor(nivel_3=[ss_query])
                
                # For dynamic/relator, preserve root
                if method.startswith("proyección") or method.startswith("contextualización"):
                    from copy import deepcopy
                    result = deepcopy(tensor)
                    result.nivel_3[0] = ss_query
                    root_vector = result.nivel_3[0]
                    harm = self.armonizador.harmonize(root_vector, archetype=root_vector, space_id=space_id)
                    result.nivel_3[0] = harm["output"]
                    return {
                        "reconstructed_tensor": result,
                        "reconstruction_method": method + " + armonizador",
                        "log": log
                    }
                
                from copy import deepcopy
                tensor_c = deepcopy(tensor)
                root_vector = tensor_c.nivel_3[0] if tensor_c.nivel_3 else ss_query
                harm = self.armonizador.harmonize(root_vector, archetype=root_vector, space_id=space_id)
                tensor_c.nivel_3[0] = harm["output"]
                return {
                    "reconstructed_tensor": tensor_c,
                    "reconstruction_method": method + " + armonizador",
                    "log": log
                }
        
        # Fallback
        log.append("🤷 No se encontraron coincidencias. Devolviendo tensor neutro.")
        tensor_n = FractalTensor(nivel_3=[ss_query])
        root_vector = tensor_n.nivel_3[0]
        harm = self.armonizador.harmonize(root_vector, archetype=root_vector, space_id=space_id)
        tensor_n.nivel_3[0] = harm["output"]
        
        return {
            "reconstructed_tensor": tensor_n,
            "reconstruction_method": "fallback neutro + armonizador",
            "log": log
        }



logger = logging.getLogger("aurora.armonizador")
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(levelname)s][%(name)s][ambig=%(ambiguity)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

Vector = List[Optional[int]]


class AmbiguityScore(int):
    """Integer score representing ambiguity distance (lower is better)."""
    pass


class AdjustmentStep:
    """Base class for harmonization adjustment steps."""

    def apply(self, vec: Vector, archetype: Union['FractalTensor', Vector, None], kb=None) -> Vector:
        raise NotImplementedError


class MicroShift(AdjustmentStep):
    """Local, triadic-aware micro-adjustments preserving self-similarity."""

    def apply(self, vec: Vector, archetype: Union['FractalTensor', Vector, None], kb=None) -> Vector:
        # Resolve archetype root vector if a FractalTensor
        if hasattr(archetype, 'nivel_3') and archetype.nivel_3:
            arche_root = archetype.nivel_3[0]
        else:
            arche_root = archetype or [0, 0, 0]

        # Ensure length 3
        v = list(vec)[:3] + [None] * max(0, 3 - len(vec))
        result = v.copy()

        # Fill None by archetype value (preserve autosimilitud)
        for i in range(3):
            if result[i] is None:
                val = arche_root[i] if arche_root and i < len(arche_root) else 0
                result[i] = val

        # Local single-bit flips that reduce ambiguity (triadic domain {0,1,None})
        best = result
        best_score = Armonizador.ambiguity_score(best, arche_root)
        for i in range(3):
            # try flipping between 0 and 1 (keep None only if archetype suggests None)
            for candidate_val in (0, 1):
                cand = best.copy()
                cand[i] = candidate_val
                cand_score = Armonizador.ambiguity_score(cand, arche_root)
                if cand_score < best_score:
                    best, best_score = cand, cand_score

        logger.debug(f"MicroShift: {v} -> {best}", extra={'ambiguity': best_score})
        return best


class Regrewire(AdjustmentStep):
    """KB-driven rewiring that picks multi-level self-similar archetypes when available."""

    def apply(self, vec: Vector, archetype: Union['FractalTensor', Vector, None], kb=None) -> Vector:
        if kb is None:
            logger.debug("Regrewire: no KB available", extra={'ambiguity': 0})
            return vec

        # Normalize query to simple root vector
        query = list(vec)[:3] + [None] * max(0, 3 - len(vec))

        # Search in default space and across universes for close archetypes
        candidates = []
        try:
            candidates += kb._get_space('default').find_archetype_by_ss(query)
        except Exception:
            pass
        for space_id in getattr(kb, 'universes', {}).keys():
            try:
                candidates += kb._get_space(space_id).find_archetype_by_ss(query)
            except Exception:
                pass

        # Fallback: allow partial matching where None in query acts as a wildcard
        if not candidates:
            try:
                for space_id in getattr(kb, 'universes', {}).keys():
                    space = kb._get_space(space_id)
                    for key, arche in space.ss_index.items():
                        try:
                            key_list = list(key)
                        except Exception:
                            continue
                        match = True
                        for q_val, k_val in zip(query, key_list):
                            if q_val is None:
                                continue
                            if q_val != k_val:
                                match = False
                                break
                        if match:
                            candidates.append(arche)
            except Exception:
                pass

        # Evaluate candidates for multi-level similarity (nivel_3 and nivel_1)
        for cand in candidates:
            if not cand or not hasattr(cand, 'nivel_3'):
                continue
            root = cand.nivel_3[0]
            sim = sum(1 for a, b in zip(root, query) if a == b)
            # Check resumen (nivel_1) consistency when present
            resumen_ok = True
            if hasattr(cand, 'nivel_1'):
                expected_summary = cand.nivel_1[0]
                actual_summary = sum((0 if x is None else int(x)) for x in query) % 8
                resumen_ok = (expected_summary == actual_summary)
            # Accept candidate if strong local similarity AND summary consistent
            if sim >= 2 and resumen_ok:
                logger.info(f"Regrewire: selected archetype {root} (sim={sim})", extra={'ambiguity': 0})
                return list(root)

        logger.debug("Regrewire: no suitable archetype found", extra={'ambiguity': 0})
        return vec


class Metatune(AdjustmentStep):
    """Golden-ratio guided meta adjustments preserving fractal patterns."""

    def apply(self, vec: Vector, archetype: Union['FractalTensor', Vector, None], kb=None) -> Vector:
        # Resolve archetype root
        if hasattr(archetype, 'nivel_3') and archetype.nivel_3:
            arche_root = archetype.nivel_3[0]
        else:
            arche_root = archetype or [0, 0, 0]

        v = list(vec)[:3] + [None] * max(0, 3 - len(vec))
        tuned = v.copy()

        # For None slots prefer archetype; otherwise apply deterministic PHI-based perturbation
        for i in range(3):
            if tuned[i] is None:
                tuned[i] = arche_root[i] if arche_root and i < len(arche_root) else 0
            else:
                # small structured flip: use fractional part of PHI*i to decide
                frac = (PHI * (i + 1)) % 1
                if frac > 0.618:  # bias threshold
                    tuned[i] = tuned[i]
                else:
                    # keep value but ensure triadic (0/1)
                    tuned[i] = 0 if tuned[i] == 0 else 1

        logger.info(f"Metatune: tuned={tuned}", extra={'ambiguity': tuned.count(None)})
        return tuned


class Armonizador:
    """Triadic-aware harmonizer that enforces autosimilarity across fractal levels.

    Behavior:
    - Uses KB to resolve archetypes when available
    - Applies MicroShift, Regrewire, Metatune sequentially
    - Stops early when ambiguity <= thresholds
    - Always returns ternary vector (0,1,None) of length 3
    """

    def __init__(self, knowledge_base=None, *, tau_1: int = 1, tau_2: int = 2, tau_3: int = 3):
        self.kb = knowledge_base
        self.tau_1, self.tau_2, self.tau_3 = tau_1, tau_2, tau_3
        self.steps = [MicroShift(), Regrewire(), Metatune()]

    @staticmethod
    def ambiguity_score(t: Vector, a: Union['FractalTensor', Vector, None]) -> AmbiguityScore:
        # Normalize archetype root
        if hasattr(a, 'nivel_3') and a.nivel_3:
            arche = a.nivel_3[0]
        else:
            arche = a or [0, 0, 0]

        # Ensure length-3 vectors
        t_norm = list(t)[:3] + [None] * max(0, 3 - len(t))
        arche_norm = list(arche)[:3] + [None] * max(0, 3 - len(arche))

        score = 0
        for x, y in zip(t_norm, arche_norm):
            if x is None or y is None:
                score += 1
            elif x != y:
                score += 1

        # small penalty if top-level summary mismatches (when archetype is FractalTensor)
        if hasattr(a, 'nivel_1') and a.nivel_1:
            expected = a.nivel_1[0]
            actual = sum((0 if x is None else int(x)) for x in t_norm) % 8
            if expected != actual:
                score += 1

        return AmbiguityScore(score)

    def harmonize(self, tensor: Vector, *, archetype: Union['FractalTensor', Vector, None] = None, space_id: str = "default") -> Dict[str, Any]:
        # Resolve archetype using KB when not provided
        if archetype is None and self.kb:
            found = self.kb._get_space(space_id).find_archetype_by_ss(tensor)
            archetype = found[0] if found else None

        if archetype is None:
            archetype = [0, 0, 0]

        # Normalize input vector
        vec = list(tensor)[:3] + [None] * max(0, 3 - len(tensor))
        result = vec
        adjustments = []
        score = self.ambiguity_score(result, archetype)

        # Apply steps sequentially with thresholds
        for i, step in enumerate(self.steps, 1):
            tau = getattr(self, f"tau_{i}", None)
            if tau is not None and score <= tau:
                logger.info(f"Stopping before step {i}: ambiguity {score} <= tau_{i}={tau}", extra={'ambiguity': score})
                break

            new_result = step.apply(result, archetype, self.kb)
            adjustments.append(step.__class__.__name__.lower())
            new_score = self.ambiguity_score(new_result, archetype)
            logger.info(f"{step.__class__.__name__}: {new_result} | Score: {new_score}", extra={'ambiguity': new_score})

            # Accept change if it improves or preserves self-similarity
            if new_score <= score:
                result = new_result
                score = new_score

            if score == 0:
                break

        # Ensure output is ternary and length 3
        final = [None if x is None else int(x) if x in (0, 1) else (1 if x else 0) for x in result[:3]]

        return {"output": final, "score": score, "adjustments": adjustments}

class TensorPoolManager:
    """Pool manager for tensor collections."""
    
    def __init__(self):
        self.tensors = []
    
    def add_tensor(self, tensor: FractalTensor):
        """Add tensor to pool."""
        self.tensors.append(tensor)

# ===============================================================================
# PATTERN 0: ETHICAL FRACTAL CLUSTER GENERATION
# ===============================================================================

def apply_ethical_constraint(vector, space_id, kb):
    """Apply ethical constraints via XOR with rules (Aurora triadic logic)."""
    rules = getattr(kb, 'get_ethics', lambda sid: [-1, -1, -1])(space_id) or [-1, -1, -1]
    return [v ^ r if r != -1 else v for v, r in zip(vector, rules)]

def compute_ethical_signature(cluster):
    """Compute ethical signature via SHA256 (fractal hash)."""
    return hashlib.sha256(str([t.nivel_3[0] for t in cluster]).encode()).hexdigest()

def golden_ratio_select(N, seed):
    """Select indices using golden ratio stepping (PHI-based fractal)."""
    return [(seed + i * int(max(1, round(N * PHI)))) % N for i in range(3)]

def _create_tensor(i, input_data, space_id, kb, entropy_seed):
    """Atomic tensor creation with ethical constraints (recursive base case)."""
    if input_data and i < len(input_data):
        vec = apply_ethical_constraint(input_data[i], space_id, kb)
        tensor = FractalTensor(nivel_3=[vec])
    else:
        tensor = FractalTensor.random(space_constraints=space_id) if hasattr(FractalTensor.random, '__code__') and 'space_constraints' in FractalTensor.random.__code__.co_varnames else FractalTensor.random()
    
    tensor.metadata.update({
        "ethical_hash": compute_ethical_signature([tensor]),
        "entropy_seed": entropy_seed,
        "space_id": space_id
    })
    return tensor

def _harmonize_tensor(tensor, armonizador, space_id):
    """Atomic harmonization (recursive base case)."""
    harmonized = armonizador.harmonize(tensor.nivel_3[0], space_id=space_id)
    tensor.nivel_3[0] = harmonized["output"]
    return tensor

def pattern0_create_fractal_cluster(
    *,
    input_data=None,
    space_id="default",
    num_tensors=3,
    context=None,
    entropy_seed=PHI,
    depth_max=3,
):
    """Generate ethical fractal cluster using Pattern 0 (recursive/fractal approach)."""
    random.seed(int(entropy_seed * 1e9))
    
    # Context initialization (reusable fractal components)
    kb = context.get('kb') if context and 'kb' in context else FractalKnowledgeBase()
    armonizador = context.get('armonizador') if context and 'armonizador' in context else Armonizador(knowledge_base=kb)
    pool = context.get('pool') if context and 'pool' in context else TensorPoolManager()
    
    # Recursive tensor generation + harmonization (single pass, fractal pipeline)
    tensors = [
        _harmonize_tensor(
            _create_tensor(i, input_data, space_id, kb, entropy_seed),
            armonizador,
            space_id
        )
        for i in range(num_tensors)
    ]
    
    # Pool management (side effect isolation)
    for tensor in tensors:
        pool.add_tensor(tensor)
    
    return tensors

# ===============================================================================
# PUBLIC API
# ===============================================================================

# Main exports
__all__ = [
    'FractalTensor',
    'Trigate', 
    'TernaryLogic',
    'Evolver',
    'Extender', 
    'FractalKnowledgeBase',
    'Armonizador',
    'TensorPoolManager',
    'Transcender',
    'pattern0_create_fractal_cluster'
]

# Compatibility aliases
KnowledgeBase = FractalKnowledgeBase
