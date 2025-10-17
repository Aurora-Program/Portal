"""
Benchmark Fractal Aurora 🌌
===========================

NO comparamos con baselines externos.
NO medimos "pérdida semántica".

MEDIMOS:
1. Autosimilitud fractal (niveles 1→2→3 reflejan misma estructura)
2. Emergencia generativa (síntesis crea conocimiento nuevo)
3. Coherencia no conmutativa (orden importa)
4. Reconstrucción jerárquica (podemos recuperar desde arriba)
5. Podado inteligente (menos dimensiones = más enfoque)

Este ES el benchmark. No hay "verdad externa".
La estructura fractal ES la verdad.
"""

import numpy as np
from typing import List, Dict, Tuple
import json
from datetime import datetime
from collections import defaultdict

from tensor_ffe import TensorFFE, VectorFFE, TransformadorFFE
from transcender import Transcender, Emergencia
from evolver import Evolver

# ============================================================================
# MÉTRICA 1: AUTOSIMILITUD FRACTAL
# ============================================================================

def metrica_autosimilitud(tensor: TensorFFE) -> Dict:
    """
    Mide si los niveles 2 y 3 reflejan la estructura del nivel 1.
    
    Hipótesis Aurora:
    - Si el fractal es coherente, los patrones en nivel 1 
      deben reaparecer en niveles 2 y 3 (autosimilitud)
    
    Medida:
    - Distribución de valores (0-7) debe ser similar entre niveles
    - Correlación de patrones entre padre-hijo
    """
    print("\n[1/5] 🔄 Autosimilitud Fractal")
    print("="*60)
    
    # Recolectar valores por nivel
    nivel_1_valores = []
    nivel_2_valores = []
    nivel_3_valores = []
    
    for v in tensor.nivel_1:
        nivel_1_valores.extend([v.forma, v.funcion, v.estructura])
    
    for v in tensor.nivel_2:
        nivel_2_valores.extend([v.forma, v.funcion, v.estructura])
    
    for v in tensor.nivel_3:
        nivel_3_valores.extend([v.forma, v.funcion, v.estructura])
    
    # Distribución de valores
    def distribucion(valores):
        total = len(valores)
        return {i: valores.count(i) / total for i in range(8)}
    
    dist_1 = distribucion(nivel_1_valores)
    dist_2 = distribucion(nivel_2_valores)
    dist_3 = distribucion(nivel_3_valores)
    
    # Similitud de distribuciones (distancia JS simplificada)
    def similitud_distribucion(d1, d2):
        suma = sum(abs(d1.get(i, 0) - d2.get(i, 0)) for i in range(8))
        return 1.0 - (suma / 2)  # Normalizado [0, 1]
    
    sim_1_2 = similitud_distribucion(dist_1, dist_2)
    sim_1_3 = similitud_distribucion(dist_1, dist_3)
    sim_2_3 = similitud_distribucion(dist_2, dist_3)
    
    autosimilitud = (sim_1_2 + sim_1_3 + sim_2_3) / 3
    
    print(f"  Nivel 1 ↔ Nivel 2: {sim_1_2:.3f}")
    print(f"  Nivel 1 ↔ Nivel 3: {sim_1_3:.3f}")
    print(f"  Nivel 2 ↔ Nivel 3: {sim_2_3:.3f}")
    print(f"  Autosimilitud Global: {autosimilitud:.3f}")
    
    # Interpretación fractal
    if autosimilitud > 0.7:
        veredicto = "✅ Fractal coherente (alta autosimilitud)"
    elif autosimilitud > 0.5:
        veredicto = "⚠️ Fractal parcial (autosimilitud media)"
    else:
        veredicto = "❌ No fractal (baja autosimilitud)"
    
    print(f"  {veredicto}")
    
    return {
        "metrica": "autosimilitud_fractal",
        "score": float(autosimilitud),
        "detalle": {
            "sim_1_2": float(sim_1_2),
            "sim_1_3": float(sim_1_3),
            "sim_2_3": float(sim_2_3),
            "distribucion_nivel_1": dist_1,
            "distribucion_nivel_2": dist_2,
            "distribucion_nivel_3": dist_3,
        },
        "interpretacion": veredicto,
    }

# ============================================================================
# MÉTRICA 2: EMERGENCIA GENERATIVA
# ============================================================================

