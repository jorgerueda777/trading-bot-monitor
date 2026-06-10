"""
Monitor de Grupos - Lee múltiples grupos y envía resultados a un canal
"""
import os
import asyncio
import re
from datetime import datetime
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.tl.types import Channel, Chat
from aiohttp import web

from src.core.classifier import EventClassifier
from src.storage.historical_storage import HistoricalStorage
from src.data_sources.binance_client import BinanceClient
from src.tracking.event_tracker import EventTracker, EventStatus

# Cargar configuración
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
    SOURCE_IDS.append(group_id)

print(f"📋 Grupos configurados: {SOURCE_IDS}")

# Canal destino
DEST_CHANNEL_ID = int(os.getenv('DEST_CHANNEL_ID'))

# Convertir a formato de canal si es necesario (Telegram usa -100 prefix para canales)
# Si el ID es positivo y no empieza con -100, convertirlo
if DEST_CHANNEL_ID > 0:
    DEST_CHANNEL_ID = int(f"-100{DEST_CHANNEL_ID}")

# Inicializar clasificador y clientes
classifier = EventClassifier()
storage = HistoricalStorage()
binance_client = BinanceClient()
event_tracker = EventTracker()

# Cliente de Telegram global
client = None
# Diccionario para trackear mensajes enviados (event_id -> message_id)
mensajes_tracking = {}
# Timestamp del último mensaje recibido (para watchdog)
last_message_time = datetime.now()


def detectar_evento_en_mensaje(text: str) -> bool:
    """Detecta si un mensaje contiene un evento válido - FIBO o VOLUMEN"""
    if not text:
        return False
    
    # Debe tener símbolo
    tiene_simbolo = bool(re.search(r'#[A-Z]+USDT', text, re.IGNORECASE))
    
    # OPCIÓN 1: Señal de VOLUMEN (formato explícito)
    es_volumen = bool(re.search(r'ORIGEN:\s*VOLUMEN', text, re.IGNORECASE))
    tiene_tipo = bool(re.search(r'TIPO:\s*(SOBRECOMPRA|SOBREVENTA)', text, re.IGNORECASE))
    formato_volumen_explicito = tiene_simbolo and es_volumen and tiene_tipo
    
    if formato_volumen_explicito:
        return True
    
    # OPCIÓN 2: Señal de VOLUMEN (formato simplificado con ENTRADA y TP)
    tiene_direccion = bool(re.search(r'(SHORT|LONG|🔴|🟢)', text, re.IGNORECASE))
    tiene_entrada = bool(re.search(r'(ENTRADA|🎯|ENTRY)', text, re.IGNORECASE))
    tiene_tp = bool(re.search(r"(TP'?S?|OBJETIVO|TARGET|🚀)", text, re.IGNORECASE))
    formato_volumen_simple = tiene_simbolo and tiene_direccion and (tiene_entrada or tiene_tp)
    
    if formato_volumen_simple:
        return True
    
    # OPCIÓN 3: Debe tener la palabra FIBO
    tiene_fibo = bool(re.search(r'FIBO\s*(1H|4H|1D)', text, re.IGNORECASE))
    
    # FORMATO ESTRICTO: SESGO + ORIGEN: FIBO
    tiene_sesgo = bool(re.search(r'SESGO\s+(ALCISTA|BAJISTA)', text, re.IGNORECASE))
    tiene_origen = bool(re.search(r'ORIGEN:\s*FIBO\s+(1H|4H|1D)', text, re.IGNORECASE))
    formato_estricto = tiene_simbolo and tiene_sesgo and tiene_origen
    
    # FORMATO FLEXIBLE: Solo necesita símbolo + FIBO + dirección (SHORT/LONG)
    formato_flexible = tiene_simbolo and tiene_fibo and tiene_direccion
    
    return formato_estricto or formato_flexible


def obtener_market_data(symbol: str):
    """Obtiene datos de mercado REALES de Binance"""
    try:
        print(f"   📊 Consultando Binance para {symbol}...")
        data = binance_client.get_market_data(symbol)
        print(f"   ✅ Datos obtenidos: precio=${data['current_price']:.2f}, OI={data['open_interest']['trend']}")
        return data
    except Exception as e:
        print(f"   ⚠️ Error obteniendo datos de Binance: {e}")
        print(f"   🔄 Usando datos de respaldo...")
        return binance_client._get_fallback_data()


