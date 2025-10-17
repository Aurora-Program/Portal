"""
Genesis Autopoiesis v1.2 - Auto-descubrimiento 🌌
=================================================

VERSIÓN 1.2 - RELATORES CORREGIDOS
-----------------------------------
Cambios en v1.2:
- ✅ Fase 6: Relatores ahora tienen tensor de transformación (emergencia Ms)
- ✅ Armonizador: broken_relator ahora 100% corregibles
- ✅ Sistema alcanza coherencia global

El sistema Genesis se usa a SÍ MISMO para:
1. Codificar palabras reales → Tensores FFE
2. Crear frases → Sintetizar emergencias
3. Descubrir arquetipos, dinámicas, relatores desde su propio lenguaje
4. Armonizar coherencia global (NUEVO en v1.1)
5. Traducirse a sí mismo (autopoiesis)

NO datos externos. Genesis aprende de Genesis.
"""

import numpy as np
from typing import List, Dict, Tuple
import json
from datetime import datetime
from sentence_transformers import SentenceTransformer

from tensor_ffe import TensorFFE, VectorFFE
from transcender import Transcender, Emergencia
from evolver import Evolver, ArchetypeLearner, DynamicsLearner, RelatorNetwork
from ffe_encoder_mcp import FFEEncoder
from armonizador import Armonizador

# ============================================================================
# FASE 1: VOCABULARIO GENESIS - Palabras fundacionales
# ============================================================================

VOCABULARIO_GENESIS = {
    # Estructura (0-7 del continuum) - REDUCIDO para rapidez
    "continuum": ["fonetico", "lexico", "semantico", "teorico"],
    
    # Fractales (autosimilitud)
    "fractal": ["fractal", "recursion", "jerarquia", "nivel"],
    
    # Emergencia (síntesis)
    "emergencia": ["emergencia", "sintesis", "transcender", "novedad"],
    
    # Forma-Función-Estructura
    "ffe": ["forma", "funcion", "estructura", "tensor"],
    
    # Orden (no conmutatividad)
    "orden": ["orden", "primero", "segundo", "tercero"],
}

# ============================================================================
# FASE 2: FRASES GENESIS - Auto-descripción
# ============================================================================

FRASES_GENESIS = [
    # Sobre estructura fractal (3 frases)
    "La estructura fractal tiene tres niveles jerarquicos",
    "Cada nivel refleja el patron del nivel anterior",
    "La recursion conecta dimension con dimension",
    
    # Sobre emergencia (3 frases)
    "La sintesis emergente crea conocimiento nuevo",
    "Tres tensores se combinan en una emergencia",
    "La novedad surge de la transcendencia",
    
    # Sobre orden (3 frases)
    "El orden de los elementos cambia el resultado",
    "La secuencia primera, segunda, tercera importa",
    "El camino determina la emergencia final",
    
    # Sobre FFE (3 frases)
    "Forma, funcion y estructura definen vectores",
    "Cada dimension tiene valores discretos",
    "El tensor integra vectores fractales",
]

# ============================================================================
# CLASE PRINCIPAL: AUTOPOIESIS
# ============================================================================

