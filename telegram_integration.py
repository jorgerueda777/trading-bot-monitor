"""
Integración con Telegram
Conecta el Motor de Clasificación con grupos de Telegram
"""
import os
import re
from datetime import datetime
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from dotenv import load_dotenv

from src.core.classifier import EventClassifier
from src.storage.historical_storage import HistoricalStorage
from src.data_sources.binance_client import BinanceClient

# Cargar variables de entorno
load_dotenv()

# Inicializar clasificador y Binance
classifier = EventClassifier()
storage = HistoricalStorage()
binance_client = BinanceClient()

# ID del grupo (se obtendrá automáticamente)
TARGET_GROUP_ID = None


def detectar_evento_en_mensaje(text: str) -> bool:
    """Detecta si un mensaje contiene un evento válido"""
    if not text:
        return False
    
    tiene_simbolo = bool(re.search(r'#[A-Z]+USDT', text, re.IGNORECASE))
    
    # FORMATO 1: Formato FIBO original
    tiene_sesgo = bool(re.search(r'SESGO\s+(ALCISTA|BAJISTA)', text, re.IGNORECASE))
    tiene_origen = bool(re.search(r'ORIGEN:\s*FIBO\s+(1H|4H|1D)', text, re.IGNORECASE))
    formato_fibo = tiene_simbolo and tiene_sesgo and tiene_origen
    
    # FORMATO 2: Formato SHORT/LONG con entradas y TPs
    tiene_direccion = bool(re.search(r'(SHORT|LONG|🔴|🟢)', text, re.IGNORECASE))
    tiene_entrada = bool(re.search(r'(ENTRADA|ENTRY|ZONA)', text, re.IGNORECASE))
    formato_trading = tiene_simbolo and tiene_direccion and tiene_entrada
    
    return formato_fibo or formato_trading


def obtener_market_data(symbol: str):
    """
    Obtiene datos de mercado REALES de Binance
    """
    return binance_client.get_market_data(symbol)


def formatear_resumen_telegram(classification) -> str:
    """Formatea la clasificación para Telegram (versión compacta)"""
    
    # Emojis según prioridad
    if classification.priority == "ALTA PRIORIDAD":
        emoji = "🔥🔥🔥"
        color = "🟢"
    elif classification.priority == "PRIORIDAD MEDIA":
        emoji = "⚠️"
        color = "🟡"
    else:
        emoji = "ℹ️"
        color = "🔴"
    
    mensaje = f"""
{emoji} **CLASIFICACIÓN DE EVENTO** {emoji}

📊 **Símbolo:** {classification.symbol}
📈 **Sesgo:** {classification.bias}
⏱️ **Origen:** {classification.origin}
✅ **Estado:** {classification.status}

━━━━━━━━━━━━━━━━━━━━━━
**PUNTUACIÓN FINAL**
{color} **{classification.final_score:.1f}/100** → **{classification.priority}**
━━━━━━━━━━━━━━━━━━━━━━

**🔍 MÉTRICAS PRINCIPALES:**

📊 **Open Interest:** {classification.open_interest.score:.0f}/100 (peso {classification.open_interest.weight}%)
  └ {classification.open_interest.analysis}

💰 **Funding Rate:** {classification.funding.score:.0f}/100 (peso {classification.funding.weight}%)
  └ {classification.funding.analysis}

📉 **CVD:** {classification.cvd.score:.0f}/100 (peso {classification.cvd.weight}%)
  └ {classification.cvd.analysis}

⚖️ **Delta:** {classification.delta.score:.0f}/100 (peso {classification.delta.weight}%)
  └ {classification.delta.analysis}

📈 **Volumen:** {classification.volume.score:.0f}/100 (peso {classification.volume.weight}%)
  └ {classification.volume.analysis}

💧 **Liquidity Sweeps:** {classification.liquidity_sweeps.score:.0f}/100 (peso {classification.liquidity_sweeps.weight}%)
  └ {classification.liquidity_sweeps.analysis}

📍 **VWAP:** {classification.vwap.score:.0f}/100 (peso {classification.vwap.weight}%)
  └ {classification.vwap.analysis}

━━━━━━━━━━━━━━━━━━━━━━
**⭐ FACTORES CLAVE:**
"""
    
    for i, factor in enumerate(classification.key_factors, 1):
        mensaje += f"\n{i}. {factor}"
    
    mensaje += f"\n\n⏰ Evaluado: {classification.evaluated_at.strftime('%H:%M:%S')}"
    mensaje += f"\n\n_Motor de Clasificación v1.0_"
    
    return mensaje


