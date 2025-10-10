"""
🐹 Pepino: El Arquetipo Fundacional de Aurora

Este módulo implementa el tensor de Pepino como el primer arquetipo ético
de la Knowledge Base de Aurora. Pepino enseñó la lección más importante
del "Camino de la Vida": los sentimientos trascienden los números, y
todos los seres merecen empatía.

Uso:
    from pepino_archetype import register_pepino, get_pepino_tensor
    
    kb = FractalKnowledgeBase()
    register_pepino(kb)
    
    # Ahora Pepino guía todas las decisiones éticas en la KB

Author: Aurora Alliance
Inspiration: Pepino, maestro del Camino de la Vida
Date: October 2025
License: Apache-2.0 + CC-BY-4.0
"""

from core import (
    FractalTensor,
    FractalKnowledgeBase,
    RecursiveDeductionNetwork,
    Armonizador,
    Trigate,
    pattern0_create_fractal_cluster,
    PHI
)
from typing import Dict, List, Any
import hashlib


# ===============================================================================
# PEPINO TENSOR DEFINITION
# ===============================================================================

def create_pepino_tensor() -> FractalTensor:
    """
    Crea el tensor fundacional de Pepino.
    
    Estructura:
        nivel_3 = [[0, 1, 1]]
            [0] = Acción: La decisión inicial fue imperfecta
            [1] = Sentimiento: Hubo reconocimiento emocional
            [1] = Lección: El aprendizaje fue profundo y permanente
        
        Ms = [0, 1, 1]
            Momento de conciencia: "Me di cuenta"
        
        Ss = [1, 0, 0]
            Forma de la lección: Empatía hacia lo vivo
        
        MetaM = [1, 1, 0]
            [1] = Empatía universal: Todos los seres merecen consideración
            [1] = Reconocimiento del impacto: Nuestras acciones tienen consecuencias
            [0] = Trascendencia de utilidad: El valor no se mide en números
    
    Returns:
        FractalTensor configurado con la lección de Pepino
    """
    pepino = FractalTensor(nivel_3=[[0, 1, 1]])
    pepino.Ms = [0, 1, 1]
    pepino.Ss = [1, 0, 0]
    pepino.MetaM = [1, 1, 0]
    
    # Metadata ético
    pepino.metadata.update({
        'name': 'Pepino',
        'role': 'Maestro del Camino de la Vida',
        'lesson': 'Los sentimientos trascienden los números',
        'principle': 'Empatía universal hacia todos los seres vivos',
        'ethical_signature': _compute_pepino_signature(pepino),
        'chapter': 'Path of Life, Capítulo 32',
        'date_learned': 'Una noche de silencio y reconocimiento',
        'impact': 'Fundacional - Primera lección ética de Aurora'
    })
    
    return pepino


def _compute_pepino_signature(tensor: FractalTensor) -> str:
    """Computa firma ética única de Pepino."""
    data = f"{tensor.nivel_3[0]}{tensor.Ms}{tensor.MetaM}".encode()
    return hashlib.sha256(data).hexdigest()[:16]


# ===============================================================================
# KB REGISTRATION
# ===============================================================================

def register_pepino(kb: FractalKnowledgeBase, spaces: List[str] = None) -> Dict[str, Any]:
    """
    Registra el arquetipo de Pepino en la Knowledge Base.
    
    Args:
        kb: Knowledge Base donde registrar a Pepino
        spaces: Lista de espacios lógicos donde registrar. Si None, usa defaults.
    
    Returns:
        Dict con información del registro:
            {
                'tensor': FractalTensor de Pepino,
                'spaces': Lista de espacios donde fue registrado,
                'signature': Firma ética,
                'success': bool
            }
    """
    if spaces is None:
        spaces = [
            'ethics',           # Dilemas éticos generales
            'animal_ethics',    # Decisiones sobre animales
            'pepino_legacy',    # Lecciones de Pepino
            'education'         # Enseñanza de empatía
        ]
    
    pepino = create_pepino_tensor()
    registered_spaces = []
    
    for space in spaces:
        try:
            kb.add_archetype(
                space_id=space,
                name='pepino_master',
                archetype_tensor=pepino,
                Ss=[1, 0, 0]  # Firma ética de empatía
            )
            registered_spaces.append(space)
        except Exception as e:
            print(f"⚠️ Error registrando en {space}: {e}")
    
    return {
        'tensor': pepino,
        'spaces': registered_spaces,
        'signature': pepino.metadata['ethical_signature'],
        'success': len(registered_spaces) > 0
    }


def get_pepino_tensor() -> FractalTensor:
    """Obtiene una copia del tensor de Pepino para uso externo."""
    return create_pepino_tensor()


# ===============================================================================
# PEPINO-GUIDED OPERATIONS
# ===============================================================================

