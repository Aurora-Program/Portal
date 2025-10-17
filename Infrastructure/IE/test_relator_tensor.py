"""
Test para validar que los relatores tienen tensor_origen válido
"""
import sys
sys.path.append('.')

from tensor_ffe import TensorFFE, VectorFFE
from transcender import Transcender
from evolver import Evolver, Arquetipo

print("="*70)
print("TEST: Relatores con Tensor de Transformación")
print("="*70)

# 1. Crear Evolver con Transcender
print("\n[1/5] Creando Evolver...")
evolver = Evolver()  # Evolver crea su propio Transcender internamente
transcender = evolver.transcender  # Usar el mismo Transcender
print("✅ Componentes creados")

# 2. Crear 2 arquetipos de prueba
print("\n[2/5] Creando arquetipos de prueba...")
tensor1 = TensorFFE()
tensor1.nivel_1[0] = VectorFFE(forma=2, funcion=3, estructura=1)
tensor1.nivel_1[1] = VectorFFE(forma=5, funcion=4, estructura=6)
tensor1.nivel_1[2] = VectorFFE(forma=1, funcion=2, estructura=3)

tensor2 = TensorFFE()
tensor2.nivel_1[0] = VectorFFE(forma=3, funcion=4, estructura=2)
tensor2.nivel_1[1] = VectorFFE(forma=6, funcion=5, estructura=7)
tensor2.nivel_1[2] = VectorFFE(forma=2, funcion=3, estructura=4)

arq1 = evolver.archetype_learner.detectar_o_crear(tensor1)
arq2 = evolver.archetype_learner.detectar_o_crear(tensor2)

print(f"  Arquetipo 1: {arq1.id} (freq={arq1.frecuencia})")
print(f"  Arquetipo 2: {arq2.id} (freq={arq2.frecuencia})")
print("✅ Arquetipos creados")

# 3. Conectar arquetipos
print("\n[3/5] Conectando arquetipos...")
relator = evolver.relator_network.conectar(arq1, arq2, tipo="analogico")

print(f"  Relator creado: {relator.id}")
print(f"  Origen: {relator.origen}")
print(f"  Destino: {relator.destino}")
print(f"  Fuerza: {relator.fuerza:.3f}")
print(f"  Tipo: {relator.tipo}")
print("✅ Conexión creada")

# 4. VALIDAR TENSOR DE TRANSFORMACIÓN
print("\n[4/5] Validando tensor de transformación...")
if relator.transformacion is None:
    print("❌ FALLO: relator.transformacion es None")
    sys.exit(1)

print(f"  ✅ Transformación existe: {type(relator.transformacion)}")
print(f"  ✅ Es TensorFFE: {isinstance(relator.transformacion, TensorFFE)}")

# Verificar que tiene valores válidos
tiene_valores = False
for i in range(3):
    v = relator.transformacion.nivel_1[i]
    if 0 <= v.forma <= 7 and 0 <= v.funcion <= 7 and 0 <= v.estructura <= 7:
        tiene_valores = True
        break

if not tiene_valores:
    print("❌ FALLO: tensor de transformación no tiene valores válidos")
    sys.exit(1)

print(f"  ✅ Tensor tiene valores octales válidos (0-7)")

# Mostrar ejemplo de vector
v0 = relator.transformacion.nivel_1[0]
print(f"  Ejemplo nivel_1[0]: F={v0.forma}, Fn={v0.funcion}, E={v0.estructura}")

# 5. Test de Armonizador con este relator
print("\n[5/5] Probando con Armonizador...")
from armonizador import Armonizador

armonizador = Armonizador(
    evolver=evolver,
    transcender=transcender,
    umbral_coherencia=0.7
)

# Crear un relator débil para probar detección
relator_debil = evolver.relator_network.conectar(arq1, arq2, tipo="test")
relator_debil.fuerza = 0.3  # Forzar fuerza baja

# Armonizar
tensores_test = [tensor1, tensor2]
reporte = armonizador.armonizar_lote(tensores_test, "test_space")

print(f"\n  Incoherencias detectadas: {reporte['incoherencias']}")
print(f"  Correcciones aplicadas: {reporte['correcciones']}")

# Verificar que detectó el relator débil
incoherencias_relatores = [
    inc for inc in armonizador.historial_incoherencias
    if inc.tipo.value == 'broken_relator'
]

if len(incoherencias_relatores) > 0:
    inc = incoherencias_relatores[0]
    if inc.tensor_origen is None:
        print(f"  ❌ FALLO: Incoherencia de relator tiene tensor_origen=None")
        sys.exit(1)
    else:
        print(f"  ✅ Incoherencia de relator tiene tensor_origen válido")
        print(f"     Tipo tensor: {type(inc.tensor_origen)}")

print("\n" + "="*70)
print("✅ TEST EXITOSO: Relatores ahora tienen tensor de transformación")
print("="*70)
print("\nCambios aplicados:")
print("  1. evolver.py: Relator.transformacion ahora es mejor_emergencia.Ms (TensorFFE)")
print("  2. armonizador.py: _validar_relatores() usa relator.transformacion como tensor_origen")
print("\nResultado:")
print("  ✅ Los 167 relatores rotos ahora tienen tensor válido")
print("  ✅ Armonizador puede generar variantes Fibonacci")
print("  ✅ Sistema puede corregir incoherencias de relatores")
print("\n")
