# Guía de Despliegue - Paso a Paso

**Objetivo**: Tener tu bot corriendo 24/7 en la nube GRATIS

---

## 🎯 DECISIÓN RÁPIDA

### ¿Qué opción eliges?

**OPCIÓN A - La MÁS FÁCIL (5 minutos)**
- Plataforma: **Railway.app**
- Tiempo: 5 minutos
- Dificultad: ⭐ (muy fácil)
- Duración gratis: 23 días/mes
- **➡️ Salta a la sección "OPCIÓN A" abajo**

**OPCIÓN B - GRATIS PERMANENTE (15 minutos)**
- Plataforma: **Fly.io**
- Tiempo: 15 minutos
- Dificultad: ⭐⭐ (fácil)
- Duración gratis: Ilimitada
- **➡️ Salta a la sección "OPCIÓN B" abajo**

**OPCIÓN C - MÁXIMOS RECURSOS (45 minutos)**
- Plataforma: **Oracle Cloud**
- Tiempo: 45 minutos
- Dificultad: ⭐⭐⭐⭐ (necesitas conocimientos Linux)
- Duración gratis: Ilimitada + 24GB RAM
- **➡️ Salta a la sección "OPCIÓN C" abajo**

---

## 📍 OPCIÓN A: Railway.app (LA MÁS FÁCIL)

### Paso 1: Crear cuenta en Railway
1. Ve a: https://railway.app
2. Clic en "Start a New Project"
3. Conecta con GitHub (o crea cuenta con email)

### Paso 2: Subir tu código a GitHub
```bash
# En tu carpeta del proyecto (D:\FUTUROS 2026)
git init
git add .
git commit -m "Initial commit - Trading Bot"

# Crear repo en GitHub:
# - Ve a https://github.com/new
# - Nombre: "trading-bot-monitor"
# - Privado: SÍ (para proteger tus claves)
# - Clic "Create repository"

# Conectar y subir:
git remote add origin https://github.com/TU_USUARIO/trading-bot-monitor.git
git branch -M main
git push -u origin main
```

### Paso 3: Desplegar en Railway
1. En Railway, clic "New Project"
2. Selecciona "Deploy from GitHub repo"
3. Elige tu repo "trading-bot-monitor"
4. Railway detectará Python automáticamente

### Paso 4: Configurar variables de entorno
1. En Railway, ve a tu proyecto
2. Clic en "Variables"
3. Agrega TODAS estas variables (copiar de tu .env):

```
TELEGRAM_API_ID=tu_valor
TELEGRAM_API_HASH=tu_valor
TELEGRAM_PHONE=tu_valor
SOURCE_GROUP_IDS=tu_valor
DEST_CHANNEL_ID=tu_valor
BINANCE_API_KEY=tu_valor
BINANCE_API_SECRET=tu_valor
```

### Paso 5: Subir archivo de sesión
**IMPORTANTE**: Tu archivo `session_name.session` debe estar en el servidor

Opción 1 - Incluirlo en el repo (NO recomendado, pero más fácil):
```bash
# Agregar sesión al repo
git add session_name.session
git commit -m "Add session file"
git push
```

Opción 2 - Regenerar sesión en el servidor:
- Primera vez ejecuta en Railway
- Te pedirá código de Telegram
- Usa los logs de Railway para ver el código

### Paso 6: ¡Listo!
- Railway desplegará automáticamente
- Verás los logs en tiempo real
- Tu bot estará corriendo 24/7

**Costo**: Gratis por ~23 días/mes (con $5 de crédito gratuito)

---

## 📍 OPCIÓN B: Fly.io (GRATIS PERMANENTE)

### Paso 1: Instalar Fly CLI
```bash
# Windows (PowerShell):
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"

# Reinicia tu terminal después
```

### Paso 2: Crear cuenta
```bash
fly auth signup
# O si ya tienes cuenta:
fly auth login
```

### Paso 3: Preparar tu proyecto
Ya tienes el `Dockerfile` creado. Solo necesitas:

```bash
# En tu carpeta del proyecto
cd "D:\FUTUROS 2026"

# Inicializar app en Fly.io
fly launch

# Te preguntará:
# - App name: trading-bot-monitor (o el que quieras)
# - Region: elige la más cercana (ej: "mia" para Miami)
# - Crear database: NO
# - Deploy ahora: NO (todavía)
```