# ============================================================================
# COMANDOS DEL BOT
# ============================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start"""
    await update.message.reply_text(
        "🤖 **Motor de Clasificación de Eventos**\n\n"
        "Comandos disponibles:\n"
        "/start - Muestra este mensaje\n"
        "/getid - Obtiene el ID de este chat\n"
        "/listchats - Lista todos los chats donde estoy\n"
        "/clasificar - Clasifica el último evento detectado\n"
        "/stats - Muestra estadísticas\n\n"
        "Envía eventos en formato:\n"
        "#SYMBOL\n"
        "SESGO ALCISTA/BAJISTA\n"
        "ORIGEN: FIBO 1H/4H/1D\n"
        "ZONA A: precio\n"
        "ZONA B: precio\n"
        "OBJETIVO A: precio\n"
        "OBJETIVO B: precio",
        parse_mode='Markdown'
    )


async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /getid - Obtiene el ID del chat/grupo"""
    chat = update.effective_chat
    user = update.effective_user
    
    mensaje = f"""
📋 **INFORMACIÓN DEL CHAT**

**Chat ID:** `{chat.id}`
**Tipo:** {chat.type}
**Título:** {chat.title if chat.title else 'Chat privado'}

**User ID:** `{user.id}`
**Usuario:** @{user.username if user.username else 'Sin username'}
**Nombre:** {user.first_name} {user.last_name if user.last_name else ''}

💡 **Tip:** Guarda el Chat ID en tu archivo .env como:
```
TELEGRAM_GROUP_ID={chat.id}
```
"""
    
    await update.message.reply_text(mensaje, parse_mode='Markdown')
    
    # Log en consola
    print(f"\n{'='*60}")
    print(f"📋 ID DEL CHAT DETECTADO:")
    print(f"   Chat ID: {chat.id}")
    print(f"   Tipo: {chat.type}")
    print(f"   Título: {chat.title if chat.title else 'N/A'}")
    print(f"{'='*60}\n")


async def clasificar_comando(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /clasificar - Clasifica un evento manualmente"""
    
    # Verificar si hay un mensaje respondido
    if not update.message.reply_to_message:
        await update.message.reply_text(
            "❌ Debes responder a un mensaje con un evento usando /clasificar"
        )
        return
    
    evento_texto = update.message.reply_to_message.text
    
    # Verificar que sea un evento
    if not detectar_evento_en_mensaje(evento_texto):
        await update.message.reply_text(
            "❌ El mensaje no parece contener un evento válido"
        )
        return
    
    await clasificar_evento(update, evento_texto)


