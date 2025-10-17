"""
Benchmark Downstream Tasks - Proyecto Genesis
==============================================

Valida si Genesis FFE puede operar en tareas reales:
- Clasificación de textos
- Búsqueda semántica (retrieval)
- Clustering
- Q&A simple

Si la pérdida semántica es 91%, ¿puede seguir siendo útil?
"""

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, adjusted_rand_score
import json
from datetime import datetime
from typing import List, Dict, Tuple
import argparse

# Imports locales
from ffe_encoder_mcp import FFEEncoder

# ============================================================================
# DATASETS DE PRUEBA (embedidos en código para portabilidad)
# ============================================================================

DATASET_CLASIFICACION = {
    "train": [
        ("El gato está sobre el tapete", "animal"),
        ("Los perros ladran en el parque", "animal"),
        ("El coche rojo acelera rápido", "vehiculo"),
        ("La moto cruza la ciudad", "vehiculo"),
        ("Python es un lenguaje de programación", "tecnologia"),
        ("JavaScript permite crear sitios web", "tecnologia"),
        ("Me encanta esta película", "entretenimiento"),
        ("La serie tiene 5 temporadas", "entretenimiento"),
    ],
    "test": [
        ("El pájaro vuela alto", "animal"),           # Similar a gato/perro
        ("El avión despega a las 8", "vehiculo"),     # Similar a coche/moto
        ("TypeScript mejora JavaScript", "tecnologia"), # Similar a Python/JS
        ("Voy al cine esta noche", "entretenimiento"), # Similar a película/serie
    ]
}

DATASET_RETRIEVAL = {
    "corpus": [
        "La capital de Francia es París",
        "El agua hierve a 100 grados Celsius",
        "Python fue creado por Guido van Rossum",
        "La fotosíntesis convierte luz en energía",
        "Einstein desarrolló la teoría de la relatividad",
        "El ADN contiene información genética",
        "Shakespeare escribió Romeo y Julieta",
        "La tierra gira alrededor del sol",
    ],
    "queries": [
        ("¿Cuál es la capital de Francia?", 0),  # Debería recuperar índice 0
        ("¿A qué temperatura hierve el agua?", 1),
        ("¿Quién creó Python?", 2),
        ("¿Qué es la fotosíntesis?", 3),
    ]
}

DATASET_CLUSTERING = [
    # Cluster 0: Animales
    "El gato maúlla", "El perro ladra", "El pájaro canta",
    # Cluster 1: Comida
    "La pizza es deliciosa", "El sushi es japonés", "Las hamburguesas son populares",
    # Cluster 2: Deportes
    "El fútbol es mundial", "El baloncesto tiene 5 jugadores", "El tenis usa raquetas",
]
CLUSTERING_LABELS = [0, 0, 0, 1, 1, 1, 2, 2, 2]

# ============================================================================
# BENCHMARK 1: CLASIFICACIÓN
# ============================================================================

