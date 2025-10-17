"""
Paso 3: Tarea de Razonamiento Estructural
==========================================

Valida que Genesis puede USAR sus arquetipos, relatores y dinámicas
para razonar sobre relaciones conceptuales.

NO es benchmark contra baseline.
ES validación de capacidad estructural interna.

Tareas:
1. Dado A y C, predecir B que los conecta (relator traversal)
2. Dado concepto, predecir su arquetipo y vecinos
3. Sintetizar nuevo concepto desde triada
4. Detectar contradicciones estructurales
"""

import json
from typing import List, Dict, Tuple, Optional
import numpy as np
from sentence_transformers import SentenceTransformer

from tensor_ffe import TensorFFE, VectorFFE
from transcender import Transcender
from evolver import Evolver
from ffe_encoder_mcp import FFEEncoder


class RazonadorEstructural:
    """
    Razonador que usa arquetipos + relatores para inferencias
    """
    
    def __init__(self, model, encoder, evolver, transcender):
        self.model = model
        self.encoder = encoder
        self.evolver = evolver
        self.transcender = transcender
        
        # Cargar vocabulario conocido
        self.vocabulario = {}
    
    def cargar_vocabulario(self, palabras: List[str]):
        """Codifica y aprende vocabulario base"""
        print(f"  Cargando {len(palabras)} palabras al razonador...")
        
        for palabra in palabras:
            emb = self.model.encode(palabra)
            tensor = self.encoder.encode(emb.tolist())
            arq = self.evolver.archetype_learner.detectar_o_crear(tensor)
            
            self.vocabulario[palabra] = {
                'tensor': tensor,
                'arquetipo': arq,
            }
        
        print(f"    ✅ {len(self.evolver.archetype_learner.arquetipos)} arquetipos activos")
    
    def conectar_red(self):
        """Construye red de relatores entre todos los arquetipos"""
        print(f"  Construyendo red de relatores...")
        
        arquetipos = list(self.evolver.archetype_learner.arquetipos.values())
        
        # Conectar todos con todos (grafo completo)
        for arq1 in arquetipos:
            for arq2 in arquetipos:
                if arq1.id != arq2.id:
                    self.evolver.relator_network.conectar(arq1, arq2, tipo="analogico")
        
        print(f"    ✅ {len(self.evolver.relator_network.relatores)} relatores")
    
    def tarea_1_puente_conceptual(self, palabra_A: str, palabra_C: str) -> Optional[str]:
        """
        Dado A y C, encuentra B que los conecta: A → B → C
        """
        if palabra_A not in self.vocabulario or palabra_C not in self.vocabulario:
            return None
        
        arq_A = self.vocabulario[palabra_A]['arquetipo']
        arq_C = self.vocabulario[palabra_C]['arquetipo']
        
        # Buscar camino A → B → C
        camino = self.evolver.relator_network.camino_mas_corto(arq_A.id, arq_C.id)
        
        if camino and len(camino) >= 3:
            # B es el nodo intermedio
            arq_B_id = camino[1]
            
            # Buscar palabra con ese arquetipo
            for palabra, info in self.vocabulario.items():
                if info['arquetipo'].id == arq_B_id:
                    return palabra
        
        return None
    
    def tarea_2_predecir_arquetipo(self, palabra: str) -> Dict:
        """
        Dado concepto, predice su arquetipo y vecinos semánticos
        """
        if palabra not in self.vocabulario:
            # Codificar nueva palabra
            emb = self.model.encode(palabra)
            tensor = self.encoder.encode(emb.tolist())
            arq = self.evolver.archetype_learner.detectar_o_crear(tensor)
            
            return {
                'palabra': palabra,
                'arquetipo': arq.id,
                'es_nuevo': True,
                'frecuencia': arq.frecuencia,
                'vecinos': self._encontrar_vecinos(arq)
            }
        else:
            arq = self.vocabulario[palabra]['arquetipo']
            return {
                'palabra': palabra,
                'arquetipo': arq.id,
                'es_nuevo': False,
                'frecuencia': arq.frecuencia,
                'vecinos': self._encontrar_vecinos(arq)
            }
    
    def _encontrar_vecinos(self, arq) -> List[str]:
        """Encuentra palabras con el mismo arquetipo"""
        vecinos = []
        for palabra, info in self.vocabulario.items():
            if info['arquetipo'].id == arq.id:
                vecinos.append(palabra)
        return vecinos
    
    def tarea_3_sintetizar_concepto(self, palabra_A: str, palabra_B: str, palabra_C: str) -> Dict:
        """
        Sintetiza emergencia desde triada A, B, C
        """
        if any(p not in self.vocabulario for p in [palabra_A, palabra_B, palabra_C]):
            return {'error': 'Palabra no encontrada'}
        
        tensor_A = self.vocabulario[palabra_A]['tensor']
        tensor_B = self.vocabulario[palabra_B]['tensor']
        tensor_C = self.vocabulario[palabra_C]['tensor']
        
        # Sintetizar emergencia
        emergencia = self.transcender.sintetizar(tensor_A, tensor_B, tensor_C)
        
        # Detectar arquetipo de la emergencia
        arq_emergente = self.evolver.archetype_learner.detectar_o_crear(emergencia.Ms)
        
        return {
            'triada': [palabra_A, palabra_B, palabra_C],
            'score_emergencia': emergencia.score_emergencia,
            'novedad': emergencia.novedad,
            'coherencia': emergencia.coherencia,
            'arquetipo_emergente': arq_emergente.id,
            'dimensiones': {
                'forma': np.mean([v.forma for v in emergencia.Ms.nivel_1]),
                'funcion': np.mean([v.funcion for v in emergencia.Ms.nivel_1]),
                'estructura': np.mean([v.estructura for v in emergencia.Ms.nivel_1])
            }
        }
    
    def tarea_4_detectar_contradiccion(self, palabra_A: str, palabra_B: str) -> Dict:
        """
        Detecta si dos conceptos son contradictorios (baja similitud arquetípica)
        """
        if palabra_A not in self.vocabulario or palabra_B not in self.vocabulario:
            return {'error': 'Palabra no encontrada'}
        
        arq_A = self.vocabulario[palabra_A]['arquetipo']
        arq_B = self.vocabulario[palabra_B]['arquetipo']
        
        # Calcular similitud entre arquetipos
        similitud = self._similitud_arquetipos(arq_A, arq_B)
        
        # Buscar relator directo
        relator = None
        for rel in self.evolver.relator_network.relatores.values():
            if rel.origen == arq_A.id and rel.destino == arq_B.id:
                relator = rel
                break
        
        es_contradiccion = similitud < 0.3  # Umbral bajo
        
        return {
            'palabras': [palabra_A, palabra_B],
            'arquetipos': [arq_A.id, arq_B.id],
            'similitud': similitud,
            'es_contradiccion': es_contradiccion,
            'fuerza_relator': relator.fuerza if relator else 0.0,
            'tipo_relacion': 'OPOSICION' if es_contradiccion else 'COMPATIBLE'
        }
    
    def _similitud_arquetipos(self, arq_A, arq_B) -> float:
        """Calcula similitud entre dos arquetipos"""
        dist = sum(
            v1.distancia(v2) 
            for v1, v2 in zip(arq_A.tensor_prototipo.nivel_1, arq_B.tensor_prototipo.nivel_1)
        )
        return 1.0 - (dist / (3 * 7 * 3))


