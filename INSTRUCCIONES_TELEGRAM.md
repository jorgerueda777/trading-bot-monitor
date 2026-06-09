# 📱 INSTRUCCIONES: Conectar con Telegram

## 🎯 Tu Situación Actual

✅ **Sistema instalado y funcionando**  
✅ **Dependencias de Telegram instaladas**  
❌ **Falta configurar el bot de Telegram**

---

## 🚀 Pasos para Configurar (5 minutos)

### 📝 PASO 1: Crear el Bot en Telegram

1. **Abre Telegram** en tu teléfono o computadora

2. **Busca a BotFather:**
   - En la barra de búsqueda escribe: `@BotFather`
   - Abre el chat oficial de BotFather

3. **Crea tu bot:**
   ```
   Envía: /newbot
   ```

4. **Responde a las preguntas:**
   
   **Pregunta 1:** "Alright, a new bot. How are we going to call it?"
   ```
   Responde: Clasificador de Eventos
   ```
   (O el nombre que prefieras)

   **Pregunta 2:** "Now, let's choose a username for your bot."
   ```
   Responde: clasificador_eventos_bot
   ```
   (Debe terminar en 'bot' y ser único)

5. **Copia tu token:**
   
   BotFather te responderá con algo como:
   ```
   Done! Your token is:
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-123456
   ```
   
   **¡IMPORTANTE! Copia este token completo.**

---

### 🔧 PASO 2: Configurar el Token

1. **Abre el archivo `.env`** en tu editor de código

2. **Busca esta línea:**
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   ```

3. **Reemplázala con tu token:**
   ```
   TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-123456
   ```

4. **Guarda el archivo**

---

### 🔍 PASO 3: Obtener el ID del Grupo

**Opción A: Si ya tienes el grupo de Telegram donde llegan los eventos**

1. **Inicia el bot:**
   ```bash
   python telegram_integration.py
   ```

2. **Añade el bot a tu grupo:**
   - Abre el grupo en Telegram
   - Click en el nombre del grupo → "Añadir miembros"
   - Busca tu bot: `@clasificador_eventos_bot`
   - Añádelo al grupo

3. **Obtén el ID:**
   - En el grupo, envía:
   ```
   /getid
   ```
   
   - El bot responderá con algo como:
   ```
   📋 INFORMACIÓN DEL CHAT
   
   Chat ID: -1001234567890
   Tipo: supergroup
   Título: Mi Grupo de Señales
   ```

4. **Copia el Chat ID** (-1001234567890)

5. **Añádelo al archivo `.env`:**
   ```
   TELEGRAM_GROUP_ID=-1001234567890
   ```

**Opción B: Si quieres crear un grupo nuevo**

1. Crea un nuevo grupo en Telegram
2. Añade tu bot al grupo
3. Sigue los pasos de la Opción A

---

### ✅ PASO 4: Verificar Configuración

```bash
python test_telegram_config.py
```

**Deberías ver:**
```
============================================================
📊 RESUMEN
============================================================
   ✅ Token configurado
   ✅ Group ID configurado
   ✅ Dependencias instaladas
   ✅ Archivo .env existe

🎉 ¡TODO LISTO! Puedes iniciar el bot:
   python telegram_integration.py
```

---

### 🚀 PASO 5: Iniciar el Bot

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

🚀 Bot iniciado. Esperando mensajes...
============================================================
```

---

## 🧪 Probar el Sistema

### Prueba 1: Comando /start

En tu grupo de Telegram, envía:
```
/start
```

El bot debe responder con información de comandos.

### Prueba 2: Comando /getid

```
/getid
```

El bot debe responder con el ID del grupo.

### Prueba 3: Enviar un Evento de Prueba

Envía este mensaje al grupo:
```
#BTCUSDT
SESGO ALCISTA
ORIGEN: FIBO 4H
ZONA A: 45000
ZONA B: 44800
OBJETIVO A: 47000
OBJETIVO B: 48500
```

**El bot automáticamente debe:**
1. Detectar el evento
2. Clasificarlo
3. Responder con el resumen completo

---

## 📊 Comandos Disponibles