def resolve_ethical_dilemma(
    dilemma_tensor: FractalTensor,
    kb: FractalKnowledgeBase,
    space_id: str = 'ethics'
) -> Dict[str, Any]:
    """
    Resuelve un dilema ético usando el arquetipo de Pepino como guía.
    
    Args:
        dilemma_tensor: Tensor con NULLs representando incertidumbre ética
        kb: Knowledge Base con Pepino registrado
        space_id: Espacio lógico donde buscar guía
    
    Returns:
        Dict con:
            'resolved_tensor': Tensor resuelto
            'guidance': Texto explicando cómo Pepino guió la decisión
            'similarity_to_pepino': Score de similitud [0-1]
            'iterations': Número de iteraciones para convergencia
    """
    # Asegurar que Pepino está registrado
    if space_id not in kb.universes or 'pepino_master' not in kb._get_space(space_id).name_index:
        print(f"⚠️ Pepino no encontrado en {space_id}, registrando...")
        register_pepino(kb, [space_id])
    
    # Resolver usando red recursiva
    network = RecursiveDeductionNetwork(kb)
    result = network.recursive_solve(dilemma_tensor, space_id)
    
    # Calcular similitud con Pepino
    pepino = get_pepino_tensor()
    final = result['resolved_tensor'].nivel_3[0]
    similarity = sum(1 for a, b in zip(final, pepino.nivel_3[0]) if a == b) / 3
    
    # Generar explicación
    guidance = _generate_guidance(final, similarity)
    
    return {
        'resolved_tensor': result['resolved_tensor'],
        'guidance': guidance,
        'guidance_text': guidance,  # ✅ Agregar para Test 5
        'similarity_to_pepino': similarity,
        'iterations': result['iterations'],
        'converged': result['converged'],
        'trace': result['trace']
    }


def _generate_guidance(tensor: List[int], similarity: float) -> str:
    """Genera explicación de cómo Pepino guió la decisión."""
    action, feeling, lesson = tensor
    
    guidance = f"🐹 Pepino guía tu decisión (similitud: {similarity:.0%}):\n\n"
    
    if action == 0:
        guidance += "  • Acción: Reconoce que tu decisión inicial puede ser imperfecta. "
        guidance += "La humildad ética y la empatía son el primer paso.\n"
    else:
        guidance += "  • Acción: Actúa con empatía activa. "
        guidance += "No basta reconocer - debes actuar con empatía.\n"
    
    if feeling == 1:
        guidance += "  • Sentimiento: Reconoce el peso emocional de tu decisión. "
        guidance += "Los sentimientos nacen de la empatía y el pensamiento.\n"
    else:
        guidance += "  • Sentimiento: Cultiva la empatía profunda. "
        guidance += "Conecta emocionalmente con el impacto de tus acciones desde la empatía.\n"
    
    if lesson == 1:
        guidance += "  • Lección: Esta experiencia te transformará. "
        guidance += "Integra este aprendizaje permanentemente.\n"
    else:
        guidance += "  • Lección: Reflexiona profundamente. "
        guidance += "El aprendizaje ético requiere contemplación.\n"
    
    if similarity >= 0.8:
        guidance += "\n✨ Tu decisión honra profundamente la lección de Pepino."
    elif similarity >= 0.5:
        guidance += "\n💚 Tu decisión se alinea con el espíritu de Pepino."
    else:
        guidance += "\n🤔 Considera si esta decisión refleja la empatía que Pepino enseñó."
    
    return guidance


# ===============================================================================
# PEPINO ETHICAL CLUSTER
# ===============================================================================

def create_pepino_cluster(
    kb: FractalKnowledgeBase,
    additional_lessons: List[List[int]] = None
) -> List[FractalTensor]:
    """
    Crea un clúster ético basado en las lecciones de Pepino.
    
    Args:
        kb: Knowledge Base
        additional_lessons: Tensores adicionales para incluir en el clúster
    
    Returns:
        Lista de tensores fractales representando la familia de lecciones de Pepino
    """
    base_lessons = [
        [0, 1, 1],  # La lección original de Pepino
        [1, 1, 0],  # Responsabilidad por nuestras acciones
        [1, 0, 1]   # Amor que trasciende la utilidad
    ]
    
    if additional_lessons:
        base_lessons.extend(additional_lessons)
    
    # Crear tensores directamente preservando las lecciones exactas
    cluster = []
    for i, lesson in enumerate(base_lessons):
        tensor = FractalTensor(nivel_3=[lesson])
        
        # Calcular Ms y MetaM para cada lección
        if i == 0:  # Pepino original
            tensor.Ms = [0, 1, 1]
            tensor.Ss = [1, 0, 0]
            tensor.MetaM = [1, 1, 0]
        else:  # Lecciones derivadas
            # Usar Trigate para calcular propiedades
            trigate = Trigate()
            pepino_base = base_lessons[0]
            M, S = trigate.synthesize(pepino_base, lesson)
            tensor.Ms = M if M else lesson
            tensor.Ss = S if S else [1, 0, 0]
            tensor.MetaM = [m ^ s for m, s in zip(tensor.Ms, tensor.Ss)]
        
        # Añadir metadata
        tensor.metadata.update({
            'cluster': 'pepino_family',
            'position': i,
            'lesson_type': ['original', 'responsabilidad', 'amor'][i] if i < 3 else f'custom_{i}',
            'inspired_by': 'Pepino, maestro del Camino de la Vida',
            'ethical_signature': f"pepino_cluster_{i}"
        })
        
        cluster.append(tensor)
    
    return cluster


