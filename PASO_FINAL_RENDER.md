# 🚀 PASO FINAL: Desplegar en Render.com

**Tu código YA ESTÁ en GitHub**: https://github.com/jorgerueda777/trading-bot-monitor

Ahora solo falta desplegarlo en Render (10 minutos).

---

## PASO 1: Crear cuenta en Render (2 minutos)

1. Ve a: https://render.com
2. Clic "Get Started"
3. **Sign up with GitHub** (más fácil)
4. Autoriza a Render

---

## PASO 2: Crear servicio (3 minutos)

1. En Render dashboard, clic **"New +"**
2. Selecciona **"Background Worker"**
3. Conecta tu repositorio:
   - Si no lo ves, clic "Configure account" → dar acceso
   - Busca y selecciona: `trading-bot-monitor`

4. **Configuración del servicio**:

| Campo | Valor |
|-------|-------|
| Name | `trading-bot-monitor` |
| Environment | `Python 3` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `python monitor_grupos.py` |
| Plan | **Free** |

5. Clic **"Create Background Worker"**

⚠️ **TODAVÍA NO HAGAS DEPLOY** - Falta configurar variables

---

## PASO 3: Variables de Entorno (5 minutos)

1. En tu servicio en Render, ve a **"Environment"** (pestaña izquierda)
2. Clic **"Add Environment Variable"**
3. Agrega TODAS estas (una por una):

```
TELEGRAM_API_ID = [tu_valor_del_.env]
TELEGRAM_API_HASH = [tu_valor_del_.env]
TELEGRAM_PHONE = [tu_valor_del_.env]
SOURCE_GROUP_IDS = [tu_valor_del_.env]
DEST_CHANNEL_ID = [tu_valor_del_.env]
BINANCE_API_KEY = [tu_valor_del_.env] (opcional)
BINANCE_API_SECRET = [tu_valor_del_.env] (opcional)
```

**IMPORTANTE**: 
- Copia los valores EXACTOS de tu archivo `.env`
- NO pongas comillas
- NO pongas espacios extras

4. Clic **"Save Changes"**

---

## PASO 4: Deploy (1 minuto)

1. Clic **"Manual Deploy"** (botón arriba derecha)
2. Clic **"Deploy latest commit"**
3. Espera 2-3 minutos
4. Ve a pestaña **"Logs"**

---

## PASO 5: Verificar que funciona

En los **Logs** busca:

```
✅ Conectado!
📋 Grupos a monitorear:
✅ Monitoreo iniciado
```

Si ves eso, **¡TU BOT ESTÁ CORRIENDO 24/7 GRATIS!** 🎉

---

## 🔍 Prueba Final

1. Envía un mensaje de prueba en uno de tus grupos monitoreados
2. Revisa los logs en Render: debe aparecer "📩 Mensaje recibido"
3. Si la señal tiene score ≥60:
   - Revisa tu canal j77
   - Debe aparecer el mensaje formateado

---

## ⚠️ Solución de Problemas

### Error: "Session file not found"
- Tu archivo `session_name.session` está en el repo
- Si no funciona, el bot generará uno nuevo
- Telegram te enviará un código de verificación

### Error: "TELEGRAM_API_ID not found"
- Ve a Environment en Render
- Verifica que TODAS las variables estén configuradas
- Clic "Save Changes"
- Redeploy

### Bot no recibe mensajes
- Verifica SOURCE_GROUP_IDS en Environment
- Verifica que el bot tenga acceso a los grupos
- Revisa logs para errores

---

## 🎯 RESUMEN

1. ✅ Código en GitHub
2. → Crear cuenta Render
3. → Crear servicio Background Worker
4. → Configurar variables de entorno
5. → Deploy
6. → Verificar logs
7. ✅ Bot corriendo 24/7 gratis

---

## 📞 ¿Necesitas ayuda?

Lee: `DEPLOY_RENDER_FACIL.md` para más detalles

---

**Tiempo total**: 10 minutos  
**Costo**: $0 (100% gratis)  
**Resultado**: Bot corriendo 24/7 en la nube

¡Éxito! 🚀
