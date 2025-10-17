"""Monitor de progreso Genesis v1.2"""
import time
import os

print("="*70)
print("MONITOR GENESIS v1.2 - Esperando ejecución completa...")
print("="*70)

target_file = "genesis_v1.2.json"
start_time = time.time()
last_check = 0

while True:
    elapsed = time.time() - start_time
    
    # Verificar si existe el archivo
    if os.path.exists(target_file):
        size = os.path.getsize(target_file)
        print(f"\n✅ ¡COMPLETADO! ({elapsed:.1f}s)")
        print(f"   Archivo: {target_file}")
        print(f"   Tamaño: {size:,} bytes")
        break
    
    # Mostrar progreso cada 10 segundos
    if elapsed - last_check >= 10:
        print(f"  [{int(elapsed)}s] Procesando... (cargando SentenceTransformer)", end="\r")
        last_check = elapsed
    
    # Timeout después de 3 minutos
    if elapsed > 180:
        print(f"\n⚠️ Timeout ({elapsed:.1f}s)")
        print("   Revisar terminal de ejecución")
        break
    
    time.sleep(2)

print("\n" + "="*70)
