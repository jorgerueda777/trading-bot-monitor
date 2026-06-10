"""
Script de inicio - Servidor HTTP PRIMERO, luego bot
"""
import os
import asyncio
from aiohttp import web

PORT = int(os.environ.get('PORT', 10000))

# Flag para indicar que el servidor está listo
server_ready = False

async def health(request):
    return web.json_response({'status': 'ok', 'server': 'ready'})

async def index(request):
    return web.Response(text='<h1>Bot Running</h1>', content_type='text/html')

async def run_web_server():
    """Servidor HTTP - Se levanta PRIMERO"""
    global server_ready
    
    app = web.Application()
    app.router.add_get('/', index)
    app.router.add_get('/health', health)
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()
    
    server_ready = True
    print(f"✅✅✅ HTTP SERVER IS RUNNING ON PORT {PORT} ✅✅✅")
    print(f"Server bound to 0.0.0.0:{PORT}")
    
    # Auto-ping cada 30 segundos para evitar sleep de Render
    async def auto_ping():
        """Hace ping al servidor cada 30 segundos para evitar sleep"""
        import aiohttp
        await asyncio.sleep(30)  # Esperar 30 segundos antes del primer ping
        
        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'http://localhost:{PORT}/health', timeout=10) as resp:
                        if resp.status == 200:
                            print("🔄 Auto-ping OK")
            except:
                pass  # Silenciar errores del ping
            
            await asyncio.sleep(30)  # Cada 30 segundos
    
    # Iniciar auto-ping
    asyncio.create_task(auto_ping())
    print("🔄 Auto-ping activado (cada 30 segundos)\n")
    
    # Mantener corriendo forever
    while True:
        await asyncio.sleep(3600)

async def run_telegram_bot():
    """Bot de Telegram - Se inicia DESPUÉS del servidor"""
    global server_ready
    
    # Esperar a que el servidor esté 100% listo
    while not server_ready:
        await asyncio.sleep(0.1)
    
    # Esperar 3 segundos extra por seguridad
    print("⏳ Waiting 3 seconds before starting Telegram bot...")
    await asyncio.sleep(3)
    
    print("📱 Starting Telegram bot...")
    
    # Importar SOLO cuando el servidor ya está corriendo
    import monitor_grupos
    
    # Ejecutar el bot
    await monitor_grupos.main()

async def main():
    print(f"🚀 STARTING SERVICE ON PORT {PORT}")
    
    # Crear ambas tareas
    server = asyncio.create_task(run_web_server())
    bot = asyncio.create_task(run_telegram_bot())
    
    # Ejecutar en paralelo
    await asyncio.gather(server, bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Stopped")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
