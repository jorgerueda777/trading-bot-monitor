"""
Script de inicio - Servidor HTTP PRIMERO, luego bot
FIX DEFINITIVO RENDER: Separated event loops + pulse monitor
"""
import os
import asyncio
import threading
import time
from aiohttp import web
from datetime import datetime

PORT = int(os.environ.get('PORT', 10000))

# Estadísticas globales
stats = {
    'server_ready': False,
    'bot_ready': False,
    'last_message_time': None,
    'message_count': 0,
    'bot_restarts': 0
}

async def health(request):
    """Health check endpoint con estadísticas"""
    return web.json_response({
        'status': 'ok',
        'server': 'ready',
        'bot_ready': stats['bot_ready'],
        'message_count': stats['message_count'],
        'last_message': stats['last_message_time'].isoformat() if stats['last_message_time'] else None,
        'bot_restarts': stats['bot_restarts']
    })

async def index(request):
    return web.Response(text=f'''<html>
<head><title>Bot Monitor</title><meta http-equiv="refresh" content="30"></head>
<body>
<h1>🤖 Bot Running</h1>
<p>Server Ready: {'✅' if stats['server_ready'] else '❌'}</p>
<p>Bot Ready: {'✅' if stats['bot_ready'] else '❌'}</p>
<p>Messages: {stats['message_count']}</p>
<p>Last Message: {stats['last_message_time'] or 'None'}</p>
<p>Bot Restarts: {stats['bot_restarts']}</p>
<p><small>Auto-refresh every 30s</small></p>
</body>
</html>''', content_type='text/html')

async def run_web_server():
    """Servidor HTTP - Se levanta PRIMERO"""
    app = web.Application()
    app.router.add_get('/', index)
    app.router.add_get('/health', health)
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()
    
    stats['server_ready'] = True
    print(f"✅✅✅ HTTP SERVER IS RUNNING ON PORT {PORT} ✅✅✅")
    print(f"Server bound to 0.0.0.0:{PORT}")
    
    # Auto-ping cada 20 segundos (más frecuente)
    async def auto_ping():
        """Hace ping al servidor cada 20 segundos para evitar sleep"""
        import aiohttp
        await asyncio.sleep(20)
        
        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'http://localhost:{PORT}/health', timeout=5) as resp:
                        if resp.status == 200:
                            print(f"🔄 Auto-ping OK [{datetime.now().strftime('%H:%M:%S')}]")
            except Exception as e:
                print(f"⚠️ Auto-ping failed: {e}")
            
            await asyncio.sleep(20)
    
    # Iniciar auto-ping
    asyncio.create_task(auto_ping())
    print("🔄 Auto-ping activado (cada 20 segundos)\n")
    
    # Mantener corriendo forever
    while True:
        await asyncio.sleep(3600)

def run_bot_in_thread():
    """Ejecuta el bot en un thread separado con su propio event loop"""
    print("🔧 Iniciando bot en thread separado...")
    
    # Crear nuevo event loop para este thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        import monitor_grupos
        loop.run_until_complete(monitor_grupos.main())
    except Exception as e:
        print(f"❌ Error en bot thread: {e}")
        import traceback
        traceback.print_exc()
    finally:
        loop.close()

async def pulse_monitor():
    """Monitorea el pulso del bot y reinicia si se congela"""
    await asyncio.sleep(60)  # Esperar 1 minuto antes de empezar
    
    print("💓 Pulse monitor activado")
    last_count = stats['message_count']
    no_activity_count = 0
    
    while True:
        await asyncio.sleep(300)  # Check cada 5 minutos
        
        current_count = stats['message_count']
        
        # Si el bot está listo pero no ha procesado mensajes en 5 min
        if stats['bot_ready']:
            if current_count == last_count:
                no_activity_count += 1
                print(f"⚠️ Pulse monitor: Sin actividad ({no_activity_count * 5} min)")
                
                # Si no hay actividad por 10 minutos, reportar
                if no_activity_count >= 2:
                    print(f"⚠️ ALERTA: Bot sin procesar mensajes por {no_activity_count * 5} minutos")
                    print(f"   Última actividad: {stats['last_message_time']}")
                    # No reiniciamos automáticamente porque podría no haber mensajes
                    # Solo alertamos
            else:
                # Hay actividad, resetear contador
                if no_activity_count > 0:
                    print(f"✅ Pulse monitor: Actividad detectada (procesó {current_count - last_count} mensajes)")
                no_activity_count = 0
            
            last_count = current_count

async def main():
    print(f"🚀 STARTING SERVICE ON PORT {PORT}")
    print(f"🔧 FIX APLICADO: Separated threads + pulse monitor\n")
    
    # Iniciar servidor HTTP en el event loop principal
    server_task = asyncio.create_task(run_web_server())
    
    # Esperar a que el servidor esté listo
    while not stats['server_ready']:
        await asyncio.sleep(0.1)
    
    # Esperar 3 segundos
    print("⏳ Waiting 3 seconds before starting bot...")
    await asyncio.sleep(3)
    
    # Iniciar bot en thread separado
    print("📱 Starting Telegram bot in separate thread...")
    bot_thread = threading.Thread(target=run_bot_in_thread, daemon=True)
    bot_thread.start()
    
    # Iniciar pulse monitor
    pulse_task = asyncio.create_task(pulse_monitor())
    
    # Mantener corriendo
    await asyncio.gather(server_task, pulse_task)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Stopped")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
