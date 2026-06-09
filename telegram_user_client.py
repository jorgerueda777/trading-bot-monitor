"""
Cliente de Usuario de Telegram (UserBot)
Lee grupos PRIVADOS usando tu cuenta de Telegram
"""
import os
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.tl.types import Channel, Chat
import re

from src.core.classifier import EventClassifier
from src.storage.historical_storage import HistoricalStorage
from src.data_sources.binance_client import BinanceClient

# Cargar variables de entorno
load_dotenv()

# Configuración
API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')
PHONE = os.getenv('TELEGRAM_PHONE')
SOURCE_GROUP_ID = os.getenv('SOURCE_GROUP_ID')  # Grupo de donde leer
DEST_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')  # Token del bot destino

# Inicializar clasificador y Binance
classifier = EventClassifier()
storage = HistoricalStorage()
binance_client = BinanceClient()

# Cliente
client = None


def detectar_evento_en_mensaje(text: str) -> bool:
    """Detecta si un mensaje contiene un evento válido - FIBO o VOLUMEN"""
    if not text:
        return False
    
    # Debe tener símbolo
    tiene_simbolo = bool(re.search(r'#[A-Z]+USDT', text, re.IGNORECASE))
    
    # OPCIÓN 1: Señal de VOLUMEN
    es_volumen = bool(re.search(r'ORIGEN:\s*VOLUMEN', text, re.IGNORECASE))
    tiene_tipo = bool(re.search(r'TIPO:\s*(SOBRECOMPRA|SOBREVENTA)', text, re.IGNORECASE))
    formato_volumen = tiene_simbolo and es_volumen and tiene_tipo
    
    if formato_volumen:
        return True
    
    # OPCIÓN 2: Debe tener la palabra FIBO
    tiene_fibo = bool(re.search(r'FIBO\s*(1H|4H|1D)', text, re.IGNORECASE))
    
    # FORMATO ESTRICTO: SESGO + ORIGEN: FIBO
    tiene_sesgo = bool(re.search(r'SESGO\s+(ALCISTA|BAJISTA)', text, re.IGNORECASE))
    tiene_origen = bool(re.search(r'ORIGEN:\s*FIBO\s+(1H|4H|1D)', text, re.IGNORECASE))
    formato_estricto = tiene_simbolo and tiene_sesgo and tiene_origen
    
    # FORMATO FLEXIBLE: Solo necesita símbolo + FIBO + dirección (SHORT/LONG)
    tiene_direccion = bool(re.search(r'(SHORT|LONG|ALCISTA|BAJISTA|🔴|🟢)', text, re.IGNORECASE))
    formato_flexible = tiene_simbolo and tiene_fibo and tiene_direccion
    
    return formato_estricto or formato_flexible


def obtener_market_data(symbol: str):
    """Obtiene datos de mercado REALES de Binance"""
    return binance_client.get_market_data(symbol)


def formatear_resumen_corto(classification) -> str:
    """Formatea resumen compacto para enviar"""
    if classification.priority == "ALTA PRIORIDAD":
        emoji = "🔥"
    elif classification.priority == "PRIORIDAD MEDIA":
        emoji = "⚠️"
    else:
        emoji = "ℹ️"
    
    mensaje = f"""
{emoji} *EVENTO CLASIFICADO*

*Símbolo:* {classification.symbol}
*Sesgo:* {classification.bias}
*Origen:* {classification.origin}

*Score:* {classification.final_score:.1f}/100
*Prioridad:* {classification.priority}

*Top 3 Factores:*
"""
    
    for i, factor in enumerate(classification.key_factors[:3], 1):
        mensaje += f"{i}. {factor}\n"
    
    return mensaje


async def enviar_a_bot(mensaje: str):
    """Envía mensaje al bot destino"""
    try:
        # Enviar a ti mismo (al chat con el bot)
        await client.send_message('@JR79_BOT', mensaje)
        print("✅ Mensaje enviado a @JR79_BOT")
    except Exception as e:
        print(f"❌ Error enviando a bot: {e}")


