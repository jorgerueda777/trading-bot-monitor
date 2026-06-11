"""
Script para generar session string con NUEVO número de teléfono
Número: +33753973592
"""
from telethon import TelegramClient
from telethon.sessions import StringSession
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv('TELEGRAM_API_ID'))
API_HASH = os.getenv('TELEGRAM_API_HASH')
PHONE = '+33753973592'  # NUEVO NÚMERO

async def main():
    print("="*70)
    print("🔐 GENERADOR DE SESSION STRING - NUEVO NÚMERO")
    print("="*70)
    print(f"\n📱 Número: {PHONE}")
    print(f"🔑 API ID: {API_ID}")
    print(f"🔑 API Hash: {API_HASH[:10]}...")

    print("\n⚠️ IMPORTANTE:")
    print("   1. Recibirás un código en Telegram en este número: +33753973592")
    print("   2. Ingresa el código cuando se te pida")
    print("   3. Si tienes 2FA, ingresa tu contraseña")
    print("\n")

    client = TelegramClient(StringSession(), API_ID, API_HASH)
    
    await client.connect()
    
    if not await client.is_user_authorized():
        await client.send_code_request(PHONE)
        print(f"📱 Código enviado a {PHONE}")
        code = input("🔢 Ingresa el código que recibiste: ")
        
        try:
            await client.sign_in(PHONE, code)
        except Exception as e:
            if 'Two-steps verification' in str(e) or 'SessionPasswordNeeded' in str(type(e).__name__):
                password = input("🔐 Ingresa tu contraseña 2FA: ")
                try:
                    await client.sign_in(password=password)
                except Exception as e2:
                    print(f"\n❌ Error: {e2}")
                    print("⚠️ La contraseña 2FA es incorrecta. Verifica e intenta de nuevo.")
                    await client.disconnect()
                    return
            else:
                raise e
    
    print("\n✅ Conectado a Telegram!")
    print("\n" + "="*70)
    print("🎉 SESSION STRING GENERADO:")
    print("="*70)
    session_string = client.session.save()
    print(session_string)
    print("="*70)
    
    # Guardar en archivo
    with open('SESSION_STRING_NUEVO.txt', 'w') as f:
        f.write(session_string)
    
    print("\n✅ Session string guardado en: SESSION_STRING_NUEVO.txt")
    print("\n📋 SIGUIENTE PASO:")
    print("   1. Copia el session string de arriba")
    print("   2. Ve a Render > Environment")
    print("   3. Actualiza TELEGRAM_SESSION_STRING con el nuevo valor")
    print("   4. Actualiza TELEGRAM_PHONE=+33753973592")
    print("   5. Guarda y el servicio se reiniciará automáticamente")
    print("\n")
    
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