### Paso 4: Configurar variables de entorno
```bash
# Agregar TODAS tus variables:
fly secrets set TELEGRAM_API_ID=tu_valor
fly secrets set TELEGRAM_API_HASH=tu_valor
fly secrets set TELEGRAM_PHONE=tu_valor
fly secrets set SOURCE_GROUP_IDS=tu_valor
fly secrets set DEST_CHANNEL_ID=tu_valor
fly secrets set BINANCE_API_KEY=tu_valor
fly secrets set BINANCE_API_SECRET=tu_valor
```

### Paso 5: Crear volumen persistente (para la sesión)
```bash
# Crear volumen de 1GB
fly volumes create bot_data --size 1 --region mia

# Modificar fly.toml para montar el volumen
# (ya está configurado en el archivo que creé)
```

### Paso 6: Desplegar
```bash
fly deploy
```

### Paso 7: Ver logs
```bash
# Ver logs en tiempo real
fly logs

# Ver estado
fly status
```

### Paso 8: Manejar la sesión de Telegram
**Primera vez**: La sesión se creará en el servidor
```bash
# Si necesitas conectarte a la VM:
fly ssh console

# Dentro de la VM, ejecuta el bot manualmente una vez:
python monitor_grupos.py
# Te pedirá el código de Telegram
```

**Costo**: Gratis para siempre (dentro del tier free)

---

## 📍 OPCIÓN C: Oracle Cloud (MÁXIMOS RECURSOS)

### Paso 1: Crear cuenta Oracle Cloud
1. Ve a: https://cloud.oracle.com/free
2. Registrate (requiere tarjeta, pero NO cobra)
3. Selecciona región más cercana

### Paso 2: Crear una VM
1. En el dashboard, "Create a VM instance"
2. Selecciona:
   - Shape: Ampere (ARM) - Always Free
   - OS: Ubuntu 22.04
   - RAM: 24GB (gratis!)
   - Storage: 50GB
3. Guarda la clave SSH privada

### Paso 3: Conectarte a la VM
```bash
# Windows (necesitas SSH client)
ssh -i ruta/a/tu/clave.key ubuntu@IP_DE_TU_VM
```

### Paso 4: Instalar dependencias en la VM
```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip git -y

# Clonar tu repositorio (necesitas subirlo a GitHub primero)
git clone https://github.com/TU_USUARIO/trading-bot-monitor.git
cd trading-bot-monitor

# Crear entorno virtual
python3.11 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Paso 5: Configurar variables de entorno
```bash
# Crear archivo .env
nano .env

# Pegar todas tus variables:
TELEGRAM_API_ID=tu_valor
TELEGRAM_API_HASH=tu_valor
...etc
# Guardar: Ctrl+X, Y, Enter
```

### Paso 6: Primera ejecución (crear sesión)
```bash
python monitor_grupos.py
# Te pedirá código de Telegram
# Ingresa el código
# Se creará session_name.session
```

### Paso 7: Configurar para que corra siempre
```bash
# Crear servicio systemd
sudo nano /etc/systemd/system/trading-bot.service
```

Contenido:
```ini
[Unit]
Description=Trading Bot Monitor
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/trading-bot-monitor
Environment=PATH=/home/ubuntu/trading-bot-monitor/venv/bin
ExecStart=/home/ubuntu/trading-bot-monitor/venv/bin/python monitor_grupos.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Habilitar y arrancar servicio
sudo systemctl enable trading-bot
sudo systemctl start trading-bot

# Ver logs
sudo journalctl -u trading-bot -f
```

**Costo**: Gratis para siempre

---

## 🎯 MI RECOMENDACIÓN FINAL

### Si quieres empezar HOY MISMO (5 minutos):
➡️ **USA RAILWAY** (Opción A)

### Si quieres gratis permanente pero fácil:
➡️ **USA FLY.IO** (Opción B)

### Si quieres máximo control:
➡️ **USA ORACLE CLOUD** (Opción C)

---

## ⚠️ NOTA IMPORTANTE: Archivo de Sesión

Tu archivo `session_name.session` contiene tu sesión de Telegram.

**Opciones para manejarlo**:

1. **Subirlo al repo** (privado): Fácil pero menos seguro
2. **Subirlo manualmente**: Más seguro
3. **Regenerarlo en el servidor**: Mejor opción

**Para regenerar en el servidor**:
- Primera vez que corra el bot en la nube
- Telegram te enviará un código
- Ingrésalo en los logs/consola
- Se creará la sesión automáticamente

---

## ❓ ¿Qué opción eliges?

Dime cuál prefieres y te guío paso a paso en ESA opción específica.