async def listar_grupos():
    """Lista todos los grupos/chats donde estás"""
    print("\n" + "="*60)
    print("📋 LISTANDO TODOS TUS GRUPOS Y CHATS")
    print("="*60 + "\n")
    
    dialogs = await client.get_dialogs()
    
    grupos = []
    canales = []
    privados = []
    
    for dialog in dialogs:
        entity = dialog.entity
        
        if isinstance(entity, Channel):
            if entity.megagroup:
                # Supergrupo
                grupos.append({
                    'id': entity.id,
                    'title': entity.title,
                    'username': entity.username,
                    'tipo': 'Supergrupo'
                })
            else:
                # Canal
                canales.append({
                    'id': entity.id,
                    'title': entity.title,
                    'username': entity.username,
                    'tipo': 'Canal'
                })
        elif isinstance(entity, Chat):
            # Grupo normal
            grupos.append({
                'id': entity.id,
                'title': entity.title,
                'username': None,
                'tipo': 'Grupo'
            })
    
    # Mostrar grupos
    if grupos:
        print("🔹 GRUPOS:")
        print("-" * 60)
        for i, g in enumerate(grupos, 1):
            username_str = f"@{g['username']}" if g['username'] else "Sin username"
            print(f"{i}. {g['title']}")
            print(f"   ID: {g['id']}")
            print(f"   Username: {username_str}")
            print(f"   Tipo: {g['tipo']}")
            print()
    
    # Mostrar canales
    if canales:
        print("🔸 CANALES:")
        print("-" * 60)
        for i, c in enumerate(canales, 1):
            username_str = f"@{c['username']}" if c['username'] else "Sin username"
            print(f"{i}. {c['title']}")
            print(f"   ID: {c['id']}")
            print(f"   Username: {username_str}")
            print()
    
    print("="*60)
    print(f"Total: {len(grupos)} grupos, {len(canales)} canales")
    print("="*60 + "\n")
    
    # Guardar en archivo
    with open('mis_grupos_telegram.txt', 'w', encoding='utf-8') as f:
        f.write("MIS GRUPOS Y CANALES DE TELEGRAM\n")
        f.write("="*60 + "\n\n")
        
        f.write("GRUPOS:\n")
        f.write("-"*60 + "\n")
        for g in grupos:
            f.write(f"Nombre: {g['title']}\n")
            f.write(f"ID: {g['id']}\n")
            f.write(f"Tipo: {g['tipo']}\n\n")
        
        f.write("\nCANALES:\n")
        f.write("-"*60 + "\n")
        for c in canales:
            f.write(f"Nombre: {c['title']}\n")
            f.write(f"ID: {c['id']}\n\n")
    
    print("✅ Lista guardada en: mis_grupos_telegram.txt")
    
    return grupos, canales


