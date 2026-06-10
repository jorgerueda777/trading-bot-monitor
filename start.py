"""
Script de inicio que ejecuta el bot y el keep-alive server en paralelo
"""
import asyncio
import sys
import os
from aiohttp import web

async def health_check(request):
    """Endpoint de health check"""
    return web.json_response({'status': 'ok', 'bot': 'running'})

async def root(request):
    """Página principal"""
    return web.Response(text='<h1>🤖 Trading Bot Monitor - Running</h1>', content_type='text/html')

async def start_web_server():
    """Inicia el servidor web INMEDIATAMENTE"""
    port = int(os.environ.get('PORT', 10000))
    
    app = web.Application()
    app.router.add_get('/', root)
    app.router.add_get('/health', health_check)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    
    print(f"✅✅✅ SERVIDOR WEB ACTIVO EN PUERTO {port} ✅✅✅")
    print(f"   Bind: 0.0.0.0:{port}")
    
    # Mantener servidor corriendo
    while True:
        await asyncio.sleep(3600)

async def start_bot():
    """Inicia el bot de Telegram"""
    await asyncio.sleep(3)  # Esperar a que el servidor web esté listo
    print("📱 Iniciando monitor de Telegram...")
    import monitor_grupos
    await monitor_grupos.main()

async def main():
    """Ejecuta servidor web y bot en paralelo"""
    print("🚀 Iniciando Trading Bot con Keep-Alive...")
    
    # Crear ambas tareas
    web_task = asyncio.create_task(start_web_server())
    bot_task = asyncio.create_task(start_bot())
    
    # Esperar ambas
    await asyncio.gather(web_task, bot_task)

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
