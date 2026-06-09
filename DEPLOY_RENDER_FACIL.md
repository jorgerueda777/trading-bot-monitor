# Despliegue en Render.com - 100% Visual (Sin Comandos)

**Tiempo total**: 10 minutos  
**Dificultad**: ⭐ (copiar y pegar)  
**Costo**: $0 - Gratis para siempre

---

## 📋 ANTES DE EMPEZAR - Prepara esto:

Abre tu archivo `.env` y ten listos estos valores:

```
TELEGRAM_API_ID=________
TELEGRAM_API_HASH=________
TELEGRAM_PHONE=________
SOURCE_GROUP_IDS=________
DEST_CHANNEL_ID=________
BINANCE_API_KEY=________ (opcional)
BINANCE_API_SECRET=________ (opcional)
```

---

## PASO 1: Subir código a GitHub (5 minutos)

### 1.1 Crear repositorio en GitHub

1. Ve a: https://github.com/new
2. Llena los datos:
   - **Repository name**: `trading-bot-monitor`
   - **Description**: "Bot de análisis de señales de trading"
   - **Visibilidad**: 🔒 **PRIVADO** (importante para proteger tus claves)
3. **NO** marques ninguna casilla (README, .gitignore, license)
4. Clic "Create repository"

### 1.2 Subir tu código

Abre PowerShell en tu carpeta del proyecto y ejecuta:

```powershell
# Ir a tu carpeta
cd "D:\FUTUROS 2026"

# Inicializar git (solo si no lo has hecho)
git init

# Agregar todo (excepto lo que está en .gitignore)
git add .

# Hacer commit
git commit -m "Initial commit - Trading bot ready for deployment"

# Conectar con GitHub (reemplaza TU_USUARIO)
git remote add origin https://github.com/TU_USUARIO/trading-bot-monitor.git

# Subir
git branch -M main
git push -u origin main
```

**Si te pide login**:
- Usuario: Tu username de GitHub
- Password: Necesitas un "Personal Access Token"
  - Ve a: https://github.com/settings/tokens
  - Clic "Generate new token (classic)"
  - Marca: `repo` (todos los permisos de repo)
  - Clic "Generate token"
  - Copia el token y úsalo como password

✅ **Verifica**: Ve a tu repo en GitHub y verifica que se subió todo

---

## PASO 2: Crear cuenta en Render (1 minuto)

1. Ve a: https://render.com/
2. Clic "Get Started"
3. **Registra con GitHub** (más fácil)
4. Autoriza a Render acceder a tus repos

✅ **Listo**: Ya tienes cuenta

---

## PASO 3: Crear el servicio (2 minutos)

### 3.1 Nuevo servicio

1. En el dashboard de Render, clic "New +"
2. Selecciona "Background Worker"
3. Conecta tu repositorio:
   - Si no ves el repo, clic "Configure account" → dar acceso
   - Selecciona `trading-bot-monitor`

### 3.2 Configurar servicio

Llena los campos:

| Campo | Valor |
|-------|-------|
| **Name** | `trading-bot-monitor` |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python monitor_grupos.py` |
| **Plan** | Free |

Clic "Create Background Worker"

⚠️ **NO HACER DEPLOY TODAVÍA** - Falta configurar variables

---

## PASO 4: Configurar Variables de Entorno (2 minutos)

1. En tu servicio, ve a la pestaña **"Environment"**
2. Clic "Add Environment Variable"
3. Agrega **TODAS** estas variables (una por una):

```
TELEGRAM_API_ID = tu_valor_aqui
TELEGRAM_API_HASH = tu_valor_aqui
TELEGRAM_PHONE = tu_valor_aqui
SOURCE_GROUP_IDS = tu_valor_aqui
DEST_CHANNEL_ID = tu_valor_aqui
BINANCE_API_KEY = tu_valor_aqui
BINANCE_API_SECRET = tu_valor_aqui
```

**IMPORTANTE**: 
- Copia los valores EXACTOS de tu archivo `.env`
- No pongas comillas
- No pongas espacios extra

Clic "Save Changes"

✅ **Verifica**: Deben aparecer 7 variables configuradas

---

## PASO 5: Subir archivo de sesión (CRÍTICO)

Tu archivo `session_name.session` debe estar en el servidor.

### Opción A: Subirlo al repositorio (MÁS FÁCIL)

```powershell
# En tu carpeta del proyecto
git add session_name.session
git commit -m "Add Telegram session"
git push
```

⚠️ **Asegúrate** que el repo sea PRIVADO

### Opción B: Regenerar sesión (MÁS SEGURO)

1. Deja que el bot inicie
2. Verá que no hay sesión
3. Te enviará un código a Telegram
4. Mira los logs en Render
5. El bot mostrará donde ingresar el código

**Para esta opción**: Deja `session_name.session` fuera del repo

---

## PASO 6: Deploy Manual (1 minuto)

1. Ve a tu servicio en Render
2. Clic en "Manual Deploy" → "Deploy latest commit"
3. Espera 2-3 minutos

---

## PASO 7: Verificar que está corriendo

1. Ve a la pestaña **"Logs"**
2. Deberías ver:

```
🤖 MONITOR DE GRUPOS - Motor de Clasificación
🔐 Conectando a Telegram...
✅ Conectado!
📋 Grupos a monitorear:
✅ Monitoreo iniciado
```

✅ **¡LISTO!** Tu bot está corriendo 24/7 gratis

---

## 🎯 VERIFICACIÓN FINAL

Envía un mensaje de prueba en uno de tus grupos monitoreados y:

1. Revisa los logs en Render
2. Revisa tu canal destino (j77)
3. Deberías ver el mensaje procesado

---

## 📊 Monitorear tu bot

### Ver logs en tiempo real:
1. Dashboard → Tu servicio → Logs
2. Los logs se actualizan automáticamente

### Reiniciar el bot:
1. Dashboard → Tu servicio → Manual Deploy → "Clear build cache & deploy"

### Ver uso de recursos:
1. Dashboard → Tu servicio → Metrics

---

## ⚠️ SOLUCIÓN DE PROBLEMAS

### Error: "Session file not found"
➡️ **Solución**: Sube `session_name.session` al repo (Opción A arriba)

### Error: "TELEGRAM_API_ID not found"
➡️ **Solución**: Verifica variables de entorno en la pestaña Environment

### Error: "Module not found"
➡️ **Solución**: Verifica que `requirements.txt` esté en el repo

### Bot se detiene después de 15 minutos
➡️ **Esto es NORMAL en Render Free**: Se suspende después de inactividad
➡️ **PERO** tu bot es activo (escucha mensajes) así que NO se suspenderá

---

## 🎉 ¡ÉXITO!

Tu bot está corriendo en la nube 24/7 gratis en Render.com

**Características**:
- ✅ Gratis permanente
- ✅ 512MB RAM
- ✅ Auto-restart si falla
- ✅ Logs en tiempo real
- ✅ Deploy automático al hacer push a GitHub

**Duración**: Ilimitada (mientras Render mantenga su tier gratuito)

---

## 📱 Siguiente nivel (Opcional)

Si quieres mejorar:

1. **Monitoreo**: Agrega alertas si el bot se cae
2. **Backup**: Respalda datos periódicamente
3. **Logs**: Guarda logs en archivos
4. **Métricas**: Agrega dashboard de métricas

Pero para empezar, ¡ya estás listo!