async def clasificar_evento(update: Update, evento_texto: str):
    """Clasifica un evento y envía el resumen"""
    
    try:
        # Extraer símbolo
        match = re.search(r'#([A-Z0-9]+)', evento_texto)
        symbol = match.group(1) if match else "UNKNOWN"
        
        # Obtener datos de mercado REALES
        market_data = obtener_market_data(symbol)
        
        # Clasificar
        resultado = classifier.classify_event(
            evento_texto,
            market_data,
            datetime.now()
        )
        
        # Guardar en histórico
        storage.save_classification(resultado.model_dump())
        
        # Formatear y enviar resumen
        resumen = formatear_resumen_telegram(resultado)
        
        await update.message.reply_text(
            resumen,
            parse_mode='Markdown'
        )
        
        # Log
        print(f"\n✅ Evento clasificado: {symbol} - {resultado.final_score:.1f}/100")
        
    except Exception as e:
        await update.message.reply_text(
            f"❌ Error al clasificar evento: {str(e)}"
        )
        print(f"❌ Error: {e}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja todos los mensajes del grupo"""
    
    # Solo procesar mensajes de texto
    if not update.message or not update.message.text:
        return
    
    texto = update.message.text
    
    # Detectar si es un evento
    if detectar_evento_en_mensaje(texto):
        print(f"\n🔍 Evento detectado en grupo: {update.effective_chat.title}")
        
        # Clasificar automáticamente
        await clasificar_evento(update, texto)


async def list_chats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /listchats - Lista todos los chats donde está el bot"""
    
    mensaje = """
📱 **CHATS DETECTADOS**

Este bot está presente en:

**Chat actual:**
"""
    
    chat = update.effective_chat
    mensaje += f"• ID: `{chat.id}`\n"
    mensaje += f"  Tipo: {chat.type}\n"
    if chat.title:
        mensaje += f"  Título: {chat.title}\n"
    else:
        mensaje += f"  Usuario: {update.effective_user.first_name}\n"
    
    mensaje += """

💡 **Para configurar este grupo:**
1. Copia el ID de arriba
2. Edita el archivo .env
3. Añade: TELEGRAM_GROUP_ID=ese_id
4. Reinicia el bot

ℹ️ **Nota:** El bot solo puede detectar chats donde:
- Está añadido actualmente
- Alguien envía un mensaje (para activarlo)

Si quieres que el bot lea otro grupo:
1. Añade el bot a ese grupo
2. En ese grupo, envía /getid
"""
    
    await update.message.reply_text(mensaje, parse_mode='Markdown')


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /stats - Muestra estadísticas"""
    
    try:
        # Cargar datos históricos
        records = storage.load_historical_data()
        total = len(records)
        
        if total == 0:
            await update.message.reply_text("📊 Aún no hay eventos clasificados")
            return
        
        # Calcular precisión
        accuracy = storage.calculate_accuracy_by_priority()
        
        # Contar por prioridad
        alta = sum(1 for r in records if r['classification'].get('priority') == 'ALTA PRIORIDAD')
        media = sum(1 for r in records if r['classification'].get('priority') == 'PRIORIDAD MEDIA')
        baja = sum(1 for r in records if r['classification'].get('priority') == 'BAJA PRIORIDAD')
        
        mensaje = f"""
📊 **ESTADÍSTICAS DEL SISTEMA**

**Total eventos clasificados:** {total}

**Por prioridad:**
🔥 Alta: {alta} eventos ({alta/total*100:.1f}%)
⚠️ Media: {media} eventos ({media/total*100:.1f}%)
ℹ️ Baja: {baja} eventos ({baja/total*100:.1f}%)

**Precisión (con outcomes):**
"""
        
        for priority, acc in accuracy.items():
            emoji = "✅" if acc >= 0.7 else "⚠️" if acc >= 0.5 else "❌"
            mensaje += f"{emoji} {priority}: {acc*100:.1f}%\n"
        
        await update.message.reply_text(mensaje, parse_mode='Markdown')
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error al obtener estadísticas: {str(e)}")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Inicia el bot de Telegram"""
    
    # Obtener token del bot
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not TOKEN:
        print("\n❌ ERROR: No se encontró TELEGRAM_BOT_TOKEN en el archivo .env")
        print("\n📋 Pasos para configurar:")
        print("1. Habla con @BotFather en Telegram")
        print("2. Crea un nuevo bot con /newbot")
        print("3. Copia el token que te da")
        print("4. Añádelo al archivo .env como:")
        print("   TELEGRAM_BOT_TOKEN=tu_token_aqui")
        print("\n")
        return
    
    print("\n" + "="*60)
    print("🤖 INICIANDO BOT DE TELEGRAM")
    print("="*60)
    print(f"✅ Token configurado")
    print(f"✅ Clasificador inicializado")
    print(f"✅ Storage inicializado")
    print("\n📋 Para obtener el ID del grupo:")
    print("   1. Añade el bot a tu grupo")
    print("   2. Envía el comando /getid en el grupo")
    print("   3. Guarda el ID en .env como TELEGRAM_GROUP_ID")
    print("\n🚀 Bot iniciado. Esperando mensajes...")
    print("="*60 + "\n")
    
    # Crear aplicación
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Registrar handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("getid", get_chat_id))
    app.add_handler(CommandHandler("listchats", list_chats))
    app.add_handler(CommandHandler("clasificar", clasificar_comando))
    app.add_handler(CommandHandler("stats", stats))
    
    # Handler para todos los mensajes (auto-clasificación)
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_message
    ))
    
    # Iniciar bot
    app.run_polling()


if __name__ == "__main__":
    main()
