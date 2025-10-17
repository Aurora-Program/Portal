"""
🌌 Aurora MCP Server
====================

Model Context Protocol server que expone Aurora Trinity-3 como servicio MCP.
Permite que Genesis y otros clientes MCP utilicen Aurora IE.

Basado en: https://modelcontextprotocol.io/
Compatible con: Genesis v0.3.1+

Author: Aurora Alliance
License: Apache-2.0
Version: 1.0.0
"""

import asyncio
import json
from typing import Any, Dict, List, Optional, Sequence
from datetime import datetime

# MCP SDK
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import (
        Resource,
        Tool,
        TextContent,
        ImageContent,
        EmbeddedResource,
        LoggingLevel
    )
except ImportError:
    print("⚠️  MCP SDK not installed. Install with: pip install mcp")
    print("   For now, using mock classes for development")
    
    # Mock classes for development without MCP SDK
    class Server:
        def __init__(self, name: str):
            self.name = name
            self._tools = {}
            self._resources = {}
        
        def list_tools(self):
            def decorator(func):
                self._tools['list'] = func
                return func
            return decorator
        
        def call_tool(self):
            def decorator(func):
                self._tools['call'] = func
                return func
            return decorator
        
        def list_resources(self):
            def decorator(func):
                self._resources['list'] = func
                return func
            return decorator
        
        def read_resource(self):
            def decorator(func):
                self._resources['read'] = func
                return func
            return decorator
    
    class Tool:
        def __init__(self, name: str, description: str, inputSchema: dict):
            self.name = name
            self.description = description
            self.inputSchema = inputSchema
    
    class Resource:
        def __init__(self, uri: str, name: str, description: str, mimeType: str):
            self.uri = uri
            self.name = name
            self.description = description
            self.mimeType = mimeType
    
    class TextContent:
        def __init__(self, type: str, text: str):
            self.type = type
            self.text = text
    
    async def stdio_server():
        """Mock stdio server for development"""
        async def run(server):
            print(f"🌌 Aurora MCP Server '{server.name}' running (mock mode)")
            print("   Install MCP SDK for full functionality: pip install mcp")
            await asyncio.sleep(3600)  # Keep alive
        
        class Context:
            async def __aenter__(self):
                return self
            async def __aexit__(self, *args):
                pass
            def __call__(self, server):
                return self
            async def run(self, server):
                await run(server)
        
        return Context()

# Aurora Core
from aurora_engine import Aurora, AuroraCognitiveCycle
from core import (
    FractalTensor,
    Trigate,
    FractalKnowledgeBase,
    pattern0_create_fractal_cluster
)

# ===============================================================================
# MCP SERVER CONFIGURATION
# ===============================================================================

# Initialize Aurora MCP Server
server = Server("aurora-trinity-3")

# Global Aurora instance (persistent across requests)
AURORA_INSTANCE = Aurora()
ACTIVE_SPACES = {}  # Track active logical spaces

# ===============================================================================
# MCP TOOLS - Aurora Capabilities
# ===============================================================================

