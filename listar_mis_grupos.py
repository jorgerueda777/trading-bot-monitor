"""
Script simple para listar todos tus grupos y canales de Telegram
"""
import os
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.tl.types import Channel, Chat

# Cargar configuración
load_dotenv()

API_ID = int(os.getenv('TELEGRAM_API_ID'))
API_HASH = os.getenv('TELEGRAM_API_HASH')
PHONE = os.getenv('TELEGRAM_PHONE')


async def main():
    print("\n" + "="*70)
    print("📱 LISTANDO TUS GRUPOS Y CANALES DE TELEGRAM")
    print("="*70 + "\n")
    
    # Crear cliente
    client = TelegramClient('session_name', API_ID, API_HASH)
    
    print("🔐 Conectando a Telegram...")
    await client.start(phone=PHONE)
    print("✅ Conectado!\n")
    
    # Obtener todos los diálogos (chats)
    print("📋 Obteniendo lista de grupos y canales...\n")
    dialogs = await client.get_dialogs()
    
    grupos = []
    canales = []
    
    # Clasificar
    for dialog in dialogs:
        entity = dialog.entity
        
        if isinstance(entity, Channel):
            if entity.megagroup:
                # Es un supergrupo
                grupos.append({
                    'id': entity.id,
                    'title': entity.title,
                    'username': entity.username,
                    'tipo': 'Supergrupo',
                    'members': getattr(entity, 'participants_count', 'N/A')
                })
            else:
                # Es un canal
                canales.append({
                    'id': entity.id,
                    'title': entity.title,
                    'username': entity.username,
                    'tipo': 'Canal',
                    'members': getattr(entity, 'participants_count', 'N/A')
                })
        elif isinstance(entity, Chat):
            # Grupo normal
            grupos.append({
                'id': entity.id,
                'title': entity.title,
                'username': None,
                'tipo': 'Grupo',
                'members': getattr(entity, 'participants_count', 'N/A')
            })
    
    # Mostrar grupos
    if grupos:
        print("="*70)
        print("🔹 GRUPOS:")
        print("="*70 + "\n")
        
        for i, g in enumerate(grupos, 1):
            print(f"📁 {i}. {g['title']}")
            print(f"   ID: {g['id']}")
            if g['username']:
                print(f"   Username: @{g['username']}")
            print(f"   Tipo: {g['tipo']}")
            print(f"   Miembros: {g['members']}")
            print()
    
    # Mostrar canales
    if canales:
        print("="*70)
        print("🔸 CANALES:")
        print("="*70 + "\n")
        
        for i, c in enumerate(canales, 1):
            print(f"📢 {i}. {c['title']}")
            print(f"   ID: {c['id']}")
            if c['username']:
                print(f"   Username: @{c['username']}")
            print(f"   Tipo: {c['tipo']}")
            print(f"   Suscriptores: {c['members']}")
            print()
    
    print("="*70)
    print(f"📊 RESUMEN: {len(grupos)} grupos, {len(canales)} canales")
    print("="*70 + "\n")
    
    # Guardar en archivo
    with open('mis_grupos_telegram.txt', 'w', encoding='utf-8') as f:
        f.write("MIS GRUPOS Y CANALES DE TELEGRAM\n")
        f.write("="*70 + "\n\n")
        
        f.write("GRUPOS:\n")
        f.write("-"*70 + "\n\n")
        for g in grupos:
            f.write(f"Nombre: {g['title']}\n")
            f.write(f"ID: {g['id']}\n")
            if g['username']:
                f.write(f"Username: @{g['username']}\n")
            f.write(f"Tipo: {g['tipo']}\n")
            f.write(f"Miembros: {g['members']}\n\n")
        
        f.write("\nCANALES:\n")
        f.write("-"*70 + "\n\n")
        for c in canales:
            f.write(f"Nombre: {c['title']}\n")
            f.write(f"ID: {c['id']}\n")
            if c['username']:
                f.write(f"Username: @{c['username']}\n")
            f.write(f"Tipo: {c['tipo']}\n")
            f.write(f"Suscriptores: {c['members']}\n\n")
    
    print("✅ Lista guardada en: mis_grupos_telegram.txt")
    print("\n📋 SIGUIENTE PASO:")
    print("   1. Revisa 'mis_grupos_telegram.txt'")
    print("   2. Identifica tu grupo de señales")
    print("   3. Copia el ID de ese grupo")
    print("   4. Úsalo para monitorear eventos")
    print()
    
    await client.disconnect()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n❌ Cancelado por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Si es la primera vez, te pedirá un código de verificación.")
        print("   Revisa tu Telegram y ingresa el código que recibes.")
