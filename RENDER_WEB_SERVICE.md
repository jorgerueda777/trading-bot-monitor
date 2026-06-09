# 🚀 Desplegar en Render - Web Service GRATIS

**Tu código está en**: https://github.com/jorgerueda777/trading-bot-monitor

**NUEVO**: Ahora incluye keep-alive para Web Service gratis

---

## ✅ LO QUE AGREGUÉ:

1. **`keep_alive.py`** - Servidor web que mantiene el servicio activo
2. **`start.py`** - Script que ejecuta bot + servidor juntos
3. **Actualizado `requirements.txt`** - Incluye `aiohttp`

---

## 📤 PASO 1: Subir cambios a GitHub

Ejecuta esto en PowerShell:

```powershell
cd "D:\FUTUROS 2026"
git add .
git commit -m "Add keep-alive server for Render Web Service"
git push
```

---

## 🌐 PASO 2: Crear Web Service en Render

1. Ve a: https://render.com
2. Login (o registra con GitHub)
3. Clic **"New +"** → **"Web Service"**
4. Conecta tu repositorio: `trading-bot-monitor`

### Configuración:

| Campo | Valor |
|-------|-------|
| **Name** | `trading-bot-monitor` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python start.py` |
| **Plan** | **Free** |

Clic **"Create Web Service"**

⚠️ **NO HAGAS DEPLOY TODAVÍA** - Falta configurar variables

---

## 🔑 PASO 3: Variables de Entorno

Pestaña **"Environment"** → Agregar estas variables:

```
TELEGRAM_API_ID = [tu_valor]
TELEGRAM_API_HASH = [tu_valor]  
TELEGRAM_PHONE = [tu_valor]
SOURCE_GROUP_IDS = [tu_valor]
DEST_CHANNEL_ID = [tu_valor]
BINANCE_API_KEY = [tu_valor] (opcional)
BINANCE_API_SECRET = [tu_valor] (opcional)
```

Clic **"Save Changes"**

---

## 🚀 PASO 4: Deploy

1. Clic **"Manual Deploy"** → **"Deploy latest commit"**
2. Espera 3-4 minutos
3. Ve a **"Logs"**

Busca:
```
🌐 Keep-alive server iniciado en puerto 10000
✅ Conectado!
✅ Monitoreo iniciado
```

---

## ✅ PASO 5: Verificar

Render te dará una URL tipo: `https://trading-bot-monitor.onrender.com`

1. Abre esa URL en tu navegador
2. Deberías ver: "🤖 Trading Bot Monitor - Status: running"
3. La página se auto-refresca cada 4 minutos

**Esto mantiene el servicio activo 24/7 GRATIS** ✅

---

## 🎯 Cómo Funciona el Keep-Alive

1. **Servidor web** corriendo en puerto 10000
2. **Auto-refresh** cada 4 minutos (evita suspensión a los 15 min)
3. **Bot de Telegram** corriendo en paralelo
4. **Totalmente gratis** con Render Web Service

---

## ⚠️ Limitaciones Render Free

- Se suspende si NO hay actividad por 15 minutos
- **Solución**: El keep-alive previene esto
- 750 horas/mes de uso
- Puede tardar ~1 min en arrancar después de suspensión

---

## 🔍 Monitorear el Bot

### Ver logs:
- Dashboard Render → Tu servicio → "Logs"

### Ver status:
- Abre: `https://tu-servicio.onrender.com`

### Health check:
- Abre: `https://tu-servicio.onrender.com/health`

---

## ✅ Resultado Final

🎉 **Bot corriendo 24/7 GRATIS** con:
- ✅ Monitoreo de grupos Telegram
- ✅ Clasificación automática
- ✅ Envío a canal j77
- ✅ Keep-alive automático
- ✅ $0 costo

**Tiempo total**: 15 minutos  
**Costo**: $0

¡Listo! 🚀
