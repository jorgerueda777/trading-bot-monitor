# 🔴 PROBLEMA ACTUAL: Bot se congela después de ~10 minutos

## 📊 SÍNTOMAS

- ✅ Bot se conecta correctamente
- ✅ Procesa mensajes inicialmente (vimos FOLKSUSDT)
- ✅ Auto-ping funciona (🔄 Auto-ping OK)
- ✅ Heartbeat activo (💓 Heartbeat: Conexión activa)
- ❌ **Después de ~10 minutos deja de recibir mensajes nuevos**
- ❌ Hay mensajes en los grupos pero no los procesa
- ❌ NO muestra errores en los logs

## 🔍 ANÁLISIS

### Qué SÍ funciona:
1. Servidor HTTP activo (puerto 10000)
2. Auto-ping cada 30 segundos
3. Heartbeat Telegram cada 60 segundos
4. Render NO suspende el servicio (se mantiene activo)

### Qué NO funciona:
1. **Event listener de Telegram** se congela silenciosamente
2. No recibe nuevos mensajes después de ~10 minutos
3. El bot sigue "vivo" pero el handler de mensajes no se ejecuta

## 🎯 CAUSA PROBABLE

El problema es que `client.run_until_disconnected()` puede bloquearse o el event handler `@client.on(events.NewMessage)` deja de dispararse.

Posibles causas técnicas:
1. **Event loop bloqueado** - Alguna operación async bloquea el loop
2. **Telethon se desconecta** silenciosamente sin lanzar excepción
3. **Handler se des-registra** por alguna razón
4. **Conflicto entre tasks** - Auto-ping, heartbeat y bot compitiendo

## 💡 SOLUCIONES A PROBAR

### Opción 1: Forzar re-registro del handler periódicamente
- Cada X minutos, verificar que el handler esté registrado

### Opción 2: Detectar "freeze" y reiniciar
- Si no recibe mensajes en N minutos → Reiniciar bot

### Opción 3: Usar polling en lugar de event listener
- En lugar de esperar eventos, hacer polling activo

### Opción 4: Separar completamente bot y servidor HTTP
- Dos procesos independientes en lugar de async tasks

## 📝 CONFIGURACIÓN ACTUAL

**Render:** Web Service (gratuito)
**Puerto:** 10000
**Start Command:** `python start.py`
**Dockerfile CMD:** `python start.py`

## 🔧 ÚLTIMA VERSIÓN DEL CÓDIGO

- `start.py`: Servidor HTTP + Auto-ping cada 30s
- `monitor_grupos.py`: Bot Telegram + Heartbeat cada 60s + Event handler
- Cliente Telegram: Con `auto_reconnect=True`, `connection_retries=5`

## ❓ PREGUNTA CLAVE

¿Los bots que tenías antes funcionando usaban exactamente este mismo setup?
- Web Service en Render
- Telethon con event handlers
- Session string en variable de entorno

Si sí, necesitamos revisar qué tiene diferente tu código anterior que funcionaba.
