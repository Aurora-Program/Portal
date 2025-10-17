"""
FFE Encoder MCP Server
Proyecto Genesis - Aurora Intelligence Engine

Servidor MCP que codifica embeddings de LLMs a Tensores FFE:
- Tool: encode_to_ffe (embedding → TensorFFE)
- Tool: decode_from_ffe (TensorFFE → vector aproximado)
- Tool: compare_embeddings (compara embedding vs FFE)
- Resource: ffe://encoder/status
- Resource: ffe://stats/compression

Fase 1: Sin LoRA (discretización directa)
Fase 2: Con LoRA₁ (pre-quantization) + LoRA₂ (emergent bias)
"""

import asyncio
import json
from typing import List, Dict, Optional
import numpy as np
from mcp.server import Server
from mcp.types import Resource, Tool, TextContent, ImageContent, EmbeddedResource
import mcp.server.stdio

from tensor_ffe import TensorFFE, VectorFFE, crear_tensor_desde_lista
from transcender import Transcender
from evolver import Evolver


class FFEEncoder:
    """Codificador de embeddings a tensores FFE"""
    
    def __init__(self, dimension_embedding: int = 768):
        self.dimension_embedding = dimension_embedding
        self.evolver = Evolver()
        self.total_codificaciones = 0
        self.ratio_compresion_promedio = 0.0
    
    def encode(self, embedding: List[float]) -> TensorFFE:
        """
        Codifica embedding de LLM a TensorFFE
        
        Estrategia (sin LoRA):
        1. PCA para reducir a 9 dimensiones principales
        2. Cuantización a rango [0, 7] (3 bits)
        3. Distribuir en 3 vectores FFE
        """
        if len(embedding) != self.dimension_embedding:
            raise ValueError(f"Esperaba {self.dimension_embedding} dims, recibió {len(embedding)}")
        
        # === Fase 1: Reducción dimensional (PCA simulado) ===
        # Seleccionar 9 componentes principales por segmentos
        segmento = len(embedding) // 9
        componentes = [
            np.mean(embedding[i*segmento:(i+1)*segmento]) 
            for i in range(9)
        ]
        
        # === Fase 2: Cuantización [0, 7] ===
        valores_octales = self._cuantizar_octales(componentes)
        
        # === Fase 3: Construir TensorFFE ===
        tensor = TensorFFE()
        tensor.nivel_1[0] = VectorFFE(
            forma=valores_octales[0],
            funcion=valores_octales[1],
            estructura=valores_octales[2]
        )
        tensor.nivel_1[1] = VectorFFE(
            forma=valores_octales[3],
            funcion=valores_octales[4],
            estructura=valores_octales[5]
        )
        tensor.nivel_1[2] = VectorFFE(
            forma=valores_octales[6],
            funcion=valores_octales[7],
            estructura=valores_octales[8]
        )
        
        tensor.reconstruir_jerarquia()
        
        # Aprender arquetipo
        self.evolver.aprender(tensor)
        
        # Métricas
        self.total_codificaciones += 1
        ratio = tensor.compresion_ratio(self.dimension_embedding * 32)
        self.ratio_compresion_promedio = (
            (self.ratio_compresion_promedio * (self.total_codificaciones - 1) + ratio) / 
            self.total_codificaciones
        )
        
        return tensor
    
    def _cuantizar_octales(self, componentes: List[float]) -> List[int]:
        """Cuantiza 9 valores float a [0, 7]"""
        # Normalizar a [0, 1]
        min_val = min(componentes)
        max_val = max(componentes)
        rango = max_val - min_val if max_val > min_val else 1.0
        
        normalizados = [(c - min_val) / rango for c in componentes]
        
        # Cuantizar a [0, 7]
        octales = [int(n * 7.999) for n in normalizados]  # 7.999 para incluir 7
        return [max(0, min(7, o)) for o in octales]
    
    def decode(self, tensor: TensorFFE, dim_salida: int = 768) -> List[float]:
        """
        Decodifica TensorFFE a vector aproximado
        Reconstrucción parcial (pérdida intencional)
        """
        # Extraer 9 valores octales
        valores = []
        for v in tensor.nivel_1:
            valores.extend([v.forma, v.funcion, v.estructura])
        
        # Expandir a dim_salida con interpolación
        vector_expandido = []
        segmento = dim_salida // 9
        
        for i, val in enumerate(valores):
            # Denormalizar [0, 7] → [-1, 1]
            denorm = (val / 7.0) * 2 - 1
            
            # Repetir con ruido Gaussiano ligero
            for _ in range(segmento):
                ruido = np.random.normal(0, 0.05)
                vector_expandido.append(denorm + ruido)
        
        # Ajustar longitud
        while len(vector_expandido) < dim_salida:
            vector_expandido.append(0.0)
        
        return vector_expandido[:dim_salida]
    
    def compare(self, embedding_original: List[float], tensor: TensorFFE) -> Dict[str, float]:
        """Compara embedding original vs reconstruido desde FFE"""
        reconstruido = self.decode(tensor, len(embedding_original))
        
        # Similitud coseno
        cos_sim = self._cosine_similarity(embedding_original, reconstruido)
        
        # Error cuadrático medio
        mse = np.mean([(a - b) ** 2 for a, b in zip(embedding_original, reconstruido)])
        
        # Ratio de compresión
        bits_original = len(embedding_original) * 32
        bits_ffe = 117
        ratio = bits_original / bits_ffe
        
        return {
            'similitud_coseno': float(cos_sim),
            'error_mse': float(mse),
            'ratio_compresion': float(ratio),
            'bits_original': bits_original,
            'bits_ffe': bits_ffe
        }
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Similitud coseno entre dos vectores"""
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = np.sqrt(sum(x ** 2 for x in a))
        norm_b = np.sqrt(sum(y ** 2 for y in b))
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        return dot / (norm_a * norm_b)
    
    def estadisticas(self) -> Dict[str, any]:
        """Estadísticas del encoder"""
        stats_evolver = self.evolver.estadisticas()
        
        return {
            'total_codificaciones': self.total_codificaciones,
            'ratio_compresion_promedio': self.ratio_compresion_promedio,
            'dimension_embedding': self.dimension_embedding,
            'arquetipos_aprendidos': stats_evolver['arquetipos'],
            'relatores': stats_evolver['relatores']
        }


# === MCP Server ===

app = Server("ffe-encoder")
encoder = FFEEncoder(dimension_embedding=768)


@app.list_resources()
async def list_resources() -> list[Resource]:
    """Lista recursos disponibles"""
    return [
        Resource(
            uri="ffe://encoder/status",
            name="FFE Encoder Status",
            mimeType="application/json",
            description="Estado actual del encoder FFE"
        ),
        Resource(
            uri="ffe://stats/compression",
            name="Compression Statistics",
            mimeType="application/json",
            description="Estadísticas de compresión y aprendizaje"
        )
    ]


@app.read_resource()
async def read_resource(uri: str) -> str:
    """Lee un recurso"""
    if uri == "ffe://encoder/status":
        status = {
            'encoder': 'operational',
            'dimension': encoder.dimension_embedding,
            'total_encodings': encoder.total_codificaciones,
            'lora_enabled': False  # Fase 1: sin LoRA
        }
        return json.dumps(status, indent=2)
    
    elif uri == "ffe://stats/compression":
        stats = encoder.estadisticas()
        return json.dumps(stats, indent=2)
    
    else:
        raise ValueError(f"Recurso desconocido: {uri}")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """Lista tools disponibles"""
    return [
        Tool(
            name="encode_to_ffe",
            description="Codifica embedding de LLM a TensorFFE (117 bits)",
            inputSchema={
                "type": "object",
                "properties": {
                    "embedding": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Embedding de LLM (768 dims)"
                    }
                },
                "required": ["embedding"]
            }
        ),
        Tool(
            name="decode_from_ffe",
            description="Decodifica TensorFFE a vector aproximado",
            inputSchema={
                "type": "object",
                "properties": {
                    "tensor_bits": {
                        "type": "string",
                        "description": "Tensor FFE serializado (117 bits en hex)"
                    },
                    "output_dim": {
                        "type": "integer",
                        "description": "Dimensión de salida (default: 768)",
                        "default": 768
                    }
                },
                "required": ["tensor_bits"]
            }
        ),
        Tool(
            name="compare_embeddings",
            description="Compara embedding original vs reconstruido desde FFE",
            inputSchema={
                "type": "object",
                "properties": {
                    "embedding": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Embedding original"
                    },
                    "tensor_bits": {
                        "type": "string",
                        "description": "Tensor FFE serializado"
                    }
                },
                "required": ["embedding", "tensor_bits"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Ejecuta una tool"""
    
    if name == "encode_to_ffe":
        embedding = arguments['embedding']
        
        # Validar dimensión
        if len(embedding) != encoder.dimension_embedding:
            return [TextContent(
                type="text",
                text=f"Error: Esperaba {encoder.dimension_embedding} dims, recibió {len(embedding)}"
            )]
        
        # Codificar
        tensor = encoder.encode(embedding)
        
        # Serializar
        bits = tensor.to_bits()
        
        result = {
            'tensor_ffe': {
                'nivel_1': [
                    {'f': v.forma, 'fn': v.funcion, 'e': v.estructura}
                    for v in tensor.nivel_1
                ],
                'nivel_abstraccion': tensor.nivel_abstraccion,
                'coherencia': tensor.coherencia()
            },
            'serializacion': {
                'bits': bits,
                'hex': hex(int(bits, 2)),
                'bytes': len(bits) // 8 + 1
            },
            'compresion': {
                'bits_original': len(embedding) * 32,
                'bits_ffe': 117,
                'ratio': tensor.compresion_ratio(len(embedding) * 32)
            }
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    elif name == "decode_from_ffe":
        tensor_bits = arguments['tensor_bits']
        output_dim = arguments.get('output_dim', 768)
        
        # Deserializar
        if tensor_bits.startswith('0x'):
            bits = bin(int(tensor_bits, 16))[2:].zfill(117)
        else:
            bits = tensor_bits
        
        tensor = TensorFFE.from_bits(bits)
        
        # Decodificar
        vector = encoder.decode(tensor, output_dim)
        
        result = {
            'vector_reconstruido': vector[:10],  # Primeros 10 valores
            'dimension': len(vector),
            'rango': [float(min(vector)), float(max(vector))],
            'nota': 'Vector completo truncado a 10 valores para visualización'
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    elif name == "compare_embeddings":
        embedding = arguments['embedding']
        tensor_bits = arguments['tensor_bits']
        
        # Deserializar tensor
        if tensor_bits.startswith('0x'):
            bits = bin(int(tensor_bits, 16))[2:].zfill(117)
        else:
            bits = tensor_bits
        
        tensor = TensorFFE.from_bits(bits)
        
        # Comparar
        comparacion = encoder.compare(embedding, tensor)
        
        return [TextContent(
            type="text",
            text=json.dumps(comparacion, indent=2)
        )]
    
    else:
        return [TextContent(
            type="text",
            text=f"Tool desconocida: {name}"
        )]


async def main():
    """Punto de entrada del servidor MCP"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    print("🌉 FFE Encoder MCP Server - Proyecto Genesis")
    print("Iniciando servidor MCP...")
    asyncio.run(main())
