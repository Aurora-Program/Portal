"""
Análisis de Relatores - Genesis Autopoiesis
============================================

Investiga los 147 relatores descubiertos:
- ¿Qué tipos de transformación dominan? (analogía, causalidad, jerarquía)
- ¿Estructura de red: hubs, clusters, caminos críticos?
- ¿Propiedades fractales en las conexiones?
- ¿Qué arquetipos son más conectados?
"""

import json
from typing import Dict, List, Tuple
from collections import defaultdict, Counter
import numpy as np

from tensor_ffe import TensorFFE
from evolver import Evolver, Relator

def analizar_relatores():
    """
    Analiza los 147 relatores de la red autopoiética
    """
    print("🕸️  ANÁLISIS DE LOS 147 RELATORES")
    print("="*70)
    
    # Cargar resultados
    with open('genesis_autopoiesis_results.json', 'r', encoding='utf-8') as f:
        resultados = json.load(f)
    
    print(f"\n  Red descubierta:")
    print(f"    Nodos (arquetipos): {resultados['fase_6']['num_nodos']}")
    print(f"    Conexiones (relatores): {resultados['fase_6']['num_conexiones']}")
    
    # Densidad teórica
    nodos = resultados['fase_6']['num_nodos']
    max_conexiones = nodos * (nodos - 1)  # Grafo dirigido
    densidad = resultados['fase_6']['num_conexiones'] / max_conexiones
    print(f"    Densidad: {densidad:.1%} ({resultados['fase_6']['num_conexiones']}/{max_conexiones})")
    
    # Reconstruir red desde Evolver
    print("\n  Reconstruyendo red desde Evolver...")
    from sentence_transformers import SentenceTransformer
    from ffe_encoder_mcp import FFEEncoder
    
    model = SentenceTransformer('all-MiniLM-L6-v2')
    encoder = FFEEncoder(dimension_embedding=384)
    evolver = Evolver()
    
    # Re-aprender arquetipos (mismo vocabulario que autopoiesis)
    VOCABULARIO_GENESIS = {
        "continuum": ["fonetico", "lexico", "semantico", "teorico"],
        "fractal": ["fractal", "recursion", "jerarquia", "nivel"],
        "emergencia": ["emergencia", "sintesis", "transcender", "novedad"],
        "ffe": ["forma", "funcion", "estructura", "tensor"],
        "orden": ["orden", "primero", "segundo", "tercero"],
    }
    
    print("  Fase 1: Codificando vocabulario...")
    tensores_vocab = {}
    for palabras in VOCABULARIO_GENESIS.values():
        for palabra in palabras:
            emb = model.encode(palabra)
            tensor = encoder.encode(emb.tolist())
            arq = evolver.archetype_learner.detectar_o_crear(tensor)
            tensores_vocab[palabra] = tensor
    
    print(f"    ✅ {len(evolver.archetype_learner.arquetipos)} arquetipos")
    
    # Fase 2: Codificar frases
    FRASES_GENESIS = [
        "La estructura fractal tiene tres niveles jerarquicos",
        "Cada nivel refleja el patron del nivel anterior",
        "La recursion conecta dimension con dimension",
        "La sintesis emergente crea conocimiento nuevo",
        "Tres tensores se combinan en una emergencia",
        "La novedad surge de la transcendencia",
        "El orden de los elementos cambia el resultado",
        "La secuencia primera, segunda, tercera importa",
        "El camino determina la emergencia final",
        "Forma, funcion y estructura definen vectores",
        "Cada dimension tiene valores discretos",
        "El tensor integra vectores fractales",
    ]
    
    print("  Fase 2: Codificando frases...")
    tensores_frases = []
    for frase in FRASES_GENESIS:
        emb = model.encode(frase)
        tensor = encoder.encode(emb.tolist())
        tensores_frases.append(tensor)
    
    print(f"    ✅ {len(tensores_frases)} frases")
    
    # Fase 3: CONECTAR TODOS LOS ARQUETIPOS (crear red completa)
    print("  Fase 3: Construyendo red de relatores...")
    arquetipos = list(evolver.archetype_learner.arquetipos.values())
    
    # Conectar todos con todos (como hizo autopoiesis)
    for i, arq1 in enumerate(arquetipos):
        for arq2 in arquetipos:
            if arq1.id != arq2.id:
                evolver.relator_network.conectar(arq1, arq2, tipo="analogico")
    
    print(f"    ✅ {len(evolver.relator_network.relatores)} relatores creados\n")
    
    # Analizar relatores
    relatores = list(evolver.relator_network.relatores.values())
    arquetipos_dict = evolver.archetype_learner.arquetipos
    print(f"    ✅ {len(relatores)} relatores activos\n")
    
    # 1. TIPOS DE TRANSFORMACIÓN
    print("="*70)
    print("🔄 1. TIPOS DE TRANSFORMACIÓN")
    print("="*70)
    
    tipos_transformacion = Counter()
    intensidades = []
    
    for rel in relatores:
        # Obtener arquetipos desde IDs
        arq_A = arquetipos_dict.get(rel.origen)
        arq_B = arquetipos_dict.get(rel.destino)
        
        if not arq_A or not arq_B:
            continue
        
        # Clasificar por similitud de vectores FFE
        A = arq_A.tensor_prototipo
        B = arq_B.tensor_prototipo
        
        # Extraer dimensiones promedio
        def dims_promedio(tensor):
            return np.array([
                np.mean([v.forma for v in tensor.nivel_1]),
                np.mean([v.funcion for v in tensor.nivel_1]),
                np.mean([v.estructura for v in tensor.nivel_1])
            ])
        
        dims_A = dims_promedio(A)
        dims_B = dims_promedio(B)
        
        diff = dims_B - dims_A
        
        # Clasificar transformación
        if np.abs(diff[0]) > 1.5:  # Cambio en Forma
            tipos_transformacion['FORMA_SHIFT'] += 1
        if np.abs(diff[1]) > 1.5:  # Cambio en Función
            tipos_transformacion['FUNCION_SHIFT'] += 1
        if np.abs(diff[2]) > 1.5:  # Cambio en Estructura
            tipos_transformacion['ESTRUCTURA_SHIFT'] += 1
        
        # Similitud general (analogía vs causalidad)
        similitud = 1 - np.linalg.norm(diff) / np.sqrt(3 * 49)  # Normalizado
        intensidades.append(rel.fuerza)
        
        if similitud > 0.8:
            tipos_transformacion['ANALOGIA'] += 1  # A ≈ B
        elif similitud < 0.5:
            tipos_transformacion['OPOSICION'] += 1  # A ⊕ B
        else:
            tipos_transformacion['CAUSALIDAD'] += 1  # A → B
    
    print("\n  Distribución de transformaciones:")
    total = sum(tipos_transformacion.values())
    for tipo, count in tipos_transformacion.most_common():
        pct = 100 * count / len(relatores)
        print(f"    {tipo:20s}: {count:3d} relatores ({pct:5.1f}%)")
    
    print(f"\n  Fuerza promedio: {np.mean(intensidades):.3f} ± {np.std(intensidades):.3f}")
    
    # 2. ESTRUCTURA DE RED
    print("\n" + "="*70)
    print("🌐 2. ESTRUCTURA DE RED")
    print("="*70)
    
    # Grado de entrada/salida por arquetipo
    grado_salida = Counter()
    grado_entrada = Counter()
    
    for rel in relatores:
        grado_salida[rel.origen] += 1
        grado_entrada[rel.destino] += 1
    
    print("\n  Hubs (nodos más conectados):")
    print("    SALIDA (generadores):")
    for arq_id, count in grado_salida.most_common(3):
        print(f"      {arq_id}: {count} conexiones salientes")
    
    print("\n    ENTRADA (receptores):")
    for arq_id, count in grado_entrada.most_common(3):
        print(f"      {arq_id}: {count} conexiones entrantes")
    
    # 3. PROPIEDADES FRACTALES
    print("\n" + "="*70)
    print("📐 3. PROPIEDADES FRACTALES")
    print("="*70)
    
    # Distribución de grados (ley de potencias?)
    grados = list(grado_salida.values()) + list(grado_entrada.values())
    grados_unicos = sorted(set(grados))
    
    print("\n  Distribución de grados:")
    hist = Counter(grados)
    for grado in sorted(hist.keys()):
        count = hist[grado]
        bar = "█" * (count // 2)
        print(f"    Grado {grado:2d}: {count:2d} nodos {bar}")
    
    # Coeficiente de clustering (autosimilitud local)
    # Simplificado: ¿cuántos vecinos de A están conectados entre sí?
    clustering_local = []
    
    arquetipos_ids = list(set(grado_salida.keys()) | set(grado_entrada.keys()))
    
    for arq_id in arquetipos_ids:
        # Vecinos (salida)
        vecinos = [rel.destino for rel in relatores if rel.origen == arq_id]
        
        if len(vecinos) < 2:
            continue
        
        # Conexiones entre vecinos
        conexiones_vecinos = 0
        for i, v1 in enumerate(vecinos):
            for v2 in vecinos[i+1:]:
                # ¿Existe relator v1→v2 o v2→v1?
                existe = any(
                    (rel.origen == v1 and rel.destino == v2) or
                    (rel.origen == v2 and rel.destino == v1)
                    for rel in relatores
                )
                if existe:
                    conexiones_vecinos += 1
        
        # Clustering local
        max_conexiones = len(vecinos) * (len(vecinos) - 1) / 2
        if max_conexiones > 0:
            clustering = conexiones_vecinos / max_conexiones
            clustering_local.append(clustering)
    
    if clustering_local:
        print(f"\n  Clustering promedio: {np.mean(clustering_local):.3f}")
        print(f"    (0 = árbol, 1 = clique completo)")
        
        if np.mean(clustering_local) > 0.5:
            print(f"    ✅ Red densamente interconectada (estructura fractal)")
        else:
            print(f"    📊 Red moderadamente conectada")
    
    # 4. CAMINOS CRÍTICOS
    print("\n" + "="*70)
    print("🛤️  4. CAMINOS CRÍTICOS")
    print("="*70)
    
    # Encontrar caminos más fuertes
    caminos_fuertes = []
    
    for rel in relatores:
        # Buscar continuaciones (B → C)
        continuaciones = [
            r for r in relatores 
            if r.origen == rel.destino
        ]
        
        for cont in continuaciones[:3]:  # Top 3
            fuerza_camino = rel.fuerza * cont.fuerza
            caminos_fuertes.append({
                'camino': f"{rel.origen} → {rel.destino} → {cont.destino}",
                'fuerza': fuerza_camino
            })
    
    # Top 10 caminos
    caminos_fuertes.sort(key=lambda x: x['fuerza'], reverse=True)
    
    print("\n  Top 10 caminos más fuertes (A → B → C):")
    for i, camino in enumerate(caminos_fuertes[:10], 1):
        print(f"    {i:2d}. {camino['camino']:35s} (fuerza={camino['fuerza']:.4f})")
    
    # 5. ARQUETIPOS MÁS CONECTADOS
    print("\n" + "="*70)
    print("🎯 5. ARQUETIPOS MÁS CONECTADOS")
    print("="*70)
    
    # Conectividad total (entrada + salida)
    conectividad_total = Counter()
    for arq_id in arquetipos_ids:
        conectividad_total[arq_id] = grado_salida[arq_id] + grado_entrada[arq_id]
    
    print("\n  Ranking por conectividad total:")
    for i, (arq_id, total) in enumerate(conectividad_total.most_common(), 1):
        entrada = grado_entrada[arq_id]
        salida = grado_salida[arq_id]
        print(f"    {i}. {arq_id}: {total:3d} total (↓{salida:2d} salida, ↑{entrada:2d} entrada)")
    
    # Guardar análisis
    analisis = {
        "total_relatores": len(relatores),
        "densidad_red": float(densidad),
        "tipos_transformacion": dict(tipos_transformacion),
        "fuerza_promedio": float(np.mean(intensidades)) if intensidades else 0.0,
        "fuerza_std": float(np.std(intensidades)) if intensidades else 0.0,
        "clustering_promedio": float(np.mean(clustering_local)) if clustering_local else 0.0,
        "top_hubs": {
            "generadores": [
                {"id": arq_id, "grado": count}
                for arq_id, count in grado_salida.most_common(3)
            ],
            "receptores": [
                {"id": arq_id, "grado": count}
                for arq_id, count in grado_entrada.most_common(3)
            ]
        },
        "top_caminos": caminos_fuertes[:10],
        "conectividad_total": {
            arq_id: count for arq_id, count in conectividad_total.most_common()
        }
    }
    
    with open('analisis_relatores.json', 'w', encoding='utf-8') as f:
        json.dump(analisis, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*70)
    print("✅ Análisis guardado en: analisis_relatores.json")
    print("="*70)
    
    return analisis

if __name__ == "__main__":
    analisis = analizar_relatores()
    
    print("\n🌌 CONCLUSIÓN:")
    print(f"  Los {analisis['total_relatores']} relatores forman una red con:")
    print(f"    • Densidad: {analisis['densidad_red']:.1%} (máximo teórico)")
    print(f"    • Clustering: {analisis['clustering_promedio']:.1%} (autosimilitud local)")
    
    if analisis['clustering_promedio'] > 0.5:
        print(f"    ✅ Estructura FRACTAL confirmada (alta interconexión)")
    
    if analisis['tipos_transformacion']:
        domina = max(analisis['tipos_transformacion'].items(), key=lambda x: x[1])
        print(f"    • Transformación dominante: {domina[0]} ({domina[1]} relatores)")
    else:
        print(f"    ⚠️  No hay transformaciones para analizar")