def benchmark_clasificacion(
    encoder_genesis: FFEEncoder,
    model_baseline: SentenceTransformer
) -> Dict:
    """
    Entrena un clasificador simple (nearest centroid) y mide accuracy.
    """
    print("\n[1/4] 📊 Clasificación de Textos")
    print("="*60)
    
    train_texts = [t for t, _ in DATASET_CLASIFICACION["train"]]
    train_labels = [l for _, l in DATASET_CLASIFICACION["train"]]
    test_texts = [t for t, _ in DATASET_CLASIFICACION["test"]]
    test_labels = [l for _, l in DATASET_CLASIFICACION["test"]]
    
    # Crear mapeo de labels
    unique_labels = list(set(train_labels))
    label_to_idx = {l: i for i, l in enumerate(unique_labels)}
    
    # Calcular centroides (promedio por clase)
    def train_centroids(texts, labels, encode_fn):
        centroides = {}
        for label in unique_labels:
            indices = [i for i, l in enumerate(labels) if l == label]
            embeddings = [encode_fn(texts[i]) for i in indices]
            centroides[label] = np.mean(embeddings, axis=0)
        return centroides
    
    # Predecir (nearest centroid)
    def predict(text, centroides, encode_fn):
        embedding = encode_fn(text)
        distances = {
            label: np.linalg.norm(embedding - centroid)
            for label, centroid in centroides.items()
        }
        return min(distances, key=distances.get)
    
    # Genesis FFE
    encode_genesis = lambda t: encoder_genesis.encode_to_ffe(
        model_baseline.encode(t)
    ).to_ndarray()
    centroides_genesis = train_centroids(train_texts, train_labels, encode_genesis)
    pred_genesis = [predict(t, centroides_genesis, encode_genesis) for t in test_texts]
    acc_genesis = accuracy_score(test_labels, pred_genesis)
    
    # Baseline
    encode_baseline = lambda t: model_baseline.encode(t)
    centroides_baseline = train_centroids(train_texts, train_labels, encode_baseline)
    pred_baseline = [predict(t, centroides_baseline, encode_baseline) for t in test_texts]
    acc_baseline = accuracy_score(test_labels, pred_baseline)
    
    print(f"  Genesis FFE:  {acc_genesis:.1%} accuracy")
    print(f"  Baseline:     {acc_baseline:.1%} accuracy")
    print(f"  Diferencia:   {(acc_genesis - acc_baseline):.1%}")
    
    return {
        "nombre": "Clasificación (Nearest Centroid)",
        "metrica": "accuracy",
        "valor_genesis": float(acc_genesis),
        "valor_baseline": float(acc_baseline),
        "diferencia": float(acc_genesis - acc_baseline),
        "dataset": "4 clases, 8 train, 4 test",
        "predictions_genesis": list(pred_genesis),
        "predictions_baseline": list(pred_baseline),
    }

# ============================================================================
# BENCHMARK 2: BÚSQUEDA SEMÁNTICA (RETRIEVAL)
# ============================================================================

def benchmark_retrieval(
    encoder_genesis: FFEEncoder,
    model_baseline: SentenceTransformer
) -> Dict:
    """
    Mide si las queries recuperan los documentos correctos.
    Métrica: Recall@1 (¿el top-1 es correcto?)
    """
    print("\n[2/4] 🔍 Búsqueda Semántica (Retrieval)")
    print("="*60)
    
    corpus = DATASET_RETRIEVAL["corpus"]
    queries = DATASET_RETRIEVAL["queries"]
    
    # Codificar corpus
    corpus_baseline = model_baseline.encode(corpus)
    corpus_genesis = np.array([
        encoder_genesis.encode_to_ffe(emb).to_ndarray()
        for emb in corpus_baseline
    ])
    
    # Evaluar queries
    hits_genesis = 0
    hits_baseline = 0
    
    for query_text, expected_idx in queries:
        # Genesis
        query_emb_base = model_baseline.encode(query_text)
        query_genesis = encoder_genesis.encode_to_ffe(query_emb_base).to_ndarray()
        similarities_genesis = cosine_similarity([query_genesis], corpus_genesis)[0]
        top1_genesis = np.argmax(similarities_genesis)
        if top1_genesis == expected_idx:
            hits_genesis += 1
        
        # Baseline
        query_baseline = model_baseline.encode(query_text)
        similarities_baseline = cosine_similarity([query_baseline], corpus_baseline)[0]
        top1_baseline = np.argmax(similarities_baseline)
        if top1_baseline == expected_idx:
            hits_baseline += 1
    
    recall_genesis = hits_genesis / len(queries)
    recall_baseline = hits_baseline / len(queries)
    
    print(f"  Genesis FFE:  {recall_genesis:.1%} Recall@1")
    print(f"  Baseline:     {recall_baseline:.1%} Recall@1")
    print(f"  Hits:         {hits_genesis}/{len(queries)} vs {hits_baseline}/{len(queries)}")
    
    return {
        "nombre": "Retrieval (Recall@1)",
        "metrica": "recall_at_1",
        "valor_genesis": float(recall_genesis),
        "valor_baseline": float(recall_baseline),
        "diferencia": float(recall_genesis - recall_baseline),
        "dataset": f"{len(corpus)} docs, {len(queries)} queries",
        "hits_genesis": hits_genesis,
        "hits_baseline": hits_baseline,
    }

