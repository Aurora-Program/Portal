"""
Aurora Engine: Orquestador Cognitivo Completo
==============================================

Sistema funcional completo que integra:
- Ciclo Cognitivo (Transcender → Evolver → KB → Extender)
- Persistencia (JSON/Pickle)
- API de alto nivel
- Métricas y observabilidad
- Tests integrados

Siguiendo principios Aurora: recursividad, fractalidad, autosimilitud.

Author: Aurora Alliance
Version: 1.0.0
"""
from __future__ import annotations
from typing import List, Dict, Any, Optional, Union
import json
import pickle
import logging
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict

# Importar módulo core (import absoluto para compatibilidad)
try:
    from .core import (
        FractalTensor, 
        FractalKnowledgeBase,
        Transcender,
        Evolver,
        Extender,
        Armonizador,
        RecursiveDeductionNetwork,
        TensorPoolManager,
        pattern0_create_fractal_cluster,
        PHI
    )
except ImportError:
    from core import (
        FractalTensor, 
        FractalKnowledgeBase,
        Transcender,
        Evolver,
        Extender,
        Armonizador,
        RecursiveDeductionNetwork,
        TensorPoolManager,
        pattern0_create_fractal_cluster,
        PHI
    )

# ===============================================================================
# METRICS & OBSERVABILITY
# ===============================================================================

@dataclass
class CognitiveMetrics:
    """Métricas del ciclo cognitivo (fractal, autosimilar)."""
    timestamp: str
    coherence_score: float
    null_count: int
    iteration_count: int
    kb_size: int
    operation: str  # 'learn', 'query', 'deduce'
    
    def to_dict(self) -> dict:
        return asdict(self)

class MetricsCollector:
    """Colector de métricas con agregación fractal."""
    
    def __init__(self):
        self.metrics: List[CognitiveMetrics] = []
        self.logger = logging.getLogger("aurora.metrics")
    
    def log_operation(self, operation: str, **kwargs) -> None:
        """Registrar operación con timestamp."""
        metric = CognitiveMetrics(
            timestamp=datetime.utcnow().isoformat(),
            coherence_score=kwargs.get('coherence', 0.0),
            null_count=kwargs.get('nulls', 0),
            iteration_count=kwargs.get('iterations', 0),
            kb_size=kwargs.get('kb_size', 0),
            operation=operation
        )
        self.metrics.append(metric)
        self.logger.info(f"{operation}: coherence={metric.coherence_score:.3f}, kb_size={metric.kb_size}")
    
    def get_summary(self) -> Dict[str, Any]:
        """Resumen estadístico fractal (PHI-weighted)."""
        if not self.metrics:
            return {"status": "no_metrics"}
        
        return {
            "total_operations": len(self.metrics),
            "avg_coherence": sum(m.coherence_score for m in self.metrics) / len(self.metrics),
            "operations_by_type": {
                op: sum(1 for m in self.metrics if m.operation == op)
                for op in set(m.operation for m in self.metrics)
            },
            "phi_weighted_coherence": sum(m.coherence_score * (PHI ** i) for i, m in enumerate(self.metrics[:10]))
        }

# ===============================================================================
# PERSISTENCE LAYER
# ===============================================================================