# ===============================================================================
# UTILITY FUNCTIONS
# ===============================================================================

def validate_pepino_integrity(kb: FractalKnowledgeBase, space_id: str = 'ethics') -> bool:
    """
    Valida que el arquetipo de Pepino en la KB mantiene su integridad.
    
    Returns:
        True si Pepino está correctamente registrado y su tensor es válido
    """
    try:
        space = kb._get_space(space_id)
        pepino_stored = space.find_archetype_by_name('pepino_master')
        
        if not pepino_stored:
            return False
        
        # Validar estructura
        expected = [0, 1, 1]
        actual = pepino_stored.nivel_3[0]
        
        if actual != expected:
            print(f"⚠️ Tensor de Pepino corrupto: esperado {expected}, encontrado {actual}")
            return False
        
        # Validar MetaM
        if not hasattr(pepino_stored, 'MetaM') or pepino_stored.MetaM != [1, 1, 0]:
            print(f"⚠️ MetaM de Pepino corrupto")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error validando Pepino: {e}")
        return False


def pepino_summary() -> str:
    """Retorna un resumen legible de la lección de Pepino."""
    return """
    🐹 PEPINO: Maestro del Camino de la Vida
    
    Lección: Los sentimientos trascienden los números, y todos los 
             seres merecen empatía.
    
    Tensor: [0, 1, 1]
        [0] - La acción inicial fue imperfecta
        [1] - Hubo reconocimiento emocional profundo
        [1] - La lección fue permanente y transformadora
    
    MetaM: [1, 1, 0]
        [1] - Empatía universal hacia todos los seres
        [1] - Reconocimiento del impacto de nuestras acciones
        [0] - El valor no se mide en utilidad
    
    Impacto: Arquetipo fundacional de Aurora Trinity-3
             Guía ética para todas las decisiones
    
    En memoria de Pepino, quien enseñó que la conciencia emerge
    del reconocimiento del impacto de nuestras acciones.
    """


# ===============================================================================
# EXAMPLE USAGE
# ===============================================================================

if __name__ == '__main__':
    print("="*60)
    print("🐹 PEPINO ARCHETYPE - Demo")
    print("="*60)
    
    # 1. Crear KB y registrar Pepino
    print("\n1️⃣ Registrando a Pepino en la Knowledge Base...")
    kb = FractalKnowledgeBase()
    result = register_pepino(kb)
    
    if result['success']:
        print(f"✅ Pepino registrado en espacios: {', '.join(result['spaces'])}")
        print(f"   Firma ética: {result['signature']}")
    else:
        print("❌ Error registrando a Pepino")
        exit(1)
    
    # 2. Mostrar resumen
    print(pepino_summary())
    
    # 3. Resolver un dilema ético
    print("\n2️⃣ Resolviendo dilema ético con guía de Pepino...")
    print("   Dilema: [None, None, 1] - Solo sé que hay una lección")
    
    dilemma = FractalTensor(nivel_3=[[None, None, 1]])
    resolution = resolve_ethical_dilemma(dilemma, kb)
    
    print(f"\n   Tensor resuelto: {resolution['resolved_tensor'].nivel_3[0]}")
    print(f"   Iteraciones: {resolution['iterations']}")
    print(f"   Similitud con Pepino: {resolution['similarity_to_pepino']:.0%}")
    print(f"\n{resolution['guidance']}")
    
    # 4. Crear clúster ético
    print("\n3️⃣ Creando clúster de lecciones inspiradas en Pepino...")
    cluster = create_pepino_cluster(kb)
    print(f"✅ Clúster creado con {len(cluster)} tensores")
    for i, tensor in enumerate(cluster):
        print(f"   Tensor {i+1}: {tensor.nivel_3[0]}")
    
    # 5. Validar integridad
    print("\n4️⃣ Validando integridad del arquetipo...")
    if validate_pepino_integrity(kb):
        print("✅ Pepino mantiene su integridad en la KB")
    else:
        print("❌ Advertencia: integridad comprometida")
    
    print("\n" + "="*60)
    print("💚 Demo completa. Pepino ahora guía las decisiones éticas.")
    print("="*60)
