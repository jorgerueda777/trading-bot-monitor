"""
Keep-Alive Server para Render Web Service
Evita que el servicio se suspenda cada 15 minutos
"""
from aiohttp import web
import asyncio
from datetime import datetime

# Estado global
bot_status = {
    'status': 'running',
    'started_at': datetime.now().isoformat(),
    'last_ping': datetime.now().isoformat()
}

async def health_check(request):
    """Endpoint de health check"""
    bot_status['last_ping'] = datetime.now().isoformat()
    return web.json_response({
        'status': 'ok',
        'bot_status': bot_status['status'],
        'started_at': bot_status['started_at'],
        'last_ping': bot_status['last_ping'],
        'uptime': 'running'
    })

async def root(request):
    """Página principal"""
    html = f"""
    <html>
        <head>
            <title>Trading Bot Monitor</title>
            <meta http-equiv="refresh" content="240">
        </head>
        <body>
            <h1>🤖 Trading Bot Monitor</h1>
            <p>✅ Bot Status: {bot_status['status']}</p>
            <p>🕐 Started: {bot_status['started_at']}</p>
            <p>📡 Last Ping: {bot_status['last_ping']}</p>
            <p><small>Auto-refresh every 4 minutes</small></p>
        </body>
    </html>
    """
    return web.Response(text=html, content_type='text/html')

async def start_server(port=10000):
    """Inicia el servidor web"""
    app = web.Application()
    app.router.add_get('/', root)
    app.router.add_get('/health', health_check)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    
    print(f"🌐 Keep-alive server iniciado en puerto {port}")
    print(f"   Health check: http://0.0.0.0:{port}/health")
    
    # Mantener el servidor corriendo
    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    asyncio.run(start_server())
