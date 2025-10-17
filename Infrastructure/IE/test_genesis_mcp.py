"""
🧪 Test Suite - Genesis MCP Server Funcional
=============================================

Suite de pruebas para validar integración MCP de Genesis Funcional.
"""

import asyncio
import json
from genesis_mcp_server import (
    inicializar_genesis,
    _genesis_pipeline,
    _transcender_sintetizar,
    _evolver_aprender,
    _armonizador_encodear,
    _genesis_estado
)
from tensor_ffe import TensorFFE

async def test_inicializacion():
    """Test 1: Inicialización de Genesis MCP."""
    print("\n" + "="*60)
    print("TEST 1: Inicialización de Genesis MCP")
    print("="*60)
    
    try:
        state = inicializar_genesis()
        
        assert state.genesis is not None, "Genesis no inicializado"
        assert state.transcender is not None, "Transcender no inicializado"
        assert state.evolver is not None, "Evolver no inicializado"
        assert state.armonizador is not None, "Armonizador no inicializado"
        
        print("✅ PASS: Todos los componentes inicializados correctamente")
        return True
    
    except Exception as e:
        print(f"❌ FAIL: {str(e)}")
        return False

async def test_armonizador_mcp():
    """Test 2: Armonizador vía MCP."""
    print("\n" + "="*60)
    print("TEST 2: Armonizador Encodear (MCP)")
    print("="*60)
    
    try:
        args = {"texto": "perro"}
        result = await _armonizador_encodear(args)
        
        response = json.loads(result[0].text)
        
        assert response["success"] == True, "Encodear falló"
        assert "tensor_ffe" in response, "Tensor FFE no encontrado"
        assert response["texto"] == "perro", "Texto no coincide"
        
        print(f"✅ PASS: Texto '{args['texto']}' encodeado correctamente")
        print(f"   Tensor FFE: {response['tensor_ffe']}")
        return True
    
    except Exception as e:
        print(f"❌ FAIL: {str(e)}")
        return False

async def test_transcender_mcp():
    """Test 3: Transcender vía MCP."""
    print("\n" + "="*60)
    print("TEST 3: Transcender Sintetizar (MCP)")
    print("="*60)
    
    try:
        # Crear 3 tensores de prueba
        tensor_a = TensorFFE(forma=3, funcion=4, estructura=2)
        tensor_b = TensorFFE(forma=5, funcion=1, estructura=6)
        tensor_c = TensorFFE(forma=2, funcion=7, estructura=3)
        
        args = {
            "tensor_a": {"forma": tensor_a.forma, "funcion": tensor_a.funcion, "estructura": tensor_a.estructura},
            "tensor_b": {"forma": tensor_b.forma, "funcion": tensor_b.funcion, "estructura": tensor_b.estructura},
            "tensor_c": {"forma": tensor_c.forma, "funcion": tensor_c.funcion, "estructura": tensor_c.estructura}
        }
        
        result = await _transcender_sintetizar(args)
        response = json.loads(result[0].text)
        
        assert response["success"] == True, "Síntesis falló"
        assert "tensor_emergente" in response, "Tensor emergente no encontrado"
        assert "score_sintesis" in response, "Score no encontrado"
        
        print(f"✅ PASS: Síntesis emergente generada")
        print(f"   Tensor emergente: {response['tensor_emergente']}")
        print(f"   Score: {response['score_sintesis']}")
        return True
    
    except Exception as e:
        print(f"❌ FAIL: {str(e)}")
        return False