def formatear_resumen_telegram(classification, grupo_origen, status=EventStatus.EN_ANALISIS, resumen_tracking=None) -> str:
    """Formatea resumen COMPACTO para Telegram - Solo info esencial"""
    
    # Determinar dirección SHORT/LONG
    if classification.bias.upper() in ['BEARISH', 'BAJISTA']:
        direccion = "🔴 SHORT"
    else:
        direccion = "🟢 LONG"
    
    # Emoji según estado
    if status == EventStatus.ALTA_PRIORIDAD:
        emoji = "🚀"
    elif status == EventStatus.FUERTE:
        emoji = "💪"
    else:
        emoji = "🔄"
    
    # FORMATO COMPACTO
    mensaje = f"""{emoji} **{classification.symbol}** {direccion} | Score: **{classification.final_score:.0f}**/100

**{status.value}**"""
    
    # Agregar evolución de scores si hay tracking
    if resumen_tracking and status != EventStatus.EN_ANALISIS:
        # Extraer solo la evolución de scores del resumen
        lines = resumen_tracking.split('\n')
        for line in lines:
            if 'Inicial:' in line or 'Actual:' in line or 'Máximo:' in line:
                mensaje += f"\n{line.strip()}"
            elif 'Tendencia:' in line:
                mensaje += f"\n{line.strip()}"
            elif 'EVOLUCIÓN:' in line:
                # Buscar la siguiente línea con los scores
                idx = lines.index(line)
                if idx + 1 < len(lines):
                    mensaje += f"\n📈 {lines[idx + 1].strip()}"
            elif 'PRECIO:' in line:
                # Incluir sección de precio
                idx = lines.index(line)
                for i in range(idx, min(idx + 4, len(lines))):
                    if lines[i].strip() and not lines[i].startswith('━'):
                        mensaje += f"\n{lines[i].strip()}"
    
    # Info básica adicional
    mensaje += f"\n\n📊 {classification.origin}"
    
    # Precio de entrada
    if hasattr(classification, 'zone_a') and classification.zone_a > 0:
        mensaje += f"\n🎯 Entrada: ${classification.zone_a:.4f}"
        # Segunda entrada si existe y es diferente
        if hasattr(classification, 'zone_b') and classification.zone_b > 0 and classification.zone_b != classification.zone_a:
            mensaje += f" | ${classification.zone_b:.4f}"
    
    # Targets (TPs)
    if hasattr(classification, 'target_a') and classification.target_a > 0:
        mensaje += f"\n🚀 TP1: ${classification.target_a:.4f}"
        # Segundo TP si existe y es diferente
        if hasattr(classification, 'target_b') and classification.target_b > 0 and classification.target_b != classification.target_a:
            mensaje += f" | TP2: ${classification.target_b:.4f}"
    
    # Stop Loss
    if hasattr(classification, 'stop_loss') and classification.stop_loss > 0:
        mensaje += f"\n🛑 SL: ${classification.stop_loss:.4f}"
    
    mensaje += f"\n⏰ {classification.evaluated_at.strftime('%H:%M:%S')}"
    
    return mensaje


async def enviar_a_canal(mensaje: str, edit_message_id=None):
    """Envía mensaje al canal destino o edita uno existente"""
    try:
        if edit_message_id:
            # Editar mensaje existente
            await client.edit_message(DEST_CHANNEL_ID, edit_message_id, mensaje, parse_mode='md')
            print(f"✅ Mensaje actualizado en el canal (ID: {DEST_CHANNEL_ID})")
            return edit_message_id
        else:
            # Enviar nuevo mensaje
            sent_message = await client.send_message(DEST_CHANNEL_ID, mensaje, parse_mode='md')
            print(f"✅ Mensaje enviado al canal (ID: {DEST_CHANNEL_ID})")
            return sent_message.id
    except Exception as e:
        print(f"❌ Error enviando/editando mensaje en canal: {e}")
        return None


async def obtener_nombre_grupo(group_id):
    """Obtiene el nombre del grupo"""
    try:
        entity = await client.get_entity(group_id)
        if hasattr(entity, 'title'):
            return entity.title
        return f"Grupo {group_id}"
    except:
        return f"Grupo {group_id}"