# ============================================================================
# BENCHMARK 3: CLUSTERING
# ============================================================================

def benchmark_clustering(
    encoder_genesis: FFEEncoder,
    model_baseline: SentenceTransformer
) -> Dict:
    """
    Agrupa textos y mide si los clusters descubiertos coinciden con las clases reales.
    Métrica: Adjusted Rand Index (ARI)
    """
    print("\n[3/4] 🎯 Clustering (K-Means)")
    print("="*60)
    
    texts = DATASET_CLUSTERING
    true_labels = CLUSTERING_LABELS
    n_clusters = 3
    
    # Codificar
    embeddings_baseline = model_baseline.encode(texts)
    embeddings_genesis = np.array([
        encoder_genesis.encode_to_ffe(emb).to_ndarray()
        for emb in embeddings_baseline
    ])
    
    # K-Means
    kmeans_genesis = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    pred_genesis = kmeans_genesis.fit_predict(embeddings_genesis)
    
    kmeans_baseline = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    pred_baseline = kmeans_baseline.fit_predict(embeddings_baseline)
    
    # Adjusted Rand Index (1.0 = perfecto, 0.0 = random)
    ari_genesis = adjusted_rand_score(true_labels, pred_genesis)
    ari_baseline = adjusted_rand_score(true_labels, pred_baseline)
    
    print(f"  Genesis FFE:  {ari_genesis:.3f} ARI")
    print(f"  Baseline:     {ari_baseline:.3f} ARI")
    print(f"  Diferencia:   {(ari_genesis - ari_baseline):.3f}")
    
    return {
        "nombre": "Clustering (K-Means)",
        "metrica": "adjusted_rand_index",
        "valor_genesis": float(ari_genesis),
        "valor_baseline": float(ari_baseline),
        "diferencia": float(ari_genesis - ari_baseline),
        "dataset": f"{len(texts)} textos, {n_clusters} clusters",
        "predictions_genesis": pred_genesis.tolist(),
        "predictions_baseline": pred_baseline.tolist(),
    }

# ============================================================================
# BENCHMARK 4: IMPACTO DE EMERGENCIA
# ============================================================================

def benchmark_emergencia_utilidad(
    encoder_genesis: FFEEncoder,
    model_baseline: SentenceTransformer
) -> Dict:
    """
    Hipótesis: La síntesis emergente (transcender) puede recuperar información
    que se perdió en la cuantización.
    
    Test: Sintetizar 3 conceptos relacionados y ver si la emergencia mejora
    la similitud semántica vs el promedio simple.
    """
    print("\n[4/4] 🌌 Utilidad de la Emergencia")
    print("="*60)
    
    from transcender import Transcender
    
    # Triadas semánticamente relacionadas
    triadas = [
        ("gato", "perro", "animal"),  # Los dos primeros deberían sintetizar el tercero
        ("París", "Francia", "capital"),
        ("Python", "programación", "código"),
    ]
    
    transcender = Transcender()
    mejoras = []
    
    for a, b, objetivo in triadas:
        # Codificar
        emb_a = model_baseline.encode(a)
        emb_b = model_baseline.encode(b)
        emb_obj = model_baseline.encode(objetivo)
        
        ffe_a = encoder_genesis.encode_to_ffe(emb_a)
        ffe_b = encoder_genesis.encode_to_ffe(emb_b)
        ffe_obj = encoder_genesis.encode_to_ffe(emb_obj)
        
        # Método 1: Promedio simple (sin emergencia)
        ffe_promedio_array = (ffe_a.to_ndarray() + ffe_b.to_ndarray()) / 2
        sim_promedio = cosine_similarity(
            [ffe_promedio_array],
            [ffe_obj.to_ndarray()]
        )[0][0]
        
        # Método 2: Síntesis emergente
        ffe_c = encoder_genesis.encode_to_ffe(model_baseline.encode("contexto"))  # Dummy
        emergencia = transcender.sintetizar(ffe_a, ffe_b, ffe_c)
        sim_emergencia = cosine_similarity(
            [emergencia.Ms.to_ndarray()],
            [ffe_obj.to_ndarray()]
        )[0][0]
        
        mejora = sim_emergencia - sim_promedio
        mejoras.append(mejora)
        
        print(f"  {a} + {b} → {objetivo}:")
        print(f"    Promedio:   {sim_promedio:.3f}")
        print(f"    Emergencia: {sim_emergencia:.3f} ({mejora:+.3f})")
    
    mejora_promedio = np.mean(mejoras)
    
    print(f"\n  Mejora promedio: {mejora_promedio:+.3f}")
    print(f"  {'✅ La emergencia aporta valor' if mejora_promedio > 0 else '⚠️ La emergencia no mejora'}")
    
    return {
        "nombre": "Utilidad de Emergencia",
        "metrica": "mejora_similitud",
        "valor_genesis": float(mejora_promedio),
        "valor_baseline": 0.0,  # Baseline no tiene emergencia
        "diferencia": float(mejora_promedio),
        "dataset": f"{len(triadas)} triadas",
        "detalle_triadas": [
            {"triada": f"{a}+{b}→{c}", "mejora": float(m)}
            for (a, b, c), m in zip(triadas, mejoras)
        ],
    }