async def test_evolver_mcp():
    """Test 4: Evolver vía MCP."""
    print("\n" + "="*60)
    print("TEST 4: Evolver Aprender (MCP)")
    print("="*60)
    
    try:
        tensor = TensorFFE(forma=3, funcion=4, estructura=2)
        
        args = {
            "tensor": {"forma": tensor.forma, "funcion": tensor.funcion, "estructura": tensor.estructura},
            "etiqueta": "test_arquetipo"
        }
        
        result = await _evolver_aprender(args)
        response = json.loads(result[0].text)
        
        assert response["success"] == True, "Aprendizaje falló"
        assert "arquetipos_descubiertos" in response, "Arquetipos no encontrados"
        
        print(f"✅ PASS: Arquetipos aprendidos")
        print(f"   Total arquetipos: {response['arquetipos_descubiertos']}")
        print(f"   Etiqueta: {response['etiqueta']}")
        return True
    
    except Exception as e:
        print(f"❌ FAIL: {str(e)}")
        return False

async def test_genesis_pipeline_mcp():
    """Test 5: Genesis Pipeline completo vía MCP."""
    print("\n" + "="*60)
    print("TEST 5: Genesis Pipeline Completo (MCP)")
    print("="*60)
    
    try:
        args = {
            "textos": ["El perro corre rápido", "El gato salta alto"],
            "opciones": {
                "usar_cache": True,
                "nivel_abstraccion": 5
            }
        }
        
        result = await _genesis_pipeline(args)
        response = json.loads(result[0].text)
        
        assert response["success"] == True, "Pipeline falló"
        assert response["fases_completadas"] == 8, "No se completaron 8 fases"
        assert "vocabulario" in response, "Vocabulario no encontrado"
        assert "emergencias" in response, "Emergencias no encontradas"
        
        print(f"✅ PASS: Pipeline Genesis ejecutado")
        print(f"   Fases completadas: {response['fases_completadas']}")
        print(f"   Textos procesados: {response['textos_procesados']}")
        print(f"   Palabras vocabulario: {response['vocabulario']['total_palabras']}")
        print(f"   Emergencias: {response['emergencias']['total']}")
        return True
    
    except Exception as e:
        print(f"❌ FAIL: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def test_genesis_estado_mcp():
    """Test 6: Estado de Genesis vía MCP."""
    print("\n" + "="*60)
    print("TEST 6: Genesis Estado (MCP)")
    print("="*60)
    
    try:
        result = await _genesis_estado({})
        response = json.loads(result[0].text)
        
        assert response["success"] == True, "Consulta de estado falló"
        assert "estadisticas" in response, "Estadísticas no encontradas"
        assert "componentes" in response, "Componentes no encontrados"
        
        print(f"✅ PASS: Estado obtenido correctamente")
        print(f"   Version: {response['version']}")
        print(f"   Estado: {response['estado']}")
        print(f"   Componentes activos: {sum(response['componentes'].values())}/4")
        return True
    
    except Exception as e:
        print(f"❌ FAIL: {str(e)}")
        return False

async def main():
    """Ejecuta suite completa de tests."""
    print("\n" + "="*70)
    print("🧪 GENESIS MCP SERVER - TEST SUITE v1.3.3 FUNCIONAL")
    print("="*70)
    
    # Inicializar estado global
    import genesis_mcp_server
    genesis_mcp_server._GLOBAL_STATE = inicializar_genesis()
    
    tests = [
        test_inicializacion,
        test_armonizador_mcp,
        test_transcender_mcp,
        test_evolver_mcp,
        test_genesis_pipeline_mcp,
        test_genesis_estado_mcp
    ]
    
    results = []
    for test in tests:
        result = await test()
        results.append(result)
        await asyncio.sleep(0.1)  # Pequeña pausa entre tests
    
    # Resumen
    print("\n" + "="*70)
    print("📊 RESUMEN DE TESTS")
    print("="*70)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\nTests ejecutados: {total}")
    print(f"Tests exitosos:   {passed} ✅")
    print(f"Tests fallidos:   {total - passed} ❌")
    print(f"Tasa de éxito:    {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 ¡TODOS LOS TESTS PASARON!")
        print("   Genesis MCP Server funcional está listo para producción.")
    else:
        print(f"\n⚠️  {total - passed} test(s) fallaron. Revisar errores arriba.")
    
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