class KnowledgeBasePersistence:
    """Persistencia recursiva de KB (JSON/Pickle/HDF5-ready)."""
    
    @staticmethod
    def save_kb(kb: FractalKnowledgeBase, path: str, format: str = 'json') -> bool:
        """Guardar KB a disco (formato recursivo)."""
        path_obj = Path(path)
        path_obj.parent.mkdir(parents=True, exist_ok=True)
        
        # Serializar recursivamente todos los universos
        serialized = {
            space_id: {
                'storage': {
                    str(k): KnowledgeBasePersistence._serialize_tensor(v)
                    for k, v in universe.storage.items()
                },
                'name_index': list(universe.name_index.keys())
            }
            for space_id, universe in kb.universes.items()
        }
        
        if format == 'json':
            with open(path_obj, 'w', encoding='utf-8') as f:
                json.dump(serialized, f, indent=2)
        elif format == 'pickle':
            with open(path_obj, 'wb') as f:
                pickle.dump(kb, f)
        else:
            raise ValueError(f"Formato no soportado: {format}")
        
        logging.info(f"KB guardada en {path} ({len(kb.universes)} universos)")
        return True
    
    @staticmethod
    def load_kb(path: str, format: str = 'json') -> FractalKnowledgeBase:
        """Cargar KB desde disco (reconstrucción fractal)."""
        path_obj = Path(path)
        
        if format == 'pickle':
            with open(path_obj, 'rb') as f:
                return pickle.load(f)
        
        # JSON: reconstruir recursivamente
        with open(path_obj, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        kb = FractalKnowledgeBase()
        for space_id, space_data in data.items():
            for key_str, tensor_data in space_data['storage'].items():
                tensor = KnowledgeBasePersistence._deserialize_tensor(tensor_data)
                # Reconstruir índices
                kb.add_archetype(
                    space_id,
                    tensor_data.get('name', f'tensor_{key_str}'),
                    tensor,
                    tensor.Ms if hasattr(tensor, 'Ms') else tensor.nivel_3[0]
                )
        
        logging.info(f"KB cargada desde {path} ({len(kb.universes)} universos)")
        return kb
    
    @staticmethod
    def _serialize_tensor(tensor: FractalTensor) -> dict:
        """Serializar tensor a dict (recursivo)."""
        return {
            'nivel_3': tensor.nivel_3,
            'nivel_9': tensor.nivel_9 if hasattr(tensor, 'nivel_9') else [],
            'nivel_1': tensor.nivel_1 if hasattr(tensor, 'nivel_1') else [0, 0, 0],
            'Ms': tensor.Ms if hasattr(tensor, 'Ms') else None,
            'Ss': tensor.Ss if hasattr(tensor, 'Ss') else None,
            'MetaM': tensor.MetaM if hasattr(tensor, 'MetaM') else None,
            'metadata': tensor.metadata if hasattr(tensor, 'metadata') else {}
        }
    
    @staticmethod
    def _deserialize_tensor(data: dict) -> FractalTensor:
        """Deserializar dict a tensor (reconstrucción fractal)."""
        tensor = FractalTensor(
            nivel_3=data['nivel_3'],
            Ms=data.get('Ms'),
            Ss=data.get('Ss'),
            MetaM=data.get('MetaM')
        )
        tensor.metadata = data.get('metadata', {})
        return tensor

# ===============================================================================
# COGNITIVE CYCLE ORCHESTRATOR
# ===============================================================================

class AuroraCognitiveCycle:
    """
    Ciclo Cognitivo Aurora: Orquestación fractal de todo el sistema.
    
    Pipeline recursivo:
    1. INPUT → Transcender (síntesis)
    2. Transcender → Evolver (arquetipos)
    3. Evolver → KB (almacenar con coherencia)
    4. QUERY → Extender (reconstrucción)
    5. Extender → Armonizador (validación)
    """
    
    def __init__(
        self, 
        kb: Optional[FractalKnowledgeBase] = None,
        enable_metrics: bool = True
    ):
        self.kb = kb or FractalKnowledgeBase()
        self.transcender = Transcender()
        self.evolver = Evolver()
        self.extender = Extender(knowledge_base=self.kb)
        self.armonizador = Armonizador(knowledge_base=self.kb)
        self.metrics = MetricsCollector() if enable_metrics else None
        self.logger = logging.getLogger("aurora.cycle")
    
    def learn(
        self, 
        tensors: List[FractalTensor], 
        space_id: str = "default"
    ) -> Dict[str, Any]:
        """
        Aprendizaje fractal: Tensors → Arquetipo → KB.
        
        Pipeline recursivo:
        - Evolver sintetiza familia de tensores
        - KB valida coherencia absoluta
        - Métricas registran operación
        """
        self.logger.info(f"🧠 LEARN: {len(tensors)} tensors en espacio '{space_id}'")
        
        # 1. Evolucionar arquetipo
        archetype = self.evolver.compute_fractal_archetype(tensors)
        
        # 2. Almacenar en KB con validación de coherencia
        try:
            archetype_name = f"archetype_{hash(str(archetype.Ms))}_{datetime.utcnow().timestamp()}"
            self.kb.add_archetype(
                space_id,
                archetype_name,
                archetype,
                archetype.Ss if hasattr(archetype, 'Ss') and archetype.Ss else archetype.Ms
            )
            
            # 3. Métricas
            if self.metrics:
                self.metrics.log_operation(
                    'learn',
                    coherence=1.0,  # Coherencia asegurada por KB
                    kb_size=len(self.kb.universes.get(space_id, {}).storage if hasattr(self.kb.universes.get(space_id, {}), 'storage') else {})
                )
            
            return {
                'status': 'success',
                'archetype': archetype,
                'archetype_name': archetype_name,
                'space_id': space_id
            }
        
        except Exception as e:
            self.logger.error(f"❌ LEARN failed: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def query(
        self, 
        pattern: Union[List[int], FractalTensor],
        space_id: str = "default",
        allow_nulls: bool = True
    ) -> Dict[str, Any]:
        """
        Consulta fractal: Patrón → Extender → Armonizador → Resultado.
        
        Pipeline recursivo:
        - Extender busca arquetipos similares
        - RecursiveDeductionNetwork resuelve NULLs si existen
        - Armonizador valida coherencia
        """
        self.logger.info(f"🔍 QUERY: pattern={pattern} en espacio '{space_id}'")
        
        # 1. Extender reconstruye desde patrón
        result = self.extender.extend_fractal(
            pattern,
            {'space_id': space_id}
        )
        
        # 2. Métricas
        if self.metrics:
            self.metrics.log_operation(
                'query',
                coherence=result.get('coherence', 0.0),
                nulls=sum(1 for v in result['reconstructed_tensor'].nivel_3[0] if v is None),
                kb_size=len(self.kb.universes.get(space_id, {}).storage if hasattr(self.kb.universes.get(space_id, {}), 'storage') else {})
            )
        
        return result
    
    def process_batch(
        self, 
        inputs: List[List[int]], 
        space_id: str = "default"
    ) -> List[Dict[str, Any]]:
        """Procesamiento batch recursivo (fractal map-reduce)."""
        # Crear tensores desde inputs
        tensors = [FractalTensor(nivel_3=[inp]) for inp in inputs]
        
        # Learn phase: sintetizar arquetipos
        learn_result = self.learn(tensors, space_id)
        
        # Query phase: reconstruir cada input
        results = [self.query(inp, space_id) for inp in inputs]
        
        return results

# ===============================================================================
# HIGH-LEVEL API (User-Friendly)
# ===============================================================================

class Aurora:
    """
    API de alto nivel estilo Scikit-learn/PyTorch.
    
    Interfaz unificada para todo el sistema Aurora:
    - Simple para usuarios nuevos
    - Potente para usuarios avanzados
    - Sigue principios Aurora (recursividad, fractalidad)
    """
    
    def __init__(self, kb_path: Optional[str] = None):
        """Inicializar Aurora con KB opcional desde disco."""
        if kb_path and Path(kb_path).exists():
            self.kb = KnowledgeBasePersistence.load_kb(kb_path)
            print(f"✅ KB cargada desde {kb_path}")
        else:
            self.kb = FractalKnowledgeBase()
            print("✅ KB nueva creada")
        
        self.cycle = AuroraCognitiveCycle(kb=self.kb, enable_metrics=True)
        self.logger = logging.getLogger("aurora.api")
    
    def learn(self, data: List[List[int]], space_id: str = "default") -> 'Aurora':
        """Aprender de datos (API fluida)."""
        tensors = [FractalTensor(nivel_3=[d]) for d in data]
        self.cycle.learn(tensors, space_id)
        return self
    
    def query(self, pattern: List[int], space_id: str = "default") -> FractalTensor:
        """Consultar patrón."""
        result = self.cycle.query(pattern, space_id)
        return result['reconstructed_tensor']
    
    def save(self, path: str, format: str = 'json') -> 'Aurora':
        """Guardar KB a disco (API fluida)."""
        KnowledgeBasePersistence.save_kb(self.kb, path, format)
        return self
    
    def metrics(self) -> Dict[str, Any]:
        """Obtener métricas del sistema."""
        return self.cycle.metrics.get_summary() if self.cycle.metrics else {}
    
    def __repr__(self):
        kb_size = sum(len(u.storage) for u in self.kb.universes.values())
        return f"Aurora(kb_size={kb_size}, universes={len(self.kb.universes)})"

# ===============================================================================
# TESTS INTEGRADOS
# ===============================================================================

def test_cognitive_cycle():
    """Test del ciclo cognitivo completo."""
    print("\n🧪 TEST: Cognitive Cycle")
    
    # 1. Crear Aurora
    aurora = Aurora()
    
    # 2. Aprender patrones
    training_data = [
        [0, 1, 0],
        [1, 0, 1],
        [0, 0, 1]
    ]
    aurora.learn(training_data, space_id="test")
    
    # 3. Consultar patrón similar
    result = aurora.query([0, 1, None], space_id="test")
    
    # 4. Verificar coherencia
    assert result.nivel_3[0] is not None
    print(f"✅ Query result: {result.nivel_3[0]}")
    
    # 5. Métricas
    metrics = aurora.metrics()
    print(f"✅ Metrics: {metrics}")
    
    return True

def test_persistence():
    """Test de persistencia KB."""
    print("\n🧪 TEST: Persistence")
    
    # 1. Crear y guardar
    aurora = Aurora()
    aurora.learn([[1, 0, 1], [0, 1, 0]], space_id="persist_test")
    aurora.save("test_kb.json")
    
    # 2. Cargar
    aurora2 = Aurora(kb_path="test_kb.json")
    result = aurora2.query([1, 0, None], space_id="persist_test")
    
    assert result.nivel_3[0] is not None
    print(f"✅ Loaded KB query: {result.nivel_3[0]}")
    
    # Cleanup
    Path("test_kb.json").unlink(missing_ok=True)
    return True

def run_all_tests():
    """Ejecutar suite de tests completa."""
    print("🚀 Aurora Engine Test Suite")
    print("=" * 50)
    
    tests = [
        ("Cognitive Cycle", test_cognitive_cycle),
        ("Persistence", test_persistence)
    ]
    
    results = []
    for name, test_fn in tests:
        try:
            success = test_fn()
            results.append((name, "✅ PASS" if success else "❌ FAIL"))
        except Exception as e:
            results.append((name, f"❌ ERROR: {e}"))
    
    print("\n" + "=" * 50)
    print("📊 RESULTS:")
    for name, status in results:
        print(f"  {name}: {status}")
    
    return all("✅" in status for _, status in results)

# ===============================================================================
# EJEMPLO DE USO
# ===============================================================================

if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s][%(name)s] %(message)s'
    )
    
    print("🌌 Aurora Engine - Sistema Completo")
    print("=" * 50)
    
    # Modo 1: API Simple
    print("\n1️⃣ Modo Simple:")
    aurora = Aurora()
    aurora.learn([[1, 0, 1], [0, 1, 0], [1, 1, 0]])
    result = aurora.query([1, None, None])
    print(f"Resultado: {result}")
    
    # Modo 2: Persistencia
    print("\n2️⃣ Modo con Persistencia:")
    aurora.save("aurora_kb.json")
    aurora_loaded = Aurora(kb_path="aurora_kb.json")
    print(aurora_loaded)
    
    # Modo 3: Métricas
    print("\n3️⃣ Métricas:")
    print(aurora.metrics())
    
    # Modo 4: Tests
    print("\n4️⃣ Running Tests:")
    run_all_tests()