# ============================================================================
# RUNNER PRINCIPAL
# ============================================================================

class DownstreamBenchmarkSuite:
    def __init__(self):
        print("🌌 Inicializando Proyecto Genesis - Downstream Benchmark")
        print("="*60)
        
        # Cargar modelos
        print("  Cargando sentence-transformer...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        print("  Inicializando FFE Encoder...")
        self.encoder = FFEEncoder(embedding_dim=384)  # MiniLM usa 384
        
        print("✅ Listo\n")
    
    def run_all(self) -> Dict:
        """Ejecuta todos los benchmarks downstream."""
        resultados = []
        
        # 1. Clasificación
        resultados.append(benchmark_clasificacion(self.encoder, self.model))
        
        # 2. Retrieval
        resultados.append(benchmark_retrieval(self.encoder, self.model))
        
        # 3. Clustering
        resultados.append(benchmark_clustering(self.encoder, self.model))
        
        # 4. Emergencia
        resultados.append(benchmark_emergencia_utilidad(self.encoder, self.model))
        
        # Resumen
        print("\n" + "="*60)
        print("📊 RESUMEN DOWNSTREAM")
        print("="*60)
        
        total_tasks = len(resultados)
        tasks_mejoradas = sum(1 for r in resultados if r.get("diferencia", 0) >= 0)
        
        print(f"\nTareas donde Genesis ≥ Baseline: {tasks_mejoradas}/{total_tasks}")
        
        for r in resultados:
            diff = r.get("diferencia", 0)
            emoji = "✅" if diff >= 0 else "⚠️"
            print(f"  {emoji} {r['nombre']}: {diff:+.3f}")
        
        # Veredicto
        print("\n" + "-"*60)
        if tasks_mejoradas >= total_tasks * 0.5:
            print("✅ VEREDICTO: Genesis FFE puede operar en tareas reales")
            print("   A pesar de la pérdida semántica, mantiene utilidad práctica.")
        else:
            print("⚠️ VEREDICTO: Genesis FFE necesita mejoras")
            print("   La pérdida semántica (91%) es demasiado alta para uso práctico.")
            print("   Sugerencia: Aumentar bits (9→12) o usar LoRA fine-tuning.")
        
        return {
            "version": "1.0.0",
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "tipo": "downstream_tasks",
            "resultados": resultados,
            "resumen": {
                "total_tareas": total_tasks,
                "tareas_exitosas": tasks_mejoradas,
                "tasa_exito": tasks_mejoradas / total_tasks,
            }
        }

# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Benchmark Downstream - Proyecto Genesis"
    )
    parser.add_argument(
        "--output",
        default="benchmark_downstream_results.json",
        help="Archivo de salida JSON"
    )
    
    args = parser.parse_args()
    
    # Ejecutar
    suite = DownstreamBenchmarkSuite()
    resultados = suite.run_all()
    
    # Guardar
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultados guardados en: {args.output}")

if __name__ == "__main__":
    main()
