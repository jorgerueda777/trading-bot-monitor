"""
Genera un session string de Telegram para usar en Render
"""
import os
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.sessions import StringSession
import asyncio

load_dotenv()

API_ID = int(os.getenv('TELEGRAM_API_ID'))
API_HASH = os.getenv('TELEGRAM_API_HASH')
PHONE = os.getenv('TELEGRAM_PHONE')

async def main():
    print("="*70)
    print("GENERAR SESSION STRING PARA RENDER")
    print("="*70)
    print()
    
    # Crear cliente con sesión de archivo existente
    client = TelegramClient('session_name', API_ID, API_HASH)
    
    print("Conectando a Telegram...")
    await client.connect()
    
    if not await client.is_user_authorized():
        print("❌ No hay sesión autorizada.")
        print("Ejecuta el bot localmente primero (python monitor_grupos.py)")
        return
    
    # Obtener la sesión como string
    session_string = StringSession.save(client.session)
    
    print("✅ Session string generado:")
    print()
    print("="*70)
    print(session_string)
    print("="*70)
    print()
    print("📋 Copia este string y agrégalo como variable de entorno en Render:")
    print("   Key: TELEGRAM_SESSION_STRING")
    print("   Value: [el string de arriba]")
    print()
    
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