async def tracking_callback(evento_tracked):
    """Callback cuando un evento cambia de estado (ejecutar o descartar)"""
    print(f"\n🔔 Evento {evento_tracked.event_id} cambió a: {evento_tracked.status.value}")
    
    # FILTRO: Solo enviar ALTA PRIORIDAD y FUERTE
    if evento_tracked.status not in [EventStatus.ALTA_PRIORIDAD, EventStatus.FUERTE]:
        print(f"   🔇 Estado {evento_tracked.status.value} no se notifica (filtrado)")
        # Limpiar tracking sin enviar mensaje
        if evento_tracked.event_id in mensajes_tracking:
            # Eliminar el mensaje inicial de j77
            message_id = mensajes_tracking.get(evento_tracked.event_id)
            if message_id:
                try:
                    await client.delete_messages(DEST_CHANNEL_ID, message_id)
                    print(f"   🗑️ Mensaje inicial eliminado de j77 (señal filtrada)")
                except:
                    pass
            del mensajes_tracking[evento_tracked.event_id]
        return
    
    # Obtener el ID del mensaje original
    message_id = mensajes_tracking.get(evento_tracked.event_id)
    if not message_id:
        print(f"⚠️ No se encontró mensaje original para evento {evento_tracked.event_id}")
        return
    
    # Re-clasificar con datos finales
    market_data = binance_client.get_market_data(evento_tracked.symbol)
    classification = classifier.classify_event(
        evento_tracked.original_message,
        market_data,
        datetime.now()
    )
    
    # Obtener nombre del grupo origen (lo extraemos del mensaje original)
    grupo_origen = "Grupo Desconocido"  # Podríamos mejorarlo guardando esta info
    
    # Generar resumen de tracking
    resumen_tracking = event_tracker.obtener_resumen_estado(evento_tracked.event_id)
    
    # Formatear mensaje actualizado
    mensaje_actualizado = formatear_resumen_telegram(
        classification,
        grupo_origen,
        status=evento_tracked.status,
        resumen_tracking=resumen_tracking
    )
    
    # Editar el mensaje en Telegram
    print(f"   📤 Actualizando mensaje en j77 ({evento_tracked.status.value})")
    await enviar_a_canal(mensaje_actualizado, edit_message_id=message_id)
    
    # Limpiar tracking
    if evento_tracked.event_id in mensajes_tracking:
        del mensajes_tracking[evento_tracked.event_id]