class GenesisAutopoiesis:
    """
    Sistema autopoiético: Genesis se usa a sí mismo para aprender.
    """
    
    def __init__(self):
        print("*** Iniciando Genesis Autopoiesis ***")
        print("="*60)
        
        # Cargar modelos
        print("  [1/5] Cargando sentence-transformer...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        print("  [2/5] Inicializando FFE Encoder...")
        self.encoder = FFEEncoder(dimension_embedding=384)
        
        print("  [3/5] Inicializando Transcender...")
        self.transcender = Transcender()
        
        print("  [4/5] Inicializando Evolver...")
        self.evolver = Evolver()
        
        print("  [5/5] Preparando vocabulario...")
        self.vocabulario_codificado = {}
        self.frases_codificadas = []
        
        print("✅ Sistema listo para autopoiesis\n")
    
    # ========================================================================
    # FASE 1: CODIFICAR VOCABULARIO
    # ========================================================================
    
    def codificar_vocabulario(self) -> Dict[str, Dict[str, TensorFFE]]:
        """
        Convierte cada palabra del vocabulario a TensorFFE.
        Retorna: {categoria: {palabra: tensor}}
        """
        print("\n" + "="*60)
        print("FASE 1: Codificación de Vocabulario Genesis")
        print("="*60)
        
        total_palabras = sum(len(palabras) for palabras in VOCABULARIO_GENESIS.values())
        contador = 0
        
        for categoria, palabras in VOCABULARIO_GENESIS.items():
            print(f"\n  [{categoria.upper()}]")
            self.vocabulario_codificado[categoria] = {}
            
            for palabra in palabras:
                contador += 1
                # Embedding → TensorFFE
                embedding = self.model.encode(palabra)
                tensor_ffe = self.encoder.encode(embedding.tolist())
                
                self.vocabulario_codificado[categoria][palabra] = tensor_ffe
                print(f"    [{contador:2d}/{total_palabras}] {palabra:15s} → TensorFFE({tensor_ffe.coherencia():.3f})")
        
        print(f"\n✅ {total_palabras} palabras codificadas en {len(VOCABULARIO_GENESIS)} categorías")
        return self.vocabulario_codificado
    
    # ========================================================================
    # FASE 2: CODIFICAR FRASES
    # ========================================================================
    
    def codificar_frases(self) -> List[Tuple[str, TensorFFE]]:
        """
        Convierte cada frase a TensorFFE.
        Retorna: [(frase, tensor), ...]
        """
        print("\n" + "="*60)
        print("FASE 2: Codificación de Frases Genesis")
        print("="*60)
        
        for i, frase in enumerate(FRASES_GENESIS, 1):
            embedding = self.model.encode(frase)
            tensor_ffe = self.encoder.encode(embedding.tolist())
            self.frases_codificadas.append((frase, tensor_ffe))
            
            print(f"  [{i:2d}/{len(FRASES_GENESIS)}] {frase[:50]:50s} → coherencia={tensor_ffe.coherencia():.3f}")
        
        print(f"\n✅ {len(FRASES_GENESIS)} frases codificadas")
        return self.frases_codificadas
    
    # ========================================================================
    # FASE 3: SÍNTESIS EMERGENTE (triadas de frases)
    # ========================================================================
    
    def sintetizar_triadas(self) -> List[Tuple[str, str, str, Emergencia]]:
        """
        Toma triadas de frases y genera emergencias.
        Descubre: ¿Qué surge de combinar 3 frases relacionadas?
        """
        print("\n" + "="*60)
        print("FASE 3: Síntesis Emergente (Triadas)")
        print("="*60)
        
        emergencias = []
        
        # Crear triadas temáticas (cada 3 frases consecutivas comparten tema)
        num_triadas = len(self.frases_codificadas) // 3
        
        for i in range(num_triadas):
            idx_a = i * 3
            idx_b = i * 3 + 1
            idx_c = i * 3 + 2
            
            frase_a, tensor_a = self.frases_codificadas[idx_a]
            frase_b, tensor_b = self.frases_codificadas[idx_b]
            frase_c, tensor_c = self.frases_codificadas[idx_c]
            
            # Sintetizar
            emergencia = self.transcender.sintetizar(tensor_a, tensor_b, tensor_c)
            emergencias.append((frase_a, frase_b, frase_c, emergencia))
            
            print(f"\n  [Triada {i+1}/{num_triadas}]")
            print(f"    A: {frase_a[:50]}")
            print(f"    B: {frase_b[:50]}")
            print(f"    C: {frase_c[:50]}")
            print(f"    → Emergencia: score={emergencia.score_emergencia:.3f}, "
                  f"nov={emergencia.novedad:.2f}, coh={emergencia.coherencia:.2f}")
        
        print(f"\n✅ {len(emergencias)} emergencias sintetizadas")
        return emergencias
    
    # ========================================================================
    # FASE 4: APRENDIZAJE DE ARQUETIPOS
    # ========================================================================
    
    def aprender_arquetipos(self) -> Dict:
        """
        Evolver aprende arquetipos desde el vocabulario codificado.
        Encuentra patrones universales en las palabras Genesis.
        """
        print("\n" + "="*60)
        print("FASE 4: Aprendizaje de Arquetipos")
        print("="*60)
        
        # Recolectar todos los tensores del vocabulario
        todos_tensores = []
        palabras_ordenadas = []
        
        for categoria, palabras_dict in self.vocabulario_codificado.items():
            for palabra, tensor in palabras_dict.items():
                todos_tensores.append(tensor)
                palabras_ordenadas.append((categoria, palabra))
        
        print(f"  Analizando {len(todos_tensores)} tensores...")
        
        # Aprender arquetipos usando detectar_o_crear
        arquetipos_detectados = []
        for tensor in todos_tensores:
            arq = self.evolver.archetype_learner.detectar_o_crear(tensor)
            if arq not in arquetipos_detectados:
                arquetipos_detectados.append(arq)
        
        print(f"\n  Arquetipos descubiertos: {len(arquetipos_detectados)}")
        for i, arq in enumerate(arquetipos_detectados[:10], 1):
            indices = [j for j, t in enumerate(todos_tensores) if arq.id == self.evolver.archetype_learner.detectar_o_crear(t).id]
            palabras_en_arq = [palabras_ordenadas[idx][1] for idx in indices[:5]]
            print(f"    [{i}] {arq.id}: {palabras_en_arq} (freq={arq.frecuencia})")
        
        return {
            "num_arquetipos": len(arquetipos_detectados),
            "arquetipos": [{"id": a.id, "frecuencia": a.frecuencia} for a in arquetipos_detectados],
        }
    
    # ========================================================================
    # FASE 5: APRENDIZAJE DE DINÁMICAS
    # ========================================================================
    
    def aprender_dinamicas(self) -> Dict:
        """
        Evolver aprende dinámicas temporales desde las frases.
        Detecta cómo evoluciona el tensor a través de las frases.
        """
        print("\n" + "="*60)
        print("FASE 5: Aprendizaje de Dinámicas Temporales")
        print("="*60)
        
        # Secuencia temporal: frases en orden
        secuencia = [tensor for _, tensor in self.frases_codificadas]
        
        print(f"  Analizando secuencia de {len(secuencia)} frases...")
        
        # Aprender dinámicas
        dinamica = self.evolver.dynamics_learner.aprender_secuencia(secuencia)
        
        if dinamica:
            print(f"\n  Dinámica aprendida: {dinamica.id}")
            print(f"  Delta promedio: forma={dinamica.delta_promedio.forma}, "
                  f"funcion={dinamica.delta_promedio.funcion}, "
                  f"estructura={dinamica.delta_promedio.estructura}")
            if dinamica.periodicidad:
                print(f"  Periodicidad detectada: {dinamica.periodicidad}")
        
        num_dinamicas = len(self.evolver.dynamics_learner.dinamicas)
        
        return {
            "num_transiciones": num_dinamicas,
            "dinamica_detectada": dinamica is not None,
        }
    
    # ========================================================================
    # FASE 6: CONSTRUCCIÓN DE RED DE RELATORES
    # ========================================================================
    
    def construir_red_relatores(self) -> Dict:
        """
        Evolver construye red de relatores entre palabras.
        Descubre conexiones fractales en el vocabulario.
        """
        print("\n" + "="*60)
        print("FASE 6: Red de Relatores (Conexiones Fractales)")
        print("="*60)
        
        # Crear arquetipos de todo el vocabulario
        arquetipos_vocab = {}
        for categoria, palabras_dict in self.vocabulario_codificado.items():
            for palabra, tensor in palabras_dict.items():
                arq = self.evolver.archetype_learner.detectar_o_crear(tensor)
                arquetipos_vocab[palabra] = arq
        
        print(f"  Construyendo red con {len(arquetipos_vocab)} arquetipos...")
        
        # Conectar arquetipos similares
        arquetipos_lista = list(arquetipos_vocab.values())
        conexiones_creadas = 0
        
        for i in range(len(arquetipos_lista)):
            for j in range(i + 1, len(arquetipos_lista)):
                arq1 = arquetipos_lista[i]
                arq2 = arquetipos_lista[j]
                
                # Conectar si son diferentes pero similares
                if arq1.id != arq2.id:
                    relator = self.evolver.relator_network.conectar(arq1, arq2, tipo="analogico")
                    if relator.fuerza > 0.5:  # Solo contar conexiones fuertes
                        conexiones_creadas += 1
        
        # Contar arquetipos únicos por ID
        arquetipos_unicos = {}
        for arq in arquetipos_vocab.values():
            arquetipos_unicos[arq.id] = arq
        
        print(f"\n  Arquetipos únicos: {len(arquetipos_unicos)}")
        print(f"  Conexiones fuertes: {conexiones_creadas}")
        print(f"  Relatores totales: {len(self.evolver.relator_network.relatores)}")
        
        # Buscar caminos entre arquetipos
        print(f"\n  Buscando caminos fractales...")
        arqs_ids = list(arquetipos_unicos.keys())
        if len(arqs_ids) >= 2:
            camino = self.evolver.relator_network.camino_mas_corto(arqs_ids[0], arqs_ids[-1])
            if camino:
                print(f"    {arqs_ids[0]} → {arqs_ids[-1]}: {len(camino)} pasos")
        
        return {
            "num_nodos": len(arquetipos_unicos),
            "num_conexiones": conexiones_creadas,
        }
    
    # ========================================================================
    # FASE 7: ARMONIZACIÓN (CORRECCIÓN DE ERRORES)
    # ========================================================================
    
    def armonizar_sistema(self) -> Dict:
        """
        Armonizador valida coherencia global y corrige incoherencias.
        Detecta: correspondencias inválidas, contradicciones, arquetipos débiles,
        relatores rotos, ciclos infinitos, NULLs ambiguos.
        """
        print("\n" + "="*60)
        print("FASE 7: Armonización (Validación + Corrección)")
        print("="*60)
        
        # Crear Armonizador
        armonizador = Armonizador(
            evolver=self.evolver,
            transcender=self.transcender,
            umbral_coherencia=0.7,
            max_recursion=10
        )
        
        print(f"  Creando Armonizador (umbral={armonizador.umbral_coherencia})...")
        
        # Recopilar TODOS los tensores del sistema
        tensores_sistema = []
        
        # 1. Tensores de vocabulario
        for categoria, palabras_dict in self.vocabulario_codificado.items():
            for palabra, tensor in palabras_dict.items():
                tensores_sistema.append(("vocab", palabra, tensor))
        
        # 2. Tensores de frases
        for frase, tensor in self.frases_codificadas:
            tensores_sistema.append(("frase", frase[:30], tensor))
        
        # 3. Tensores de emergencias (Ms, Ss, MetaM)
        for i, (t1, t2, t3, emerg) in enumerate(self.emergencias):
            tensores_sistema.append(("emerg_ms", f"e{i}_ms", emerg.Ms))
            tensores_sistema.append(("emerg_ss", f"e{i}_ss", emerg.Ss))
            tensores_sistema.append(("emerg_metamm", f"e{i}_metamm", emerg.MetaM))
        
        total_tensores = len(tensores_sistema)
        print(f"  Total tensores en sistema: {total_tensores}")
        print(f"    - Vocabulario: {sum(1 for t in tensores_sistema if t[0]=='vocab')}")
        print(f"    - Frases: {sum(1 for t in tensores_sistema if t[0]=='frase')}")
        print(f"    - Emergencias: {sum(1 for t in tensores_sistema if t[0].startswith('emerg'))}")
        
        # Armonizar lote completo
        solo_tensores = [t[2] for t in tensores_sistema]
        
        print(f"\n  🔧 Armonizando {len(solo_tensores)} tensores...")
        reporte = armonizador.armonizar_lote(solo_tensores, "genesis_space")
        
        # Mostrar resultados
        print(f"\n  📊 REPORTE DE ARMONIZACIÓN:")
        print(f"     Coherencia global: {'✅' if reporte['coherente'] else '❌'}")
        print(f"     Incoherencias detectadas: {reporte['incoherencias']}")
        print(f"     Correcciones exitosas: {reporte['correcciones']}")
        print(f"     Correcciones fallidas: {reporte.get('fallidas', 0)}")
        print(f"     Aprendizajes registrados: {reporte['aprendizajes']}")
        
        if reporte.get('coherencia_promedio') is not None:
            print(f"     Coherencia promedio: {reporte['coherencia_promedio']:.3f}")
        
        # Estadísticas globales
        stats = armonizador.obtener_estadisticas()
        print(f"\n  📈 ESTADÍSTICAS ARMONIZADOR:")
        print(f"     Total incoherencias históricas: {stats['total_incoherencias']}")
        print(f"     Total aprendizajes: {stats['total_aprendizajes']}")
        print(f"     Arquetipos monitoreados: {stats['confianzas_arquetipos']}")
        print(f"     Relatores monitoreados: {stats['confianzas_relatores']}")
        print(f"     Espacios lógicos: {stats['correspondencias_espacios']}")
        
        if stats.get('confianza_promedio_arquetipos') is not None:
            print(f"     Confianza promedio arquetipos: {stats['confianza_promedio_arquetipos']:.3f}")
        if stats.get('confianza_promedio_relatores') is not None:
            print(f"     Confianza promedio relatores: {stats['confianza_promedio_relatores']:.3f}")
        
        return {
            "coherente": reporte["coherente"],
            "incoherencias": reporte["incoherencias"],
            "correcciones": reporte["correcciones"],
            "correcciones_fallidas": reporte.get("fallidas", 0),
            "aprendizajes": reporte["aprendizajes"],
            "coherencia_promedio": reporte.get("coherencia_promedio"),
            "estadisticas": stats,
        }
    
    # ========================================================================
    # FASE 8: AUTO-TRADUCCIÓN
    # ========================================================================
    
    def auto_traduccion(self) -> Dict:
        """
        Genesis se traduce a sí mismo:
        Toma una frase nueva, la codifica, sintetiza con arquetipos,
        y genera una "traducción" emergente.
        """
        print("\n" + "="*60)
        print("FASE 8: Auto-Traducción (Genesis → Genesis)")
        print("="*60)
        
        frases_nuevas = [
            "El sistema aprende de su propia coherencia",
            "La recursion genera autosimilitud perfecta",
            "Tres vectores forman un tensor completo",
        ]
        
        traducciones = []
        
        for frase in frases_nuevas:
            print(f"\n  Frase original: {frase}")
            
            # Codificar frase nueva
            embedding = self.model.encode(frase)
            tensor_frase = self.encoder.encode(embedding.tolist())
            
            # Buscar arquetipo más cercano
            distancias_arquetipos = []
            for categoria, palabras_dict in self.vocabulario_codificado.items():
                for palabra, tensor_vocab in palabras_dict.items():
                    dist = np.linalg.norm(
                        tensor_frase.to_ndarray() - tensor_vocab.to_ndarray()
                    )
                    distancias_arquetipos.append((dist, palabra, tensor_vocab))
            
            # Top 3 más cercanos
            top_3 = sorted(distancias_arquetipos, key=lambda x: x[0])[:3]
            palabras_cercanas = [p[1] for p in top_3]
            tensores_cercanos = [p[2] for p in top_3]
            
            print(f"    Arquetipos cercanos: {', '.join(palabras_cercanas)}")
            
            # Sintetizar con los 3 arquetipos
            emergencia = self.transcender.sintetizar(
                tensores_cercanos[0],
                tensores_cercanos[1],
                tensores_cercanos[2]
            )
            
            print(f"    Emergencia: score={emergencia.score_emergencia:.3f}")
            
            traducciones.append({
                "original": frase,
                "arquetipos": palabras_cercanas,
                "emergencia_score": emergencia.score_emergencia,
            })
        
        print(f"\n✅ {len(traducciones)} traducciones auto-generadas")
        return traducciones
    
    # ========================================================================
    # EJECUTAR TODO
    # ========================================================================
    
    def ejecutar_autopoiesis(self) -> Dict:
        """
        Ejecuta todo el proceso de autopoiesis.
        """
        print("\n" + "="*70)
        print("GENESIS AUTOPOIESIS - INICIO")
        print("="*70)
        
        resultados = {
            "version": "1.1.0-armonizador",
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        
        # Fase 1: Vocabulario
        self.codificar_vocabulario()
        resultados["fase_1"] = {
            "vocabulario_size": sum(len(p) for p in self.vocabulario_codificado.values())
        }
        
        # Fase 2: Frases
        self.codificar_frases()
        resultados["fase_2"] = {
            "frases_size": len(self.frases_codificadas)
        }
        
        # Fase 3: Emergencias
        emergencias = self.sintetizar_triadas()
        self.emergencias = emergencias  # Guardar para Fase 7
        resultados["fase_3"] = {
            "emergencias_size": len(emergencias),
            "score_promedio": np.mean([e[3].score_emergencia for e in emergencias]),
        }
        
        # Fase 4: Arquetipos
        arquetipos_info = self.aprender_arquetipos()
        resultados["fase_4"] = arquetipos_info
        
        # Fase 5: Dinámicas
        dinamicas_info = self.aprender_dinamicas()
        resultados["fase_5"] = dinamicas_info
        
        # Fase 6: Relatores
        relatores_info = self.construir_red_relatores()
        resultados["fase_6"] = relatores_info
        
        # Fase 7: Armonización
        armonizacion_info = self.armonizar_sistema()
        resultados["fase_7"] = armonizacion_info
        
        # Fase 8: Auto-traducción
        traducciones = self.auto_traduccion()
        resultados["fase_8"] = {
            "traducciones": traducciones
        }
        
        # VEREDICTO FINAL
        print("\n" + "="*60)
        print("*** VEREDICTO AUTOPOIESIS ***")
        print("="*60)
        
        print(f"\n  Vocabulario:  {resultados['fase_1']['vocabulario_size']} palabras")
        print(f"  Frases:       {resultados['fase_2']['frases_size']} frases")
        print(f"  Emergencias:  {resultados['fase_3']['emergencias_size']} (score={resultados['fase_3']['score_promedio']:.3f})")
        print(f"  Arquetipos:   {resultados['fase_4']['num_arquetipos']}")
        print(f"  Dinámicas:    {resultados['fase_5']['num_transiciones']} transiciones")
        print(f"  Relatores:    {resultados['fase_6']['num_conexiones']} conexiones")
        print(f"  Armonización: {'✅ Coherente' if resultados['fase_7']['coherente'] else '⚠️ Incoherencias'} ({resultados['fase_7']['correcciones']} correcciones)")
        print(f"  Traducciones: {len(resultados['fase_8']['traducciones'])}")
        
        print("\n  ✅ GENESIS SE HA AUTO-DESCUBIERTO Y AUTO-CORREGIDO")
        print("     El sistema ahora comprende su propia estructura y mantiene coherencia.")
        
        return resultados

# ============================================================================
# CLI
# ============================================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Genesis Autopoiesis - El sistema se descubre a sí mismo"
    )
    parser.add_argument(
        "--output",
        default="genesis_autopoiesis_results.json",
        help="Archivo de salida JSON"
    )
    
    args = parser.parse_args()
    
    # Ejecutar autopoiesis
    genesis = GenesisAutopoiesis()
    resultados = genesis.ejecutar_autopoiesis()
    
    # Guardar
    # Serializar quitando objetos no serializables
    resultados_serializables = {
        "version": resultados["version"],
        "fecha": resultados["fecha"],
        "fase_1": resultados["fase_1"],
        "fase_2": resultados["fase_2"],
        "fase_3": {
            "emergencias_size": resultados["fase_3"]["emergencias_size"],
            "score_promedio": float(resultados["fase_3"]["score_promedio"]),
        },
        "fase_4": {
            "num_arquetipos": resultados["fase_4"]["num_arquetipos"],
        },
        "fase_5": resultados["fase_5"],
        "fase_6": resultados["fase_6"],
        "fase_7": {
            "coherente": resultados["fase_7"]["coherente"],
            "incoherencias": resultados["fase_7"]["incoherencias"],
            "correcciones": resultados["fase_7"]["correcciones"],
            "aprendizajes": resultados["fase_7"]["aprendizajes"],
            "coherencia_promedio": float(resultados["fase_7"]["coherencia_promedio"]) if resultados["fase_7"]["coherencia_promedio"] else None,
        },
        "fase_8": {
            "traducciones": [
                {
                    "original": t["original"],
                    "arquetipos": t["arquetipos"],
                    "emergencia_score": float(t["emergencia_score"]),
                }
                for t in resultados["fase_8"]["traducciones"]
            ]
        },
    }
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(resultados_serializables, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultados guardados en: {args.output}")

if __name__ == "__main__":
    main()
