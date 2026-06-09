# 📱 Guía de Configuración de Telegram

Esta guía te ayudará a conectar el Motor de Clasificación con Telegram en **menos de 5 minutos**.

---

## 🎯 Objetivo

- ✅ Leer eventos de un grupo de Telegram
- ✅ Clasificar automáticamente cada evento
- ✅ Enviar resumen de clasificación al grupo

---

## 📋 Pasos de Configuración

### Paso 1: Crear tu Bot de Telegram

1. **Abre Telegram** y busca: `@BotFather`

2. **Inicia una conversación** con BotFather

3. **Crea un nuevo bot** enviando:
   ```
   /newbot
   ```

4. **Sigue las instrucciones:**
   - Elige un nombre para tu bot (ej: "Clasificador de Eventos")
   - Elige un username (debe terminar en 'bot', ej: "clasificador_eventos_bot")

5. **Copia el token** que BotFather te proporciona. Se verá así:
   ```
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

6. **Guarda el token** en el archivo `.env`:
   ```bash
   # Copia .env.example a .env
   cp .env.example .env
   
   # Edita .env y añade tu token
   TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

---

### Paso 2: Obtener el ID del Grupo

#### Opción A: Usando el Bot (Recomendado)

1. **Añade tu bot al grupo** de Telegram donde llegan los eventos:
   - Ve al grupo
   - Click en el nombre del grupo → "Añadir miembros"
   - Busca tu bot por el username
   - Añádelo

2. **Dale permisos de administrador** (opcional pero recomendado):
   - Click en el nombre del grupo → "Editar"
   - Click en "Administradores" → Añade tu bot

3. **Obtén el ID del grupo:**
   - En el grupo, envía el comando:
   ```
   /getid
   ```
   
   - El bot responderá con algo como:
   ```
   📋 INFORMACIÓN DEL CHAT
   
   Chat ID: -1001234567890
   Tipo: supergroup
   Título: Mi Grupo de Trading
   ```

4. **Guarda el Chat ID** en `.env`:
   ```
   TELEGRAM_GROUP_ID=-1001234567890
   ```

#### Opción B: Manual (usando otro bot)

1. Añade `@RawDataBot` a tu grupo
2. El bot te mostrará el ID del grupo automáticamente
3. Guarda el ID en `.env`
4. Remueve `@RawDataBot` del grupo

---

### Paso 3: Instalar Dependencias

```bash
# Instalar python-telegram-bot
pip install -r requirements.txt

# O solo la librería de Telegram
pip install python-telegram-bot
```

---

### Paso 4: Iniciar el Bot

```bash
python telegram_integration.py
```

**Deberías ver:**
```
============================================================
🤖 INICIANDO BOT DE TELEGRAM
============================================================
✅ Token configurado
✅ Clasificador inicializado
✅ Storage inicializado

📋 Para obtener el ID del grupo:
   1. Añade el bot a tu grupo
   2. Envía el comando /getid en el grupo
   3. Guarda el ID en .env como TELEGRAM_GROUP_ID

🚀 Bot iniciado. Esperando mensajes...
============================================================
```

---

## 🎮 Comandos Disponibles

Una vez que el bot está corriendo, puedes usar estos comandos en Telegram:

### `/start`
Muestra información del bot y comandos disponibles.

### `/getid`
Obtiene el ID del chat actual (grupo o privado).
```
/getid
```

### `/clasificar`
Clasifica un evento manualmente. Debes responder a un mensaje que contenga un evento.
```
[Responde a un mensaje con evento]
/clasificar
```

### `/stats`
Muestra estadísticas del sistema (eventos clasificados, precisión, etc.)
```
/stats
```

---

## 🔄 Funcionamiento Automático

El bot clasifica **automáticamente** cualquier mensaje que detecte como un evento válido.

**Formato de evento que detecta:**
```
#BTCUSDT
SESGO ALCISTA
ORIGEN: FIBO 4H
ZONA A: 45000
ZONA B: 44800
OBJETIVO A: 47000
OBJETIVO B: 48500
```

Cuando llega un mensaje con este formato, el bot:
1. ✅ Lo detecta automáticamente
2. ✅ Obtiene datos del mercado
3. ✅ Clasifica el evento
4. ✅ Envía el resumen al grupo

**Ejemplo de respuesta del bot:**
```
🔥🔥🔥 CLASIFICACIÓN DE EVENTO 🔥🔥🔥

📊 Símbolo: BTCUSDT
📈 Sesgo: BULLISH
⏱️ Origen: FIBO_4H
✅ Estado: VIGENTE

━━━━━━━━━━━━━━━━━━━━━━
PUNTUACIÓN FINAL
🟢 94.4/100 → ALTA PRIORIDAD
━━━━━━━━━━━━━━━━━━━━━━

🔍 MÉTRICAS PRINCIPALES:

📊 Open Interest: 95/100 (peso 25%)
  └ OI increasing, variación: +25.00%

💰 Funding Rate: 100/100 (peso 5%)
  └ FR 0.0120% (extremo)

... más métricas ...

⭐ FACTORES CLAVE:
1. Open Interest: OI increasing (peso: 23.9)
2. CVD: divergencia detectada (peso: 18.0)
3. Delta: dominancia compradora (peso: 15.0)
```

