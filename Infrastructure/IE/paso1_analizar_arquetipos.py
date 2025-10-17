"""
Análisis de Arquetipos - Genesis Autopoiesis
=============================================

Investiga los 8 arquetipos descubiertos:
- ¿Qué palabras comparten cada arquetipo?
- ¿Mapean a los 8 niveles del continuum?
- ¿Qué patrones universales representan?
"""

import json
from typing import Dict, List
from collections import defaultdict

from tensor_ffe import TensorFFE, VectorFFE
from evolver import Evolver

# Recargar resultados de autopoiesis
with open('genesis_autopoiesis_results.json', 'r', encoding='utf-8') as f:
    resultados = json.load(f)

# Vocabulario original
VOCABULARIO_GENESIS = {
    "continuum": ["fonetico", "lexico", "semantico", "teorico"],
    "fractal": ["fractal", "recursion", "jerarquia", "nivel"],
    "emergencia": ["emergencia", "sintesis", "transcender", "novedad"],
    "ffe": ["forma", "funcion", "estructura", "tensor"],
    "orden": ["orden", "primero", "segundo", "tercero"],
}

def analizar_arquetipos():
    """
    Reconstruye los arquetipos y analiza sus patrones
    """
    print("🎭 ANÁLISIS DE LOS 8 ARQUETIPOS")
    print("="*70)
    
    from sentence_transformers import SentenceTransformer
    from ffe_encoder_mcp import FFEEncoder
    
    # Cargar modelos
    print("\n  Cargando modelos...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    encoder = FFEEncoder(dimension_embedding=384)
    evolver = Evolver()
    
    # Reconstruir arquetipos
    print("  Reconstruyendo arquetipos desde vocabulario...\n")
    
    palabras_por_arquetipo = defaultdict(list)
    arquetipos_info = {}
    
    contador = 0
    for categoria, palabras in VOCABULARIO_GENESIS.items():
        print(f"\n  [{categoria.upper()}]")
        for palabra in palabras:
            contador += 1
            # Codificar
            embedding = model.encode(palabra)
            tensor_ffe = encoder.encode(embedding.tolist())
            
            # Detectar arquetipo
            arq = evolver.archetype_learner.detectar_o_crear(tensor_ffe)
            palabras_por_arquetipo[arq.id].append(palabra)
            
            if arq.id not in arquetipos_info:
                arquetipos_info[arq.id] = {
                    'prototipo': arq.tensor_prototipo,
                    'frecuencia': arq.frecuencia,
                    'nivel_abstraccion': arq.nivel_abstraccion,
                }
            
            print(f"    [{contador:2d}/20] {palabra:15s} → {arq.id} (freq={arq.frecuencia})")
    
    # Resumen por arquetipo
    print("\n" + "="*70)
    print("📊 RESUMEN DE ARQUETIPOS")
    print("="*70)
    
    for arq_id in sorted(palabras_por_arquetipo.keys()):
        palabras = palabras_por_arquetipo[arq_id]
        info = arquetipos_info[arq_id]
        prototipo = info['prototipo']
        
        print(f"\n🎯 {arq_id}")
        print(f"   Palabras ({len(palabras)}): {', '.join(palabras)}")
        print(f"   Frecuencia: {info['frecuencia']}")
        print(f"   Nivel abstracción: {info['nivel_abstraccion']}")
        print(f"   Prototipo FFE:")
        for i, v in enumerate(prototipo.nivel_1):
            print(f"     Vector[{i}]: forma={v.forma}, funcion={v.funcion}, estructura={v.estructura}")
        print(f"   Coherencia: {prototipo.coherencia():.3f}")
    
    # Análisis de patrones
    print("\n" + "="*70)
    print("🔬 ANÁLISIS DE PATRONES")
    print("="*70)
    
    # ¿Los arquetipos mapean a niveles del continuum?
    print("\n1. Mapeo a Niveles del Continuum (0-7):")
    niveles_continuum = {
        0: "Fonético", 1: "Silábico", 2: "Morfémico", 3: "Léxico",
        4: "Sintáctico", 5: "Semántico", 6: "Discursivo", 7: "Teórico"
    }
    
    for arq_id, palabras in sorted(palabras_por_arquetipo.items()):
        info = arquetipos_info[arq_id]
        nivel = info['nivel_abstraccion']
        print(f"   {arq_id} → Nivel {nivel} ({niveles_continuum[nivel]}): {palabras}")
    
    # ¿Qué dimensiones dominan en cada arquetipo?
    print("\n2. Dimensiones Dominantes por Arquetipo:")
    for arq_id in sorted(palabras_por_arquetipo.keys()):
        info = arquetipos_info[arq_id]
        prototipo = info['prototipo']
        
        # Promedios
        forma_avg = sum(v.forma for v in prototipo.nivel_1) / 3
        func_avg = sum(v.funcion for v in prototipo.nivel_1) / 3
        est_avg = sum(v.estructura for v in prototipo.nivel_1) / 3
        
        dominante = max([
            ('FORMA', forma_avg),
            ('FUNCION', func_avg),
            ('ESTRUCTURA', est_avg)
        ], key=lambda x: x[1])
        
        print(f"   {arq_id}: {dominante[0]} dominante (valor={dominante[1]:.1f})")
        print(f"      → F={forma_avg:.1f}, Fn={func_avg:.1f}, E={est_avg:.1f}")
    
    # ¿Hay arquetipos que agrupen categorías semánticas?
    print("\n3. Agrupación por Categoría Original:")
    for categoria, palabras_cat in VOCABULARIO_GENESIS.items():
        arquetipos_en_cat = set()
        for palabra in palabras_cat:
            for arq_id, palabras_arq in palabras_por_arquetipo.items():
                if palabra in palabras_arq:
                    arquetipos_en_cat.add(arq_id)
        
        print(f"   [{categoria}] → {len(arquetipos_en_cat)} arquetipos: {sorted(arquetipos_en_cat)}")
        
        if len(arquetipos_en_cat) == 1:
            print(f"      ✅ Categoría colapsó a UN arquetipo (coherencia perfecta)")
        elif len(arquetipos_en_cat) == len(palabras_cat):
            print(f"      ⚠️ Cada palabra es su propio arquetipo (sin agrupación)")
        else:
            print(f"      📊 Agrupación parcial")
    
    # Guardar análisis
    analisis = {
        "total_arquetipos": len(palabras_por_arquetipo),
        "palabras_por_arquetipo": {k: v for k, v in palabras_por_arquetipo.items()},
        "arquetipos_por_nivel": defaultdict(list),
    }
    
    for arq_id, info in arquetipos_info.items():
        nivel = info['nivel_abstraccion']
        analisis["arquetipos_por_nivel"][str(nivel)].append(arq_id)
    
    with open('analisis_arquetipos.json', 'w', encoding='utf-8') as f:
        json.dump(analisis, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*70)
    print("✅ Análisis guardado en: analisis_arquetipos.json")
    print("="*70)
    
    return analisis

if __name__ == "__main__":
    analisis = analizar_arquetipos()
    
    print("\n🌌 CONCLUSIÓN:")
    print(f"  Genesis descubrió {analisis['total_arquetipos']} patrones universales")
    print(f"  desde {sum(len(p) for p in VOCABULARIO_GENESIS.values())} palabras.")
    print(f"  Ratio de abstracción: {20 / analisis['total_arquetipos']:.1f}x")
