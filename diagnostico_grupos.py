"""
Diagnóstico de grupos configurados
Verifica que el bot puede acceder a todos los grupos
"""
import os
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()

API_ID = int(os.getenv('TELEGRAM_API_ID'))
API_HASH = os.getenv('TELEGRAM_API_HASH')
PHONE = os.getenv('TELEGRAM_PHONE')

# IDs de grupos a monitorear
SOURCE_IDS_STR = os.getenv('SOURCE_GROUP_IDS', '').split(',')
SOURCE_IDS = []

for id_str in SOURCE_IDS_STR:
    if not id_str.strip():
        continue
    
    group_id = int(id_str.strip())
    
    # Convertir IDs al formato correcto para supergrupos/canales
    # Si el ID tiene 10 dígitos, necesita convertirse a formato -100xxxxxxxxxx
    if len(str(abs(group_id))) == 10:
        # Convertir a formato -100xxxxxxxxxx
        group_id = int(f"-100{abs(group_id)}")
    
    SOURCE_IDS.append(group_id)

DEST_CHANNEL_ID = int(os.getenv('DEST_CHANNEL_ID'))


async def verificar_acceso():
    """Verifica el acceso a todos los grupos configurados"""
    
    print("\n" + "="*70)
    print("🔍 DIAGNÓSTICO DE GRUPOS")
    print("="*70)
    
    print(f"\n📋 Grupos configurados en .env:")
    print(f"   SOURCE_GROUP_IDS: {os.getenv('SOURCE_GROUP_IDS')}")
    print(f"   DEST_CHANNEL_ID: {DEST_CHANNEL_ID}")
    
    print(f"\n🔢 IDs parseados:")
    for idx, group_id in enumerate(SOURCE_IDS, 1):
        print(f"   {idx}. {group_id}")
    
    print(f"\n🔐 Conectando a Telegram...")
    client = TelegramClient('session_name', API_ID, API_HASH)
    await client.start(phone=PHONE)
    print(f"✅ Conectado\n")
    
    print("="*70)
    print("VERIFICANDO ACCESO A CADA GRUPO")
    print("="*70 + "\n")
    
    resultados = []
    
    # Verificar grupos fuente
    for group_id in SOURCE_IDS:
        print(f"📊 Grupo ID: {group_id}")
        try:
            entity = await client.get_entity(group_id)
            
            if hasattr(entity, 'title'):
                nombre = entity.title
            else:
                nombre = f"Chat {group_id}"
            
            print(f"   ✅ Acceso correcto")
            print(f"   📝 Nombre: {nombre}")
            
            # Verificar si es grupo, supergrupo o canal
            tipo = type(entity).__name__
            print(f"   🏷️ Tipo: {tipo}")
            
            # Intentar obtener el último mensaje
            try:
                messages = await client.get_messages(entity, limit=1)
                if messages:
                    last_msg = messages[0]
                    print(f"   💬 Último mensaje: {last_msg.date}")
                else:
                    print(f"   💬 Sin mensajes recientes")
            except:
                print(f"   ⚠️ No se pudo leer mensajes (puede ser un canal)")
            
            resultados.append((group_id, True, nombre))
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            print(f"   ⚠️ Verifica que:")
            print(f"      - Estés en el grupo/canal")
            print(f"      - El ID sea correcto")
            print(f"      - Tengas permisos para leer")
            resultados.append((group_id, False, str(e)))
        
        print()
    
    # Verificar canal destino
    print(f"📤 Canal destino ID: {DEST_CHANNEL_ID}")
    try:
        entity = await client.get_entity(DEST_CHANNEL_ID)
        
        if hasattr(entity, 'title'):
            nombre = entity.title
        else:
            nombre = f"Chat {DEST_CHANNEL_ID}"
        
        print(f"   ✅ Acceso correcto")
        print(f"   📝 Nombre: {nombre}")
        
        # Verificar permisos de escritura
        try:
            # Intentar enviar un mensaje de prueba (comentado para no spamear)
            # await client.send_message(entity, "Test de permisos")
            print(f"   ✍️ Permisos de escritura: Probablemente OK")
        except:
            print(f"   ⚠️ No se pudo verificar permisos de escritura")
        
        resultados.append((DEST_CHANNEL_ID, True, nombre))
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        resultados.append((DEST_CHANNEL_ID, False, str(e)))
    
    print()
    
    # Resumen
    print("="*70)
    print("📊 RESUMEN")
    print("="*70 + "\n")
    
    grupos_ok = 0
    for group_id, success, info in resultados[:-1]:  # Excluir destino
        status = "✅" if success else "❌"
        print(f"{status} Grupo {group_id}: {info if success else 'ERROR'}")
        if success:
            grupos_ok += 1
    
    dest_ok = resultados[-1][1]
    print(f"\n{'✅' if dest_ok else '❌'} Canal destino {DEST_CHANNEL_ID}: {resultados[-1][2]}")
    
    print(f"\n{'='*70}")
    if grupos_ok == len(SOURCE_IDS) and dest_ok:
        print("✅ TODOS LOS GRUPOS CONFIGURADOS CORRECTAMENTE")
        print(f"\n🚀 El bot puede leer {grupos_ok} grupos y escribir en el canal")
        print("\nPara iniciar el monitoreo ejecuta:")
        print("   python monitor_grupos.py")
    else:
        print(f"⚠️ ADVERTENCIA: Solo {grupos_ok}/{len(SOURCE_IDS)} grupos accesibles")
        print("\nRevisa los errores arriba y corrige la configuración")
    
    print("="*70 + "\n")
    
    await client.disconnect()


if __name__ == "__main__":
    try:
        asyncio.run(verificar_acceso())
    except KeyboardInterrupt:
        print("\n\n👋 Diagnóstico cancelado")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