---

## 🛠️ Solución de Problemas

### Error: "No se encontró TELEGRAM_BOT_TOKEN"

**Solución:**
1. Verifica que creaste el archivo `.env` (no `.env.example`)
2. Verifica que el token esté correctamente copiado
3. Reinicia el bot

### Error: "Unauthorized"

**Solución:**
- El token es incorrecto
- Genera un nuevo token con BotFather usando `/token`

### El bot no responde en el grupo

**Solución:**
1. Verifica que el bot esté añadido al grupo
2. Si es un grupo privado, dale permisos de administrador
3. Verifica que el bot esté corriendo (`python telegram_integration.py`)

### El bot no detecta eventos automáticamente

**Solución:**
- Verifica que el evento tenga el formato correcto:
  - Debe empezar con `#SYMBOL`
  - Debe tener `SESGO ALCISTA` o `SESGO BAJISTA`
  - Debe tener `ORIGEN: FIBO 1H/4H/1D`

---

## 🔐 Seguridad y Privacidad

### ⚠️ Importante:

1. **Nunca compartas tu TELEGRAM_BOT_TOKEN**
   - Es como una contraseña
   - Cualquiera con el token puede controlar tu bot

2. **Archivo .env NO debe subirse a Git**
   - Ya está en `.gitignore`
   - Contiene información sensible

3. **Permisos del bot**
   - El bot solo puede leer mensajes de grupos donde está añadido
   - No puede leer mensajes privados de usuarios (a menos que le escriban)

---

## 📊 Configuración Avanzada

### Enviar solo alertas de Alta Prioridad

Modifica `telegram_integration.py`:

```python
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if detectar_evento_en_mensaje(texto):
        resultado = classifier.classify_event(...)
        
        # Solo enviar si es alta prioridad
        if resultado.priority == "ALTA PRIORIDAD":
            await clasificar_evento(update, texto)
```

### Enviar a canal privado en vez del grupo

```python
CANAL_ALERTAS_ID = -1001234567890  # Tu canal privado

async def clasificar_evento(update: Update, evento_texto: str):
    # ... clasificar ...
    
    # Enviar al canal en vez de responder
    await context.bot.send_message(
        chat_id=CANAL_ALERTAS_ID,
        text=resumen,
        parse_mode='Markdown'
    )
```

### Notificaciones personalizadas por prioridad

```python
# Diferentes destinos según prioridad
if resultado.priority == "ALTA PRIORIDAD":
    # Enviar al canal VIP
    await context.bot.send_message(CANAL_VIP, resumen)
elif resultado.priority == "PRIORIDAD MEDIA":
    # Solo al grupo principal
    await update.message.reply_text(resumen)
# Baja prioridad: no enviar nada
```

---

## 🚀 Ejecución en Producción

### Opción 1: Servidor Linux con screen

```bash
# Instalar screen
sudo apt-get install screen

# Crear sesión
screen -S telegram_bot

# Iniciar bot
python telegram_integration.py

# Desconectar (Ctrl+A, luego D)
# Reconectar: screen -r telegram_bot
```

### Opción 2: Systemd Service

Crear `/etc/systemd/system/telegram-classifier.service`:

```ini
[Unit]
Description=Telegram Event Classifier Bot
After=network.target

[Service]
Type=simple
User=tu_usuario
WorkingDirectory=/ruta/a/tu/proyecto
ExecStart=/usr/bin/python3 telegram_integration.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Iniciar:
```bash
sudo systemctl enable telegram-classifier
sudo systemctl start telegram-classifier
sudo systemctl status telegram-classifier
```

### Opción 3: Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "telegram_integration.py"]
```

```bash
docker build -t telegram-classifier .
docker run -d --name telegram-bot --env-file .env telegram-classifier
```

---

## 📝 Checklist de Configuración

- [ ] Crear bot con @BotFather
- [ ] Copiar token a `.env`
- [ ] Añadir bot al grupo
- [ ] Ejecutar `/getid` en el grupo
- [ ] Copiar Chat ID a `.env`
- [ ] Instalar dependencias: `pip install -r requirements.txt`
- [ ] Iniciar bot: `python telegram_integration.py`
- [ ] Probar con `/start`
- [ ] Enviar un evento de prueba al grupo
- [ ] Verificar que el bot responde automáticamente

---

## 🎉 ¡Listo!

Tu bot ahora está:
- ✅ Leyendo eventos del grupo
- ✅ Clasificándolos automáticamente
- ✅ Enviando resúmenes al grupo

**Próximos pasos:**
1. Conectar con API real de exchange (ver `EXCHANGE_INTEGRATION.md`)
2. Ajustar perfiles de evaluación según tus necesidades
3. Configurar alertas personalizadas
4. Analizar históricos para recalibración

---

## 🆘 Soporte

¿Problemas? Verifica:
1. El token está correctamente configurado en `.env`
2. El bot está añadido al grupo
3. El bot tiene permisos para leer mensajes
4. El script `telegram_integration.py` está corriendo

---

*Última actualización: 2026-06-07*
