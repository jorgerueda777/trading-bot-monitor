# ✅ Checklist de Despliegue - Render.com

Sigue estos pasos EN ORDEN. Marca cada uno cuando lo completes.

---

## 📋 PREPARACIÓN (Antes de empezar)

- [ ] Tengo mi archivo `.env` con todas las credenciales
- [ ] Tengo cuenta en GitHub (si no: https://github.com/signup)
- [ ] Mi bot funciona correctamente en local (probado)
- [ ] Tengo mi archivo `session_name.session` (generado al correr el bot)

---

## 🔐 PASO 1: Proteger Archivos Sensibles

- [ ] Verificar que existe el archivo `.gitignore` en la raíz del proyecto
- [ ] El `.gitignore` contiene:
  ```
  .env
  .env.local
  *.log
  ```
- [ ] **DECISIÓN**: ¿Vas a subir `session_name.session` al repo?
  - [ ] **SÍ** → Asegúrate que el repo será PRIVADO
  - [ ] **NO** → Descomenta `# session_name.session` en `.gitignore`

---

## 📤 PASO 2: Subir Código a GitHub (10 minutos)

### 2.1 Crear repositorio en GitHub

- [ ] Ir a: https://github.com/new
- [ ] Llenar datos:
  - Nombre: `trading-bot-monitor`
  - Visibilidad: 🔒 **PRIVADO**
  - NO marcar ninguna casilla
- [ ] Clic "Create repository"
- [ ] **Copiar** la URL del repo (ejemplo: `https://github.com/tuusuario/trading-bot-monitor.git`)

### 2.2 Inicializar Git en tu proyecto

Abrir PowerShell en `D:\FUTUROS 2026`:

- [ ] Ejecutar: `git init`
- [ ] Ejecutar: `git add .`
- [ ] Ejecutar: `git commit -m "Initial commit - Trading bot"`

### 2.3 Conectar con GitHub

- [ ] Ejecutar (reemplaza la URL con la tuya):
  ```powershell
  git remote add origin https://github.com/TUUSUARIO/trading-bot-monitor.git
  ```
- [ ] Ejecutar: `git branch -M main`
- [ ] Ejecutar: `git push -u origin main`

Si pide login:
- [ ] Usuario: tu username de GitHub
- [ ] Password: necesitas crear un Personal Access Token
  - [ ] Ir a: https://github.com/settings/tokens
  - [ ] Clic "Generate new token (classic)"
  - [ ] Marcar: `repo` (todos los permisos)
  - [ ] Generar y copiar el token
  - [ ] Usar el token como password

### 2.4 Verificar

- [ ] Ir a tu repo en GitHub
- [ ] Verificar que aparecen todos los archivos
- [ ] Verificar que el repo es PRIVADO (candado 🔒)

---

## 🚀 PASO 3: Crear Cuenta en Render (2 minutos)

- [ ] Ir a: https://render.com
- [ ] Clic "Get Started"
- [ ] Registrarse con GitHub (más fácil)
- [ ] Autorizar a Render

---

## ⚙️ PASO 4: Crear Servicio en Render (5 minutos)

### 4.1 Nuevo servicio

- [ ] En Render dashboard, clic "New +"
- [ ] Seleccionar "Background Worker"
- [ ] Si no ves tu repo:
  - [ ] Clic "Configure account"
  - [ ] Dar acceso a `trading-bot-monitor`
- [ ] Seleccionar `trading-bot-monitor`

### 4.2 Configurar servicio

Llenar campos:

- [ ] **Name**: `trading-bot-monitor`
- [ ] **Environment**: `Python 3`
- [ ] **Build Command**: `pip install -r requirements.txt`
- [ ] **Start Command**: `python monitor_grupos.py`
- [ ] **Plan**: Free
- [ ] Clic "Create Background Worker"

**⚠️ NO HACER DEPLOY TODAVÍA**

---

## 🔑 PASO 5: Configurar Variables de Entorno (5 minutos)

En tu servicio en Render:

- [ ] Ir a pestaña "Environment"
- [ ] Agregar las siguientes variables (copiar de tu `.env`):

```
Variable                  | Valor
--------------------------|------------------
TELEGRAM_API_ID           | (tu valor)
TELEGRAM_API_HASH         | (tu valor)
TELEGRAM_PHONE            | (tu valor)
SOURCE_GROUP_IDS          | (tu valor)
DEST_CHANNEL_ID           | (tu valor)
BINANCE_API_KEY           | (tu valor - opcional)
BINANCE_API_SECRET        | (tu valor - opcional)
```

- [ ] Hacer clic en "Add Variable" para cada una
- [ ] Verificar que todas están correctas (sin comillas, sin espacios extra)
- [ ] Clic "Save Changes"

**Total**: 7 variables (5 obligatorias + 2 opcionales de Binance)

---

## 📁 PASO 6: Manejar Archivo de Sesión (CRÍTICO)

Elige UNA de estas opciones:

### Opción A: Subir sesión al repo (MÁS FÁCIL)

- [ ] Verificar que el repo es PRIVADO
- [ ] En PowerShell:
  ```powershell
  git add session_name.session
  git commit -m "Add Telegram session"
  git push
  ```
- [ ] Verificar en GitHub que se subió el archivo

### Opción B: Regenerar sesión (MÁS SEGURO)

- [ ] Editar `.gitignore` y descomentar `session_name.session`
- [ ] Cuando el bot inicie por primera vez en Render:
  - [ ] Telegram te enviará un código
  - [ ] Ver logs en Render
  - [ ] Ingresar el código donde indique

**Recomendación**: Opción A para empezar rápido

---

## 🎬 PASO 7: Desplegar (2 minutos)

- [ ] En tu servicio en Render, clic "Manual Deploy"
- [ ] Clic "Deploy latest commit"
- [ ] Esperar 2-3 minutos (verás progreso)
- [ ] Estado debe cambiar a "Live" (verde)

---

## 🔍 PASO 8: Verificar que Funciona (5 minutos)

### 8.1 Revisar logs

- [ ] En Render, ir a pestaña "Logs"
- [ ] Buscar estas líneas:
  ```
  ✅ Conectado!
  📋 Grupos a monitorear:
  ✅ Monitoreo iniciado
  ```

### 8.2 Prueba real

- [ ] Enviar mensaje de prueba en uno de tus grupos monitoreados
- [ ] Revisar logs: debe aparecer "📩 Mensaje recibido"
- [ ] Si la señal califica (score ≥60):
  - [ ] Revisar tu canal destino (j77)
  - [ ] Debe aparecer el mensaje formateado

### 8.3 Verificación de métricas

- [ ] En Render, ir a "Metrics"
- [ ] Verificar:
  - CPU: < 10% (normal)
  - Memory: 100-200MB (normal)
  - No errores en últimos 5 minutos

---

## ✅ PASO 9: Confirmar Éxito

Si TODO lo anterior funcionó:

- [ ] ✅ Bot corriendo 24/7
- [ ] ✅ Recibe mensajes de grupos
- [ ] ✅ Clasifica señales
- [ ] ✅ Envía notificaciones a j77
- [ ] ✅ Logs visibles en Render

**🎉 ¡FELICIDADES! Tu bot está en producción**

---

## 🛠️ SOLUCIÓN DE PROBLEMAS

### ❌ Error: "Session file not found"

- [ ] Verificar que subiste `session_name.session` al repo
- [ ] O seguir Opción B para regenerar

### ❌ Error: "TELEGRAM_API_ID not found"

- [ ] Ir a Environment en Render
- [ ] Verificar que la variable existe
- [ ] Verificar que el valor es correcto (sin comillas)
- [ ] Clic "Save Changes"
- [ ] Hacer redeploy

### ❌ Error: "Module not found"

- [ ] Verificar que `requirements.txt` está en el repo
- [ ] Verificar que Build Command es: `pip install -r requirements.txt`
- [ ] Hacer redeploy con "Clear build cache"

### ❌ Bot se detiene después de desplegar

- [ ] Revisar logs completos
- [ ] Buscar línea con "Error" o "Exception"
- [ ] Verificar todas las variables de entorno

### ❌ No llegan mensajes al canal j77

- [ ] Verificar que las señales tienen score ≥60
- [ ] Revisar logs: buscar "Score < 60: NO se envía"
- [ ] Verificar DEST_CHANNEL_ID es correcto
- [ ] Verificar que el bot tiene permisos en j77

---

## 📊 MONITOREO DIARIO

Tareas recomendadas:

- [ ] Ver logs 1 vez al día
- [ ] Verificar que el bot sigue "Live" (verde)
- [ ] Revisar uso de recursos (debe ser < 50%)

---

## 🔄 ACTUALIZACIONES FUTURAS

Cuando hagas cambios al código:

```powershell
git add .
git commit -m "Descripción del cambio"
git push
```

Render desplegará automáticamente los cambios.

---

## 📞 SI NECESITAS AYUDA

1. Revisar "DEPLOY_RENDER_FACIL.md"
2. Revisar "GUIA_DESPLIEGUE_PASO_A_PASO.md"
3. Buscar error específico en los logs

---

**Tiempo total estimado**: 30 minutos
**Costo**: $0 (100% gratis)
**Resultado**: Bot corriendo 24/7 en la nube