@server.list_tools()
async def list_tools() -> List[Tool]:
    """Lista todas las herramientas Aurora disponibles via MCP."""
    return [
        Tool(
            name="aurora_learn",
            description="Learn ternary patterns (0, 1, NULL) in a logical space. "
                       "Returns success confirmation and KB stats.",
            inputSchema={
                "type": "object",
                "properties": {
                    "patterns": {
                        "type": "array",
                        "description": "List of ternary vectors [[1,0,1], [0,1,0], ...]",
                        "items": {
                            "type": "array",
                            "items": {"type": ["integer", "null"]}
                        }
                    },
                    "space_id": {
                        "type": "string",
                        "description": "Logical space identifier (default: 'default')",
                        "default": "default"
                    }
                },
                "required": ["patterns"]
            }
        ),
        Tool(
            name="aurora_query",
            description="Query Aurora with a ternary pattern (can include NULLs). "
                       "Aurora will deduce unknown values using RecursiveDeductionNetwork.",
            inputSchema={
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "array",
                        "description": "Ternary vector [1, null, 0] with potential NULLs",
                        "items": {"type": ["integer", "null"]}
                    },
                    "space_id": {
                        "type": "string",
                        "description": "Logical space to query (default: 'default')",
                        "default": "default"
                    }
                },
                "required": ["pattern"]
            }
        ),
        Tool(
            name="aurora_synthesize",
            description="Synthesize 3 tensors into emergent pattern using Transcender. "
                       "Returns M_emergent and MetaM.",
            inputSchema={
                "type": "object",
                "properties": {
                    "tensor_a": {
                        "type": "array",
                        "description": "First ternary vector",
                        "items": {"type": "integer"}
                    },
                    "tensor_b": {
                        "type": "array",
                        "description": "Second ternary vector",
                        "items": {"type": "integer"}
                    },
                    "tensor_c": {
                        "type": "array",
                        "description": "Third ternary vector",
                        "items": {"type": "integer"}
                    }
                },
                "required": ["tensor_a", "tensor_b", "tensor_c"]
            }
        ),
        Tool(
            name="aurora_pattern0",
            description="Generate ethical fractal cluster using Pattern 0. "
                       "Creates harmonized tensors with PHI-based coherence.",
            inputSchema={
                "type": "object",
                "properties": {
                    "input_data": {
                        "type": "array",
                        "description": "Optional seed patterns",
                        "items": {
                            "type": "array",
                            "items": {"type": "integer"}
                        }
                    },
                    "num_tensors": {
                        "type": "integer",
                        "description": "Number of tensors to generate (default: 3)",
                        "default": 3
                    },
                    "space_id": {
                        "type": "string",
                        "description": "Logical space",
                        "default": "default"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="aurora_kb_status",
            description="Get Knowledge Base status: universes, archetypes, metrics.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="aurora_save_kb",
            description="Persist Knowledge Base to disk (JSON format).",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "File path for KB (default: aurora_kb.json)",
                        "default": "aurora_kb.json"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="aurora_load_kb",
            description="Load Knowledge Base from disk.",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "File path to load",
                        "default": "aurora_kb.json"
                    }
                },
                "required": ["path"]
            }
        ),
        Tool(
            name="aurora_metrics",
            description="Get Aurora system metrics: operations, coherence, stats.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent]:
    """Ejecuta herramienta Aurora solicitada por Genesis u otro cliente MCP."""
    
    try:
        if name == "aurora_learn":
            patterns = arguments.get("patterns", [])
            space_id = arguments.get("space_id", "default")
            
            # Learn patterns
            AURORA_INSTANCE.learn(patterns, space_id=space_id)
            
            # Track space
            ACTIVE_SPACES[space_id] = {
                "last_updated": datetime.now().isoformat(),
                "pattern_count": len(patterns)
            }
            
            result = {
                "success": True,
                "space_id": space_id,
                "patterns_learned": len(patterns),
                "kb_universes": len(AURORA_INSTANCE.kb.universes),
                "message": f"Learned {len(patterns)} patterns in space '{space_id}'"
            }
            
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "aurora_query":
            pattern = arguments.get("pattern", [])
            space_id = arguments.get("space_id", "default")
            
            # Query with potential NULLs
            result_tensor = AURORA_INSTANCE.query(pattern, space_id=space_id)
            
            # Extract result
            if hasattr(result_tensor, 'nivel_3') and result_tensor.nivel_3:
                resolved_pattern = result_tensor.nivel_3[0]
            else:
                resolved_pattern = pattern
            
            null_count = sum(1 for x in pattern if x is None)
            
            result = {
                "success": True,
                "input_pattern": pattern,
                "resolved_pattern": resolved_pattern,
                "nulls_resolved": null_count,
                "space_id": space_id,
                "method": "RecursiveDeductionNetwork" if null_count > 0 else "direct_lookup"
            }
            
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "aurora_synthesize":
            from core import Transcender, FractalTensor
            
            tensor_a = FractalTensor(nivel_3=[arguments["tensor_a"]])
            tensor_b = FractalTensor(nivel_3=[arguments["tensor_b"]])
            tensor_c = FractalTensor(nivel_3=[arguments["tensor_c"]])
            
            transcender = Transcender()
            synthesized = transcender.compute_full_fractal(
                tensor_a, tensor_b, tensor_c
            )
            
            result = {
                "success": True,
                "M_emergent": synthesized.Ms,
                "MetaM": synthesized.MetaM,
                "Ss": synthesized.Ss if hasattr(synthesized, 'Ss') else None,
                "nivel_3": synthesized.nivel_3[0] if synthesized.nivel_3 else []
            }
            
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "aurora_pattern0":
            input_data = arguments.get("input_data")
            num_tensors = arguments.get("num_tensors", 3)
            space_id = arguments.get("space_id", "default")
            
            context = {
                'kb': AURORA_INSTANCE.kb,
                'armonizador': AURORA_INSTANCE.cycle.armonizador,
                'pool': AURORA_INSTANCE.cycle.pool
            }
            
            cluster = pattern0_create_fractal_cluster(
                input_data=input_data,
                space_id=space_id,
                num_tensors=num_tensors,
                context=context
            )
            
            result = {
                "success": True,
                "num_tensors": len(cluster),
                "tensors": [
                    {
                        "nivel_3": t.nivel_3[0] if t.nivel_3 else [],
                        "ethical_hash": t.metadata.get("ethical_hash", "")[:16]
                    }
                    for t in cluster
                ],
                "space_id": space_id
            }
            
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "aurora_kb_status":
            status = {
                "total_universes": len(AURORA_INSTANCE.kb.universes),
                "active_spaces": list(ACTIVE_SPACES.keys()),
                "universes": {
                    space_id: {
                        "archetypes": len(universe.storage),
                        "indexed": len(universe.ms_index)
                    }
                    for space_id, universe in AURORA_INSTANCE.kb.universes.items()
                }
            }
            
            return [TextContent(type="text", text=json.dumps(status, indent=2))]
        
        elif name == "aurora_save_kb":
            path = arguments.get("path", "aurora_kb.json")
            AURORA_INSTANCE.save(path, format='json')
            
            result = {
                "success": True,
                "path": path,
                "universes_saved": len(AURORA_INSTANCE.kb.universes),
                "message": f"KB saved to {path}"
            }
            
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "aurora_load_kb":
            path = arguments["path"]
            global AURORA_INSTANCE
            AURORA_INSTANCE = Aurora(kb_path=path)
            
            result = {
                "success": True,
                "path": path,
                "universes_loaded": len(AURORA_INSTANCE.kb.universes),
                "message": f"KB loaded from {path}"
            }
            
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "aurora_metrics":
            metrics = AURORA_INSTANCE.metrics()
            
            return [TextContent(type="text", text=json.dumps(metrics, indent=2))]
        
        else:
            error = {"error": f"Unknown tool: {name}"}
            return [TextContent(type="text", text=json.dumps(error))]
    
    except Exception as e:
        error = {
            "error": str(e),
            "tool": name,
            "arguments": arguments
        }
        return [TextContent(type="text", text=json.dumps(error, indent=2))]

# ===============================================================================
# MCP RESOURCES - Aurora Knowledge Base
# ===============================================================================

@server.list_resources()
async def list_resources() -> List[Resource]:
    """Lista recursos Aurora disponibles (KB, modelos, métricas)."""
    resources = [
        Resource(
            uri="aurora://kb/status",
            name="Knowledge Base Status",
            description="Current state of Aurora Knowledge Base",
            mimeType="application/json"
        ),
        Resource(
            uri="aurora://metrics/current",
            name="Aurora Metrics",
            description="Real-time system metrics",
            mimeType="application/json"
        ),
        Resource(
            uri="aurora://config/trigate",
            name="Trigate Configuration",
            description="Trigate LUT configuration and stats",
            mimeType="application/json"
        )
    ]
    
    # Add dynamic resources for each active space
    for space_id in ACTIVE_SPACES.keys():
        resources.append(
            Resource(
                uri=f"aurora://kb/space/{space_id}",
                name=f"Space: {space_id}",
                description=f"Knowledge Base for logical space '{space_id}'",
                mimeType="application/json"
            )
        )
    
    return resources

@server.read_resource()
async def read_resource(uri: str) -> str:
    """Lee contenido de recurso Aurora."""
    
    if uri == "aurora://kb/status":
        status = {
            "total_universes": len(AURORA_INSTANCE.kb.universes),
            "active_spaces": list(ACTIVE_SPACES.keys()),
            "timestamp": datetime.now().isoformat()
        }
        return json.dumps(status, indent=2)
    
    elif uri == "aurora://metrics/current":
        metrics = AURORA_INSTANCE.metrics()
        return json.dumps(metrics, indent=2)
    
    elif uri == "aurora://config/trigate":
        config = {
            "lut_entries_per_operation": 27,
            "operations": ["infer", "learn", "deduce_a", "deduce_b"],
            "null_handling": "computational_honesty",
            "lookup_complexity": "O(1)"
        }
        return json.dumps(config, indent=2)
    
    elif uri.startswith("aurora://kb/space/"):
        space_id = uri.split("/")[-1]
        if space_id in AURORA_INSTANCE.kb.universes:
            universe = AURORA_INSTANCE.kb.universes[space_id]
            space_data = {
                "space_id": space_id,
                "archetypes": len(universe.storage),
                "names": list(universe.name_index.keys()),
                "indexed_ms": len(universe.ms_index),
                "indexed_ss": len(universe.ss_index)
            }
            return json.dumps(space_data, indent=2)
        else:
            return json.dumps({"error": f"Space '{space_id}' not found"})
    
    else:
        return json.dumps({"error": f"Resource not found: {uri}"})

# ===============================================================================
# MAIN - Start MCP Server
# ===============================================================================

async def main():
    """Inicializa y ejecuta Aurora MCP Server."""
    print("="*70)
    print("  🌌 AURORA MCP SERVER")
    print("="*70)
    print(f"  Version: 1.0.0")
    print(f"  Protocol: Model Context Protocol (MCP)")
    print(f"  Compatible with: Genesis v0.3.1+")
    print(f"  Timestamp: {datetime.now().isoformat()}")
    print("="*70)
    print()
    print("🔧 Initializing Aurora Trinity-3...")
    print(f"   KB Universes: {len(AURORA_INSTANCE.kb.universes)}")
    print(f"   Tools available: 8")
    print(f"   Resources available: 3+ (dynamic)")
    print()
    print("✅ Aurora MCP Server ready!")
    print("   Waiting for Genesis or MCP client connections...")
    print()
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