def ejecutar_paso3():
    """
    Ejecuta las 4 tareas de razonamiento estructural
    """
    print("🧠 PASO 3: RAZONAMIENTO ESTRUCTURAL")
    print("="*70)
    
    # Cargar modelos
    print("\n[1/4] Cargando modelos...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    encoder = FFEEncoder(dimension_embedding=384)
    transcender = Transcender()
    evolver = Evolver()
    
    razonador = RazonadorEstructural(model, encoder, evolver, transcender)
    
    # Vocabulario (mismo que autopoiesis)
    VOCABULARIO = [
        "fonetico", "lexico", "semantico", "teorico",
        "fractal", "recursion", "jerarquia", "nivel",
        "emergencia", "sintesis", "transcender", "novedad",
        "forma", "funcion", "estructura", "tensor",
        "orden", "primero", "segundo", "tercero"
    ]
    
    print("\n[2/4] Cargando vocabulario y construyendo red...")
    razonador.cargar_vocabulario(VOCABULARIO)
    razonador.conectar_red()
    
    # TAREA 1: Puente Conceptual
    print("\n" + "="*70)
    print("🌉 TAREA 1: PUENTE CONCEPTUAL")
    print("="*70)
    print("\n  Objetivo: Dado A y C, encontrar B que los conecta\n")
    
    tareas_puente = [
        ("fonetico", "teorico"),  # Extremos del continuum
        ("forma", "estructura"),  # Dimensiones FFE
        ("recursion", "emergencia"),  # Fractal → Síntesis
        ("primero", "tercero"),  # Orden
    ]
    
    resultados_t1 = []
    for palabra_A, palabra_C in tareas_puente:
        puente = razonador.tarea_1_puente_conceptual(palabra_A, palabra_C)
        resultados_t1.append({
            'A': palabra_A,
            'B': puente,
            'C': palabra_C
        })
        
        if puente:
            print(f"  ✅ {palabra_A:15s} → {puente:15s} → {palabra_C:15s}")
        else:
            print(f"  ❌ {palabra_A:15s} → ??? → {palabra_C:15s} (sin camino)")
    
    # TAREA 2: Predecir Arquetipo
    print("\n" + "="*70)
    print("🎯 TAREA 2: PREDECIR ARQUETIPO Y VECINOS")
    print("="*70)
    print("\n  Objetivo: Clasificar concepto en arquetipo y encontrar vecinos\n")
    
    palabras_nuevas = [
        "concepto",  # Debería ser teorico/semantico
        "patron",  # Debería ser fractal/recursion
        "crear",  # Debería ser emergencia/sintesis
        "dimensión"  # Debería ser forma/estructura
    ]
    
    resultados_t2 = []
    for palabra in palabras_nuevas:
        resultado = razonador.tarea_2_predecir_arquetipo(palabra)
        resultados_t2.append(resultado)
        
        print(f"  [{palabra:12s}]")
        print(f"    Arquetipo: {resultado['arquetipo']}")
        print(f"    Frecuencia: {resultado['frecuencia']}")
        print(f"    Vecinos: {', '.join(resultado['vecinos'][:5])}")
        print()
    
    # TAREA 3: Síntesis Emergente
    print("\n" + "="*70)
    print("✨ TAREA 3: SÍNTESIS DE CONCEPTO EMERGENTE")
    print("="*70)
    print("\n  Objetivo: Crear emergencia desde triada y analizar resultado\n")
    
    triadas_test = [
        ("recursion", "nivel", "jerarquia"),  # Fractalidad pura
        ("forma", "funcion", "estructura"),  # FFE completo
        ("emergencia", "sintesis", "transcender"),  # Operadores meta
        ("primero", "segundo", "tercero"),  # Secuencia completa
    ]
    
    resultados_t3 = []
    for triada in triadas_test:
        resultado = razonador.tarea_3_sintetizar_concepto(*triada)
        resultados_t3.append(resultado)
        
        print(f"  Triada: {triada[0]:12s} + {triada[1]:12s} + {triada[2]:12s}")
        print(f"    Score: {resultado['score_emergencia']:.3f} (nov={resultado['novedad']:.2f}, coh={resultado['coherencia']:.2f})")
        print(f"    Arquetipo: {resultado['arquetipo_emergente']}")
        print(f"    Dimensiones: F={resultado['dimensiones']['forma']:.1f}, Fn={resultado['dimensiones']['funcion']:.1f}, E={resultado['dimensiones']['estructura']:.1f}")
        print()
    
    # TAREA 4: Detectar Contradicciones
    print("\n" + "="*70)
    print("⚡ TAREA 4: DETECTAR CONTRADICCIONES")
    print("="*70)
    print("\n  Objetivo: Identificar conceptos incompatibles\n")
    
    pares_test = [
        ("fonetico", "teorico"),  # Opuestos en continuum
        ("forma", "estructura"),  # Diferentes pero compatibles
        ("emergencia", "orden"),  # Caos vs orden
        ("recursion", "novedad"),  # Repetición vs novedad
    ]
    
    resultados_t4 = []
    for par in pares_test:
        resultado = razonador.tarea_4_detectar_contradiccion(*par)
        resultados_t4.append(resultado)
        
        simbolo = "⚡" if resultado['es_contradiccion'] else "✅"
        print(f"  {simbolo} {par[0]:15s} ↔ {par[1]:15s}")
        print(f"     Similitud: {resultado['similitud']:.3f}")
        print(f"     Relación: {resultado['tipo_relacion']}")
        print(f"     Fuerza: {resultado['fuerza_relator']:.3f}")
        print()
    
    # Guardar resultados
    analisis = {
        "tarea_1_puentes": resultados_t1,
        "tarea_2_arquetipos": resultados_t2,
        "tarea_3_sintesis": resultados_t3,
        "tarea_4_contradicciones": resultados_t4,
        "metricas": {
            "puentes_exitosos": sum(1 for r in resultados_t1 if r['B'] is not None),
            "arquetipos_predichos": len(resultados_t2),
            "sintesis_exitosas": len(resultados_t3),
            "contradicciones_detectadas": sum(1 for r in resultados_t4 if r['es_contradiccion'])
        }
    }
    
    with open('paso3_razonamiento.json', 'w', encoding='utf-8') as f:
        json.dump(analisis, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*70)
    print("✅ Análisis guardado en: paso3_razonamiento.json")
    print("="*70)
    
    # Resumen
    print("\n🌌 RESUMEN:")
    print(f"  Tarea 1: {analisis['metricas']['puentes_exitosos']}/{len(resultados_t1)} puentes encontrados")
    print(f"  Tarea 2: {analisis['metricas']['arquetipos_predichos']} arquetipos predichos")
    print(f"  Tarea 3: {analisis['metricas']['sintesis_exitosas']} síntesis emergentes")
    print(f"  Tarea 4: {analisis['metricas']['contradicciones_detectadas']}/{len(resultados_t4)} contradicciones detectadas")
    
    # Interpretación
    print("\n💡 INTERPRETACIÓN:")
    
    if analisis['metricas']['puentes_exitosos'] >= len(resultados_t1) * 0.75:
        print("  ✅ Genesis puede RAZONAR sobre conexiones conceptuales")
    else:
        print("  ⚠️  Genesis necesita más relatores para inferir puentes")
    
    if analisis['metricas']['contradicciones_detectadas'] > 0:
        print("  ✅ Genesis detecta INCOMPATIBILIDADES estructurales")
    else:
        print("  ℹ️  Todos los conceptos son compatibles (red densa)")
    
    emergencias_fuertes = sum(1 for r in resultados_t3 if r['score_emergencia'] > 0.5)
    if emergencias_fuertes >= len(resultados_t3) * 0.5:
        print(f"  ✅ Genesis genera SÍNTESIS COHERENTES ({emergencias_fuertes}/{len(resultados_t3)} fuertes)")
    else:
        print(f"  ⚠️  Síntesis débiles (solo {emergencias_fuertes}/{len(resultados_t3)} > 0.5)")
    
    return analisis


if __name__ == "__main__":
    analisis = ejecutar_paso3()
