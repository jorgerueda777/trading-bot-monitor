# 🚀 Despliega Tu Bot AHORA - 4 Pasos Simples

**Plataforma**: Render.com  
**Costo**: $0 (Gratis permanente)  
**Tiempo**: 15 minutos

---

## ✨ LO QUE VOY A HACER POR TI

Ya preparé TODO el código para desplegar. Solo necesitas:

1. ✅ Subir a GitHub (5 min)
2. ✅ Crear servicio en Render (3 min)
3. ✅ Copiar tus variables (5 min)
4. ✅ Deploy (2 min)

**Total**: 15 minutos y listo

---

## 📋 ANTES DE EMPEZAR

Abre tu archivo `.env` y ten a mano:

```
TELEGRAM_API_ID=________
TELEGRAM_API_HASH=________
TELEGRAM_PHONE=________
SOURCE_GROUP_IDS=________
DEST_CHANNEL_ID=________
```

---

## 🔥 PASO 1: GitHub (5 minutos)

### 1. Crear repo
- Ve a: https://github.com/new
- Nombre: `trading-bot-monitor`
- Visibilidad: **PRIVADO** 🔒
- Clic "Create"

### 2. Subir código
PowerShell en tu carpeta:

```powershell
cd "D:\FUTUROS 2026"
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/TUUSUARIO/trading-bot-monitor.git
git branch -M main
git push -u origin main
```

Si pide password → Usa Personal Access Token de GitHub

✅ Verificar en GitHub que se subió todo

---

## 🌐 PASO 2: Render (3 minutos)

### 1. Crear cuenta
- Ve a: https://render.com
- Registra con GitHub

### 2. Nuevo servicio
- Clic "New +" → "Background Worker"
- Selecciona tu repo `trading-bot-monitor`
- Configuración:
  - **Name**: `trading-bot-monitor`
  - **Environment**: Python 3
  - **Build**: `pip install -r requirements.txt`
  - **Start**: `python monitor_grupos.py`
  - **Plan**: Free
- Clic "Create" (NO deploy todavía)

---

## 🔑 PASO 3: Variables (5 minutos)

En tu servicio → pestaña "Environment" → Agregar:

```
TELEGRAM_API_ID = copia_tu_valor_aqui
TELEGRAM_API_HASH = copia_tu_valor_aqui
TELEGRAM_PHONE = copia_tu_valor_aqui
SOURCE_GROUP_IDS = copia_tu_valor_aqui
DEST_CHANNEL_ID = copia_tu_valor_aqui
BINANCE_API_KEY = copia_tu_valor_aqui (opcional)
BINANCE_API_SECRET = copia_tu_valor_aqui (opcional)
```

Clic "Save Changes"

---

## 🚀 PASO 4: Deploy (2 minutos)

1. Clic "Manual Deploy" → "Deploy latest commit"
2. Espera 2-3 minutos
3. Ve a "Logs"
4. Busca: `✅ Conectado!`

---

## ✅ VERIFICAR

- [ ] Logs muestran "Monitoreo iniciado"
- [ ] Envía mensaje de prueba en tu grupo
- [ ] Revisa que aparece en j77

**🎉 ¡LISTO! Bot corriendo 24/7 gratis**

---

## 📁 Archivo de Sesión (IMPORTANTE)

Tu `session_name.session` debe estar en el servidor.

**Opción más fácil**: Súbelo a GitHub

```powershell
git add session_name.session
git commit -m "Add session"
git push
```

Render lo tomará automáticamente.

---

## 🆘 ¿Problemas?

Lee: `CHECKLIST_DESPLIEGUE.md` (guía paso a paso detallada)

O: `DEPLOY_RENDER_FACIL.md` (guía completa con soluciones)

---

## 💡 TIP

Después del primer despliegue, cualquier cambio que hagas:

```powershell
git add .
git commit -m "Cambio X"
git push
```

Render lo despliega automáticamente. ¡Sin hacer nada más!

---

**¿Listo?** Empieza con el Paso 1 ⬆️
