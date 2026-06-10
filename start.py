"""
Script de inicio - Servidor HTTP primero, bot después
"""
import asyncio
import sys
import os
from aiohttp import web

# Puerto para Render
PORT = int(os.environ.get('PORT', 10000))

async def health(request):
    return web.json_response({'status': 'ok'})

async def index(request):
    return web.Response(text='Bot Running', content_type='text/html')

async def start_server():
    """Inicia servidor HTTP INMEDIATAMENTE"""
    app = web.Application()
    app.router.add_get('/', index)
    app.router.add_get('/health', health)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()
    
    print(f"✅ HTTP SERVER RUNNING ON PORT {PORT}")
    
    # Mantener vivo
    while True:
        await asyncio.sleep(3600)

async def start_bot():
    """Inicia bot después de 5 segundos"""
    await asyncio.sleep(5)
    print("📱 Starting Telegram bot...")
    import monitor_grupos
    await monitor_grupos.main()

async def main():
    """Corre ambos en paralelo"""
    print(f"🚀 Starting on port {PORT}...")
    
    # Servidor primero, bot después
    await asyncio.gather(
        start_server(),
        start_bot()
    )

if __name__ == "__main__":
    asyncio.run(main())