| Comando | Descripción |
|---------|-------------|
| `/start` | Información del bot |
| `/getid` | Obtener ID del chat |
| `/clasificar` | Clasificar evento (responder a un mensaje) |
| `/stats` | Ver estadísticas |

---

## 🎯 Flujo Automático

Una vez configurado, el bot funciona así:

```
1. Alguien envía un evento al grupo
   ↓
2. Bot detecta automáticamente el formato
   ↓
3. Bot obtiene datos del mercado (por ahora mock)
   ↓
4. Bot clasifica el evento
   ↓
5. Bot responde con el resumen en el grupo
```

**Ejemplo de mensaje del bot:**

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

[Métricas detalladas...]
```

---

## 🔧 Solución de Problemas Comunes

### ❌ "No se encontró TELEGRAM_BOT_TOKEN"

**Causa:** No configuraste el token en `.env`

**Solución:**
1. Verifica que copiaste el token de BotFather
2. Verifica que está en el archivo `.env` (no `.env.example`)
3. Reinicia el bot

### ❌ "Unauthorized"

**Causa:** Token incorrecto

**Solución:**
1. Ve a BotFather en Telegram
2. Envía `/token`
3. Selecciona tu bot
4. Copia el nuevo token
5. Actualiza `.env`

### ❌ El bot no responde en el grupo

**Causa 1:** El bot no está en el grupo

**Solución:** Añade el bot al grupo

**Causa 2:** El bot no tiene permisos

**Solución:** Dale permisos de administrador al bot

**Causa 3:** El bot no está corriendo

**Solución:** Ejecuta `python telegram_integration.py`

### ⚠️ El bot no detecta eventos automáticamente

**Causa:** Formato del evento incorrecto

**Solución:** Verifica que el evento tenga:
- `#SYMBOL` (con # y USDT al final)
- `SESGO ALCISTA` o `SESGO BAJISTA`
- `ORIGEN: FIBO 1H` (o 4H o 1D)

---

## 📁 Archivos Importantes

```
.env                          ← Token y Group ID aquí
telegram_integration.py       ← Script principal del bot
test_telegram_config.py       ← Verificador de configuración
TELEGRAM_SETUP.md            ← Guía completa (más detallada)
```

---

## 🎓 Próximos Pasos

Una vez que el bot funciona:

1. **Conectar con exchange real** (Binance/Bybit)
   - Ver `EXCHANGE_INTEGRATION.md` (próximamente)

2. **Personalizar alertas**
   - Modificar `telegram_integration.py`
   - Enviar solo eventos de ALTA PRIORIDAD

3. **Configurar notificaciones VIP**
   - Enviar alertas a canal privado
   - Diferentes destinos según prioridad

4. **Ejecutar 24/7**
   - Usar screen/tmux en Linux
   - Configurar como servicio systemd
   - Deploy en Docker

---

## 📞 ¿Necesitas Ayuda?

1. **Ejecuta el verificador:**
   ```bash
   python test_telegram_config.py
   ```

2. **Lee la guía completa:**
   ```
   TELEGRAM_SETUP.md
   ```

3. **Revisa los logs** cuando el bot esté corriendo
   - Te dirá exactamente qué está pasando

---

## ✅ Checklist Final

Marca cada paso cuando lo completes:

- [ ] Hablé con @BotFather en Telegram
- [ ] Creé un bot con /newbot
- [ ] Copié el token a `.env`
- [ ] Añadí el bot a mi grupo
- [ ] Obtuve el Chat ID con /getid
- [ ] Copié el Chat ID a `.env`
- [ ] Ejecuté `python test_telegram_config.py` ✅
- [ ] Todo aparece en verde ✅
- [ ] Inicié el bot con `python telegram_integration.py`
- [ ] Probé con /start en el grupo ✅
- [ ] Envié un evento de prueba ✅
- [ ] El bot respondió automáticamente ✅

---

## 🎉 ¡Listo!

Tu sistema ahora:
- ✅ Lee eventos del grupo de Telegram
- ✅ Los clasifica automáticamente
- ✅ Envía resúmenes al grupo

**¡Disfruta tu Motor de Clasificación integrado con Telegram!** 🚀

---

*¿Dudas? Todo está en `TELEGRAM_SETUP.md` con más detalles*