async def main():
    global client
    
    print("\n" + "="*70)
    print("🤖 MONITOR DE GRUPOS - Motor de Clasificación")
    print("="*70 + "\n")
    
    if not SOURCE_IDS:
        print("❌ ERROR: No hay grupos configurados en SOURCE_GROUP_IDS")
        return
    
    # Crear cliente - usar StringSession si está disponible, sino archivo
    from telethon.sessions import StringSession
    
    session_string = os.getenv('TELEGRAM_SESSION_STRING', '').strip()
    
    # Configurar cliente con opciones de keep-alive
    if session_string:
        print("📱 Usando sesión de string...")
        client = TelegramClient(
            StringSession(session_string), 
            API_ID, 
            API_HASH,
            connection_retries=5,
            retry_delay=3,
            auto_reconnect=True,
            timeout=60
        )
    else:
        print("📁 Usando sesión de archivo (session_name.session)...")
        client = TelegramClient(
            'session_name', 
            API_ID, 
            API_HASH,
            connection_retries=5,
            retry_delay=3,
            auto_reconnect=True,
            timeout=60
        )
    
    print("🔐 Conectando a Telegram...")
    
    # Conectar sin pedir input
    try:
        await client.connect()
        
        # Si no está autorizado, fallar sin pedir código
        if not await client.is_user_authorized():
            print("❌ ERROR: Sesión no autorizada")
            if session_string:
                print("⚠️ El TELEGRAM_SESSION_STRING no es válido")
            else:
                print("⚠️ El archivo session_name.session debe estar en el repositorio")
                print("   y contener una sesión válida de Telegram")
            await client.disconnect()
            return
        
        print("✅ Conectado!\n")
        
    except Exception as e:
        print(f"❌ Error conectando a Telegram: {e}")
        return
    
    # Obtener nombres de grupos
    print("📋 Grupos a monitorear:")
    nombres_grupos = {}
    for group_id in SOURCE_IDS:
        nombre = await obtener_nombre_grupo(group_id)
        nombres_grupos[group_id] = nombre
        print(f"   • {nombre} (ID: {group_id})")
    
    # Obtener nombre del canal destino
    nombre_destino = await obtener_nombre_grupo(DEST_CHANNEL_ID)
    print(f"\n📤 Canal destino:")
    print(f"   • {nombre_destino} (ID: {DEST_CHANNEL_ID})")
    
    print("\n" + "="*70)
    print("✅ Monitoreo iniciado - Esperando eventos...")
    print("="*70 + "\n")
    
    # Iniciar loop de tracking en segundo plano
    asyncio.create_task(event_tracker.monitor_loop(callback=tracking_callback))
    print("🔄 Sistema de seguimiento activado")
    print("   ⚡ Intervalos dinámicos: 10seg (VOLUMEN), 15seg (FIBO)")
    print("   🎯 Umbral unificado: 75 para ALTA PRIORIDAD")
    print("   📊 Nueva escala: RUIDO<50, INTERESANTE 50-59, FUERTE 60-74, ALTA≥75\n")
    
    # Agregar heartbeat task para verificar conexión
    async def heartbeat():
        """Verifica periódicamente que la conexión esté activa"""
        while True:
            try:
                await asyncio.sleep(60)  # Cada minuto
                # Hacer una llamada simple para verificar conexión
                await client.get_me()
                print("💓 Heartbeat: Conexión activa")
            except Exception as e:
                print(f"⚠️ Heartbeat falló: {e}")
                print("🔄 Forzando reconexión...")
                try:
                    await client.disconnect()
                    await asyncio.sleep(2)
                    await client.connect()
                    print("✅ Reconectado exitosamente")
                except Exception as reconnect_error:
                    print(f"❌ Error en reconexión: {reconnect_error}")
    
    # Iniciar heartbeat
    asyncio.create_task(heartbeat())
    print("💓 Heartbeat activado (verifica conexión cada 60 segundos)\n")
    
    # Watchdog para detectar si dejamos de recibir mensajes
    async def watchdog():
        """Detecta si el handler dejó de recibir mensajes"""
        global last_message_time
        while True:
            await asyncio.sleep(180)  # Cada 3 minutos
            time_since_last = (datetime.now() - last_message_time).total_seconds()
            if time_since_last > 600:  # 10 minutos sin mensajes
                print(f"⚠️ WATCHDOG: Sin mensajes por {time_since_last/60:.1f} minutos")
                print(f"🔄 Forzando verificación de conexión...")
                try:
                    me = await client.get_me()
                    print(f"✅ Conexión OK - Usuario: {me.first_name}")
                except Exception as e:
                    print(f"❌ Conexión perdida: {e}")
                    raise Exception("Conexión perdida - reiniciando")
    
    asyncio.create_task(watchdog())
    print("🐕 Watchdog activado (detecta freeze cada 3 minutos)\n")
    
    # Handler para nuevos mensajes
    @client.on(events.NewMessage(chats=SOURCE_IDS))
    async def handler(event):
        """Procesa mensajes de los grupos monitoreados"""
        global last_message_time
        last_message_time = datetime.now()
        print(f"🔔 [HANDLER] Mensaje recibido - {datetime.now().strftime('%H:%M:%S')}")
        try:
            mensaje = event.message.message
            grupo_id = event.chat_id
            grupo_nombre = nombres_grupos.get(grupo_id, f"Grupo {grupo_id}")
            
            # MOSTRAR TODOS LOS MENSAJES (para debug)
            print(f"\n📩 Mensaje recibido de: {grupo_nombre}")
            if mensaje:
                preview = mensaje[:100].replace('\n', ' ')
                print(f"   Preview: {preview}...")
            else:
                print(f"   (mensaje vacío o media)")
            
            if not mensaje:
                return
            
            # Detectar si es un evento
            es_evento = detectar_evento_en_mensaje(mensaje)
            
            if es_evento:
                print(f"\n{'='*70}")
                print(f"🔍 EVENTO DETECTADO en: {grupo_nombre}")
                print(f"{'='*70}")
                print(f"Mensaje completo:\n{mensaje[:300]}...")
                print()
                
                # Extraer símbolo
                match = re.search(r'#([A-Z0-9]+)', mensaje)
                symbol = match.group(1) if match else "UNKNOWN"
                
                # Extraer sesgo
                match_bias = re.search(r'SESGO\s+(ALCISTA|BAJISTA)', mensaje, re.IGNORECASE)
                if not match_bias:
                    match_bias = re.search(r'(LONG|SHORT)', mensaje, re.IGNORECASE)
                bias = match_bias.group(1).upper() if match_bias else "UNKNOWN"
                
                # Convertir a formato estándar
                if bias in ["ALCISTA", "LONG"]:
                    bias = "BULLISH"
                elif bias in ["BAJISTA", "SHORT"]:
                    bias = "BEARISH"
                
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
                
                # ============================================
                # EXTRACCIÓN CRÍTICA DE PRECIOS DE ENTRADA
                # ============================================
                # El resultado ya contiene zone_a y zone_b del parser interno
                entry_1 = resultado.zone_a
                entry_2 = resultado.zone_b
                
                # Log detallado de extracción
                print(f"   📍 PARSER DE ENTRADA:")
                print(f"      Entrada 1: {entry_1}")
                print(f"      Entrada 2: {entry_2}")
                print(f"      Símbolo: {resultado.symbol}")
                print(f"      Origen: {resultado.origin}")
                
                # Validación obligatoria
                if entry_1 == 0.0 or entry_1 == 1.0:
                    print(f"   ⚠️ WARNING: Entrada sospechosa detectada (entry_1={entry_1})")
                    print(f"   ❌ ERROR: No se pudo extraer precio de entrada válido del mensaje")
                    print(f"   📄 Mensaje original (primeras líneas):")
                    for line in mensaje.split('\n')[:10]:
                        print(f"      {line}")
                    print(f"   ℹ️ El sistema NO continuará con valores por defecto")
                    print(f"   🚫 Señal ignorada por error de parsing\n")
                    return  # Saltar esta señal, no procesarla
                
                # Seleccionar precio de referencia
                # Usar zona A como referencia principal
                entry_price = entry_1
                
                # Verificar que el precio sea razonable
                current_price = market_data.get('current_price', 0.0)
                if current_price > 0:
                    # Calcular diferencia porcentual
                    diff_pct = abs((entry_price - current_price) / current_price) * 100
                    
                    # Si la diferencia es >50%, posible error de parsing
                    if diff_pct > 50:
                        print(f"   ⚠️ WARNING: Gran diferencia entre entrada y precio actual:")
                        print(f"      Entrada parseada: ${entry_price:.8f}")
                        print(f"      Precio actual: ${current_price:.8f}")
                        print(f"      Diferencia: {diff_pct:.2f}%")
                        print(f"   ⚠️ Posible error de parsing - revisar mensaje:")
                        print(f"      {mensaje[:200]}")
                
                print(f"   ✅ Precio entrada validado: ${entry_price:.8f}")
                print(f"   📊 Precio actual mercado: ${current_price:.8f}")
                
                print(f"✅ Clasificado: {resultado.final_score:.1f}/100 - {resultado.priority}")
                
                # Guardar en histórico
                storage.save_classification(resultado.model_dump())
                
                # Generar ID único para el evento
                event_id = f"{symbol}_{int(datetime.now().timestamp())}"
                
                # Agregar al tracker
                evento_tracked = event_tracker.agregar_evento(
                    event_id=event_id,
                    symbol=symbol,
                    bias=bias,
                    original_message=mensaje,
                    market_data=market_data,
                    score=resultado.final_score,
                    origin=resultado.origin,  # CRÍTICO: Pasar el origen (FIBO_XX o VOLUMEN)
                    entry_price=entry_price  # Precio de entrada validado
                )
                
                print(f"🔄 Evento agregado al seguimiento (ID: {event_id})")
                
                # Obtener intervalo de check
                check_interval = getattr(evento_tracked, 'check_interval', 15)
                
                # Mostrar tiempos según origen y score
                if resultado.origin == "VOLUMEN":
                    print(f"   📊 Tipo: VOLUMEN (1M)")
                    print(f"   ⚡ Intervalo: {check_interval} segundos")
                    if resultado.final_score < 50:
                        print(f"   📉 Score bajo: Clasificado como RUIDO")
                    elif resultado.final_score >= 60:
                        print(f"   ⏱️ OBSERVACIÓN EXTENDIDA: hasta 20 minutos (mínimo: 2 min)")
                    else:
                        print(f"   ⏱️ Monitoreo estándar: 2-5 minutos")
                else:
                    # FIBO
                    print(f"   📈 Tipo: {resultado.origin}")
                    print(f"   ⚡ Intervalo: {check_interval} segundos")
                    if resultado.final_score >= 60:
                        # Observación extendida unificada de 20 minutos
                        if resultado.origin == "FIBO_1H":
                            print(f"   ⏱️ OBSERVACIÓN EXTENDIDA: hasta 20 minutos (mínimo: 5 min)")
                        elif resultado.origin == "FIBO_4H":
                            print(f"   ⏱️ OBSERVACIÓN EXTENDIDA: hasta 20 minutos (mínimo: 7 min)")
                        elif resultado.origin == "FIBO_1D":
                            print(f"   ⏱️ OBSERVACIÓN EXTENDIDA: hasta 20 minutos (mínimo: 10 min)")
                        else:
                            print(f"   ⏱️ OBSERVACIÓN EXTENDIDA: hasta 20 minutos (mínimo: 7 min)")
                    else:
                        # Score < 60: Observación estándar
                        if resultado.origin == "FIBO_1H":
                            print(f"   ⏱️ Monitoreo: 2.5-5 minutos")
                        elif resultado.origin == "FIBO_4H":
                            print(f"   ⏱️ Monitoreo: 4-7 minutos")
                        elif resultado.origin == "FIBO_1D":
                            print(f"   ⏱️ Monitoreo: 5-10 minutos")
                        else:
                            print(f"   ⏱️ Monitoreo: 4-7 minutos")
                
                if resultado.final_score >= 60:
                    print(f"   ⭐ Score >= 60: Observación extendida activa")
                
                print(f"   🎯 Umbral ALTA PRIORIDAD: 75")
                print(f"   💰 Entrada 1: ${entry_1:.8f}")
                if entry_2 > 0 and entry_2 != entry_1:
                    print(f"   💰 Entrada 2: ${entry_2:.8f}")
                print(f"   💰 Precio referencia: ${entry_price:.8f}")
                print(f"   🛡️ Protección contra descarte prematuro activa")
                
                # FILTRO: Solo enviar a j77 si score >= 60 (potencial FUERTE o ALTA)
                if resultado.final_score >= 60:
                    print(f"   ✅ Score >= 60: Enviando a j77")
                    
                    # Formatear resumen inicial (EN ANÁLISIS)
                    resumen = formatear_resumen_telegram(
                        resultado, 
                        grupo_nombre,
                        status=EventStatus.EN_ANALISIS
                    )
                    
                    # Enviar al canal destino
                    print(f"📤 Enviando estado inicial a {nombre_destino}...")
                    message_id = await enviar_a_canal(resumen)
                    
                    # Guardar el ID del mensaje para poder editarlo después
                    if message_id:
                        mensajes_tracking[event_id] = message_id
                else:
                    print(f"   🔇 Score < 60: NO se envía a j77 (filtrado)")
                    print(f"   ℹ️ Solo se envían señales con score >= 60")
                
                print(f"{'='*70}\n")
            else:
                print(f"   ❌ No es un evento válido (falta formato FIBO)")
        
        except Exception as e:
            print(f"❌ Error procesando mensaje: {e}")
            import traceback
            traceback.print_exc()
    
    # Mantener corriendo con reconexión automática
    print("💡 Bot en ejecución continua (reconexión automática activa)\n")
    
    try:
        await client.run_until_disconnected()
    except Exception as e:
        print(f"⚠️ Desconexión detectada: {e}")
        print("🔄 Intentando reconectar...")
        # El loop externo manejará la reconexión


if __name__ == "__main__":
    while True:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("\n\n👋 Monitor detenido por el usuario")
            break
        except Exception as e:
            print(f"\n❌ Error crítico: {e}")
            import traceback
            traceback.print_exc()
            print("\n🔄 Reiniciando en 10 segundos...")
            import time
            time.sleep(10)