async def monitorear_grupo(group_id: int):
    """Monitorea un grupo específico para eventos"""
    print("\n" + "="*60)
    print(f"👁️ MONITOREANDO GRUPO ID: {group_id}")
    print("="*60 + "\n")
    
    # Obtener info del grupo
    try:
        entity = await client.get_entity(group_id)
        if hasattr(entity, 'title'):
            print(f"📱 Grupo: {entity.title}")
        print("✅ Conexión establecida")
        print("🔍 Esperando eventos...\n")
    except Exception as e:
        print(f"❌ Error: No se pudo acceder al grupo {group_id}")
        print(f"   Verifica que el ID sea correcto y que estés en el grupo")
        return
    
    @client.on(events.NewMessage(chats=group_id))
    async def handler(event):
        """Maneja mensajes nuevos del grupo"""
        try:
            mensaje = event.message.message
            
            if not mensaje:
                return
            
            # Detectar si es un evento
            if detectar_evento_en_mensaje(mensaje):
                print(f"\n{'='*60}")
                print(f"🔍 EVENTO DETECTADO!")
                print(f"{'='*60}")
                print(f"Mensaje:\n{mensaje[:100]}...")
                print()
                
                # Extraer símbolo
                match = re.search(r'#([A-Z0-9]+)', mensaje)
                symbol = match.group(1) if match else "UNKNOWN"
                
                # Obtener datos de mercado REALES
                market_data = obtener_market_data(symbol)
                
                # Clasificar
                print("⚙️ Clasificando evento...")
                resultado = classifier.classify_event(
                    mensaje,
                    market_data,
                    datetime.now()
                )
                
                print(f"✅ Clasificado: {resultado.final_score:.1f}/100 - {resultado.priority}")
                
                # Guardar
                storage.save_classification(resultado.model_dump())
                
                # Formatear resumen
                resumen = formatear_resumen_corto(resultado)
                
                # Enviar a bot destino
                print("📤 Enviando a @JR79_BOT...")
                await enviar_a_bot(resumen)
                
                print(f"{'='*60}\n")
        
        except Exception as e:
            print(f"❌ Error procesando mensaje: {e}")
    
    # Mantener el cliente corriendo
    print("✅ Monitoreo activo. Presiona Ctrl+C para detener.\n")
    await client.run_until_disconnected()


async def main():
    """Función principal"""
    global client
    
    print("\n" + "="*60)
    print("🤖 CLIENTE DE USUARIO DE TELEGRAM")
    print("   Lee grupos PRIVADOS con tu cuenta")
    print("="*60 + "\n")
    
    # Verificar configuración
    if not API_ID or not API_HASH:
        print("❌ ERROR: Falta configuración")
        print("\n📋 Necesitas obtener tus credenciales de Telegram:")
        print("1. Ve a: https://my.telegram.org")
        print("2. Inicia sesión con tu número de teléfono")
        print("3. Ve a 'API Development Tools'")
        print("4. Crea una aplicación")
        print("5. Copia 'api_id' y 'api_hash'")
        print("6. Añádelos al archivo .env:")
        print("   TELEGRAM_API_ID=tu_api_id")
        print("   TELEGRAM_API_HASH=tu_api_hash")
        print("   TELEGRAM_PHONE=+34123456789")
        return
    
    # Crear cliente
    client = TelegramClient('session_name', int(API_ID), API_HASH)
    
    print("🔐 Conectando a Telegram...")
    await client.start(phone=PHONE if PHONE else None)
    print("✅ Conectado!\n")
    
    # Menú
    while True:
        print("\n" + "="*60)
        print("MENÚ - ¿Qué quieres hacer?")
        print("="*60)
        print("1. Listar todos mis grupos y canales")
        print("2. Monitorear un grupo específico (leer eventos)")
        print("3. Salir")
        print("="*60)
        
        opcion = input("\nElige una opción (1-3): ").strip()
        
        if opcion == "1":
            # Listar grupos
            await listar_grupos()
            input("\nPresiona Enter para continuar...")
        
        elif opcion == "2":
            # Monitorear grupo
            if SOURCE_GROUP_ID:
                print(f"\n✅ Grupo configurado en .env: {SOURCE_GROUP_ID}")
                usar = input("¿Usar este grupo? (s/n): ").strip().lower()
                if usar == 's':
                    group_id = int(SOURCE_GROUP_ID)
                else:
                    group_id = input("Ingresa el ID del grupo (número): ").strip()
                    try:
                        group_id = int(group_id)
                    except:
                        print("❌ ID inválido")
                        continue
            else:
                print("\n📋 Primero lista tus grupos (opción 1) para ver los IDs")
                group_id = input("Ingresa el ID del grupo (número): ").strip()
                try:
                    group_id = int(group_id)
                except:
                    print("❌ ID inválido")
                    continue
            
            # Iniciar monitoreo
            await monitorear_grupo(group_id)
            break
        
        elif opcion == "3":
            print("\n👋 Cerrando...")
            break
        
        else:
            print("❌ Opción inválida")
    
    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