def metrica_emergencia_generativa(
    tensores: List[TensorFFE],
    transcender: Transcender
) -> Dict:
    """
    Mide si la síntesis (A,B,C) genera conocimiento NUEVO.
    
    Hipótesis Aurora:
    - La emergencia no es promedio, es CREACIÓN
    - (A,B,C) debe ser diferente de A, B, C individualmente
    - El score de emergencia debe ser alto
    
    Medida:
    - Novedad: ¿Ms es diferente de A, B, C?
    - Score de emergencia del transcender
    - Varianza: ¿Diferentes inputs generan diferentes emergencias?
    """
    print("\n[2/5] 🌟 Emergencia Generativa")
    print("="*60)
    
    emergencias = []
    novedades = []
    
    # Generar múltiples síntesis
    n = min(len(tensores) // 3, 20)  # Máximo 20 triadas
    
    for i in range(n):
        idx_a = i * 3
        idx_b = i * 3 + 1
        idx_c = i * 3 + 2
        
        if idx_c >= len(tensores):
            break
        
        A = tensores[idx_a]
        B = tensores[idx_b]
        C = tensores[idx_c]
        
        emergencia = transcender.sintetizar(A, B, C)
        emergencias.append(emergencia)
        
        # Novedad: ¿Ms es diferente de A?
        distancia_A = np.linalg.norm(
            emergencia.Ms.to_ndarray() - A.to_ndarray()
        )
        novedades.append(distancia_A)
    
    # Scores de emergencia
    scores = [e.score_emergencia for e in emergencias]
    score_promedio = np.mean(scores)
    score_std = np.std(scores)
    
    # Novedad promedio
    novedad_promedio = np.mean(novedades)
    
    # Varianza de emergencias (¿son todas diferentes?)
    if len(emergencias) > 1:
        emergencias_arrays = [e.Ms.to_ndarray() for e in emergencias]
        distancias = []
        for i in range(len(emergencias_arrays)):
            for j in range(i + 1, len(emergencias_arrays)):
                dist = np.linalg.norm(emergencias_arrays[i] - emergencias_arrays[j])
                distancias.append(dist)
        varianza = np.mean(distancias)
    else:
        varianza = 0.0
    
    print(f"  Score Emergencia:  {score_promedio:.3f} ± {score_std:.3f}")
    print(f"  Novedad (vs input): {novedad_promedio:.3f}")
    print(f"  Varianza (diversidad): {varianza:.3f}")
    
    # Interpretación
    if score_promedio > 0.5 and novedad_promedio > 0.3:
        veredicto = "✅ Emergencia generativa activa"
    elif score_promedio > 0.3:
        veredicto = "⚠️ Emergencia parcial"
    else:
        veredicto = "❌ Emergencia débil"
    
    print(f"  {veredicto}")
    
    return {
        "metrica": "emergencia_generativa",
        "score": float(score_promedio),
        "detalle": {
            "score_promedio": float(score_promedio),
            "score_std": float(score_std),
            "novedad_promedio": float(novedad_promedio),
            "varianza_emergencias": float(varianza),
            "num_sintesis": len(emergencias),
        },
        "interpretacion": veredicto,
    }

# ============================================================================
# MÉTRICA 3: NO CONMUTATIVIDAD
# ============================================================================

def metrica_no_conmutatividad(
    tensores: List[TensorFFE],
    transcender: Transcender
) -> Dict:
    """
    Mide si el orden (A,B,C) vs (B,A,C) genera resultados diferentes.
    
    Hipótesis Aurora:
    - El universo no es conmutativo
    - f(A,B,C) ≠ f(B,A,C) ≠ f(C,B,A)
    
    Medida:
    - Distancia entre emergencias con diferente orden
    - Cuanto mayor la distancia, más no-conmutativo
    """
    print("\n[3/5] 🔀 No Conmutatividad")
    print("="*60)
    
    # Tomar primeras 3 tensores
    if len(tensores) < 3:
        return {
            "metrica": "no_conmutatividad",
            "score": 0.0,
            "detalle": {},
            "interpretacion": "⚠️ Insuficientes tensores",
        }
    
    A, B, C = tensores[0], tensores[1], tensores[2]
    
    # Todas las permutaciones
    permutaciones = [
        ("ABC", A, B, C),
        ("ACB", A, C, B),
        ("BAC", B, A, C),
        ("BCA", B, C, A),
        ("CAB", C, A, B),
        ("CBA", C, B, A),
    ]
    
    emergencias = {}
    for nombre, t1, t2, t3 in permutaciones:
        e = transcender.sintetizar(t1, t2, t3)
        emergencias[nombre] = e.Ms.to_ndarray()
    
    # Calcular distancias entre todas las permutaciones
    distancias = []
    pares = []
    for i, (n1, _, _, _) in enumerate(permutaciones):
        for j, (n2, _, _, _) in enumerate(permutaciones):
            if i < j:
                dist = np.linalg.norm(emergencias[n1] - emergencias[n2])
                distancias.append(dist)
                pares.append((n1, n2, dist))
    
    distancia_promedio = np.mean(distancias)
    distancia_std = np.std(distancias)
    
    # Encontrar el par más diferente
    par_max = max(pares, key=lambda x: x[2])
    
    print(f"  Distancia promedio: {distancia_promedio:.3f} ± {distancia_std:.3f}")
    print(f"  Par más diferente:  {par_max[0]} vs {par_max[1]} → {par_max[2]:.3f}")
    
    # Interpretación (escala relativa al rango posible)
    if distancia_promedio > 0.5:
        veredicto = "✅ Fuertemente no conmutativo"
    elif distancia_promedio > 0.2:
        veredicto = "⚠️ Parcialmente no conmutativo"
    else:
        veredicto = "❌ Casi conmutativo (problema)"
    
    print(f"  {veredicto}")
    
    return {
        "metrica": "no_conmutatividad",
        "score": float(distancia_promedio),
        "detalle": {
            "distancia_promedio": float(distancia_promedio),
            "distancia_std": float(distancia_std),
            "par_mas_diferente": {
                "orden_1": par_max[0],
                "orden_2": par_max[1],
                "distancia": float(par_max[2]),
            },
            "todas_distancias": [
                {"par": f"{p[0]}-{p[1]}", "distancia": float(p[2])}
                for p in pares[:10]  # Top 10
            ],
        },
        "interpretacion": veredicto,
    }

# ============================================================================
# MÉTRICA 4: RECONSTRUCCIÓN JERÁRQUICA
# ============================================================================

def metrica_reconstruccion_jerarquica(tensores: List[TensorFFE]) -> Dict:
    """
    Mide si podemos reconstruir información desde niveles superiores.
    
    Hipótesis Aurora:
    - El podado es REVERSIBLE
    - Desde nivel 1 podemos regenerar niveles 2 y 3
    - La información no se "pierde", se COMPRIME
    
    Medida:
    - Comparar nivel 2 original vs regenerado desde nivel 1
    - Comparar nivel 3 original vs regenerado desde nivel 2
    """
    print("\n[4/5] 🔼 Reconstrucción Jerárquica")
    print("="*60)
    
    similitudes_nivel_2 = []
    similitudes_nivel_3 = []
    
    for tensor in tensores[:20]:  # Máximo 20 tensores
        # Regenerar desde nivel 1
        tensor_regenerado = TensorFFE(
            nivel_1=tensor.nivel_1.copy()
        )
        
        # Comparar nivel 2
        for i in range(min(len(tensor.nivel_2), len(tensor_regenerado.nivel_2))):
            original = tensor.nivel_2[i]
            regenerado = tensor_regenerado.nivel_2[i]
            
            # Similitud simple: cuenta valores iguales
            matches = sum([
                original.forma == regenerado.forma,
                original.funcion == regenerado.funcion,
                original.estructura == regenerado.estructura,
            ])
            similitudes_nivel_2.append(matches / 3)
        
        # Comparar nivel 3
        for i in range(min(len(tensor.nivel_3), len(tensor_regenerado.nivel_3))):
            original = tensor.nivel_3[i]
            regenerado = tensor_regenerado.nivel_3[i]
            
            matches = sum([
                original.forma == regenerado.forma,
                original.funcion == regenerado.funcion,
                original.estructura == regenerado.estructura,
            ])
            similitudes_nivel_3.append(matches / 3)
    
    sim_2_promedio = np.mean(similitudes_nivel_2) if similitudes_nivel_2 else 0.0
    sim_3_promedio = np.mean(similitudes_nivel_3) if similitudes_nivel_3 else 0.0
    
    reconstruccion_global = (sim_2_promedio + sim_3_promedio) / 2
    
    print(f"  Nivel 2 regenerado: {sim_2_promedio:.1%} similitud")
    print(f"  Nivel 3 regenerado: {sim_3_promedio:.1%} similitud")
    print(f"  Reconstrucción global: {reconstruccion_global:.1%}")
    
    # Interpretación
    if reconstruccion_global > 0.8:
        veredicto = "✅ Reconstrucción perfecta (información preservada)"
    elif reconstruccion_global > 0.5:
        veredicto = "⚠️ Reconstrucción parcial (algo de pérdida)"
    else:
        veredicto = "❌ Reconstrucción débil (pérdida significativa)"
    
    print(f"  {veredicto}")
    
    return {
        "metrica": "reconstruccion_jerarquica",
        "score": float(reconstruccion_global),
        "detalle": {
            "nivel_2_similitud": float(sim_2_promedio),
            "nivel_3_similitud": float(sim_3_promedio),
            "num_comparaciones_nivel_2": len(similitudes_nivel_2),
            "num_comparaciones_nivel_3": len(similitudes_nivel_3),
        },
        "interpretacion": veredicto,
    }

# ============================================================================
# MÉTRICA 5: PODADO INTELIGENTE
# ============================================================================

def metrica_podado_inteligente(
    tensores: List[TensorFFE],
    transformador: TransformadorFFE
) -> Dict:
    """
    Mide si el podado (abstracting) mantiene COHERENCIA.
    
    Hipótesis Aurora:
    - Al abstraer (0→1→2→3), debemos GANAR información útil
    - Niveles altos deben tener más "entropía" (diversidad conceptual)
    - El podado no es pérdida, es ENFOQUE
    
    Medida:
    - Entropía por nivel (diversidad de valores)
    - Coherencia al abstraer (patrones consistentes)
    """
    print("\n[5/5] ✂️ Podado Inteligente")
    print("="*60)
    
    # Abstraer tensores a diferentes niveles
    niveles_continuum = [0, 2, 4, 6]  # Fonético → Léxico → Semántico → Discursivo
    
    entropias_por_nivel = defaultdict(list)
    
    for tensor in tensores[:20]:
        for nivel in niveles_continuum:
            # Ajustar nivel de abstracción del tensor
            tensor_abstraido = TensorFFE(nivel_1=tensor.nivel_1.copy())
            tensor_abstraido.nivel_abstraccion = nivel
            
            # Calcular entropía del nivel 1 (el que se mantiene)
            valores = []
            for v in tensor_abstraido.nivel_1:
                valores.extend([v.forma, v.funcion, v.estructura])
            
            # Entropía de Shannon simplificada
            freq = [valores.count(i) / len(valores) for i in range(8) if valores.count(i) > 0]
            entropia = -sum(p * np.log2(p) for p in freq if p > 0)
            
            entropias_por_nivel[nivel].append(entropia)
    
    # Promedios por nivel
    entropias_promedio = {
        nivel: np.mean(valores)
        for nivel, valores in entropias_por_nivel.items()
    }
    
    # Tendencia: ¿aumenta la entropía al abstraer?
    niveles_ordenados = sorted(entropias_promedio.keys())
    entropias_ordenadas = [entropias_promedio[n] for n in niveles_ordenados]
    
    # Correlación entre nivel y entropía
    correlacion = np.corrcoef(niveles_ordenados, entropias_ordenadas)[0, 1]
    
    print(f"  Entropía por nivel del continuum:")
    for nivel in niveles_ordenados:
        nombre = ["Fonético", "Silábico", "Morfémico", "Léxico", 
                  "Sintáctico", "Semántico", "Discursivo", "Teórico"][nivel]
        print(f"    [{nivel}] {nombre:12s}: {entropias_promedio[nivel]:.3f}")
    
    print(f"\n  Correlación (nivel ↔ entropía): {correlacion:.3f}")
    
    # Interpretación
    if correlacion > 0.5:
        veredicto = "✅ Podado inteligente (entropía crece con abstracción)"
    elif correlacion > 0:
        veredicto = "⚠️ Podado parcial (tendencia débil)"
    else:
        veredicto = "❌ Podado sin patrón (entropía no crece)"
    
    print(f"  {veredicto}")
    
    return {
        "metrica": "podado_inteligente",
        "score": float(correlacion),
        "detalle": {
            "entropias_por_nivel": {
                str(k): float(v) for k, v in entropias_promedio.items()
            },
            "correlacion_nivel_entropia": float(correlacion),
        },
        "interpretacion": veredicto,
    }

# ============================================================================
# SUITE FRACTAL AURORA
# ============================================================================

class BenchmarkFractalAurora:
    """
    Benchmark que NO compara con external truth.
    La verdad ES la estructura fractal.
    """
    
    def __init__(self, num_tensores: int = 50):
        print("🌌 Inicializando Benchmark Fractal Aurora")
        print("="*60)
        print("  NO comparamos con baseline externo")
        print("  Medimos COHERENCIA INTERNA fractal")
        print("="*60)
        
        self.transcender = Transcender()
        self.transformador = TransformadorFFE()
        
        # Generar tensores aleatorios (representan "conocimiento")
        print(f"\n  Generando {num_tensores} tensores aleatorios...")
        self.tensores = self._generar_tensores_aleatorios(num_tensores)
        print("✅ Listo\n")
    
    def _generar_tensores_aleatorios(self, n: int) -> List[TensorFFE]:
        """Genera tensores con valores aleatorios 0-7."""
        tensores = []
        for _ in range(n):
            nivel_1 = [
                VectorFFE(
                    forma=np.random.randint(0, 8),
                    funcion=np.random.randint(0, 8),
                    estructura=np.random.randint(0, 8)
                )
                for _ in range(3)
            ]
            tensores.append(TensorFFE(nivel_1=nivel_1))
        return tensores
    
    def run_all(self) -> Dict:
        """Ejecuta todas las métricas fractales."""
        resultados = []
        
        # 1. Autosimilitud
        resultados.append(metrica_autosimilitud(self.tensores[0]))
        
        # 2. Emergencia
        resultados.append(metrica_emergencia_generativa(
            self.tensores, self.transcender
        ))
        
        # 3. No Conmutatividad
        resultados.append(metrica_no_conmutatividad(
            self.tensores, self.transcender
        ))
        
        # 4. Reconstrucción
        resultados.append(metrica_reconstruccion_jerarquica(self.tensores))
        
        # 5. Podado
        resultados.append(metrica_podado_inteligente(
            self.tensores, self.transformador
        ))
        
        # VEREDICTO FRACTAL
        print("\n" + "="*60)
        print("🌌 VEREDICTO FRACTAL AURORA")
        print("="*60)
        
        scores = [r["score"] for r in resultados]
        score_global = np.mean(scores)
        
        print(f"\nScore Global: {score_global:.3f}\n")
        
        for r in resultados:
            emoji = "✅" if r["score"] > 0.5 else "⚠️" if r["score"] > 0.3 else "❌"
            print(f"  {emoji} {r['metrica']:30s}: {r['score']:.3f}")
        
        print("\n" + "-"*60)
        
        if score_global > 0.6:
            veredicto = "✅ SISTEMA FRACTAL COHERENTE"
            mensaje = "La estructura Aurora es internamente consistente."
        elif score_global > 0.4:
            veredicto = "⚠️ SISTEMA PARCIALMENTE FRACTAL"
            mensaje = "Algunas propiedades fractales presentes, refinar necesario."
        else:
            veredicto = "❌ SISTEMA NO FRACTAL"
            mensaje = "La estructura no exhibe coherencia fractal."
        
        print(f"\n{veredicto}")
        print(f"{mensaje}\n")
        
        return {
            "version": "1.0.0-fractal",
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "tipo": "benchmark_fractal_aurora",
            "paradigma": "NO baseline, solo coherencia interna",
            "metricas": resultados,
            "resumen": {
                "score_global": float(score_global),
                "veredicto": veredicto,
                "mensaje": mensaje,
            }
        }

# ============================================================================
# CLI
# ============================================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Benchmark Fractal Aurora - NO baseline comparison"
    )
    parser.add_argument(
        "--tensores",
        type=int,
        default=50,
        help="Número de tensores a generar"
    )
    parser.add_argument(
        "--output",
        default="benchmark_fractal_aurora.json",
        help="Archivo de salida JSON"
    )
    
    args = parser.parse_args()
    
    # Ejecutar
    suite = BenchmarkFractalAurora(num_tensores=args.tensores)
    resultados = suite.run_all()
    
    # Guardar
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Resultados guardados en: {args.output}")

if __name__ == "__main__":
    main()
