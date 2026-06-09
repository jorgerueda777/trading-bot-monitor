"""
Script de inicio que ejecuta el bot y el keep-alive server en paralelo
"""
import asyncio
import sys
from keep_alive import start_server

async def main():
    """Ejecuta bot y servidor en paralelo"""
    print("🚀 Iniciando Trading Bot con Keep-Alive...")
    
    # Iniciar servidor keep-alive PRIMERO (para que Render detecte el puerto)
    print("🌐 Iniciando servidor web...")
    server_task = asyncio.create_task(start_server())
    
    # Esperar un poco para que el servidor se levante
    await asyncio.sleep(2)
    
    # Iniciar bot (importar aquí para evitar conflictos)
    print("📱 Iniciando monitor de Telegram...")
    import monitor_grupos
    bot_task = asyncio.create_task(monitor_grupos.main())
    
    # Esperar ambos
    await asyncio.gather(server_task, bot_task)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Bot detenido por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
