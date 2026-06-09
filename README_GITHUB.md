# Trading Bot Monitor 🤖📊

Bot de análisis automático de señales de trading desde grupos de Telegram.

## 🎯 Características

- ✅ Monitoreo en tiempo real de grupos de Telegram
- ✅ Clasificación inteligente de señales (FIBO y VOLUMEN)
- ✅ Integración con Binance para datos de mercado
- ✅ Scoring automático (0-100)
- ✅ Filtrado por prioridad (ALTA PRIORIDAD ≥75)
- ✅ Envío automático a canal de notificaciones
- ✅ Extracción de entrada, targets y stop loss

## 🚀 Despliegue en Render.com (GRATIS)

### Paso 1: Fork o copia este repositorio

### Paso 2: Crear servicio en Render
1. Ve a [render.com](https://render.com)
2. Crea un "Background Worker"
3. Conecta este repositorio

### Paso 3: Configurar variables de entorno

Agrega estas variables en Render:

```
TELEGRAM_API_ID=tu_api_id
TELEGRAM_API_HASH=tu_api_hash
TELEGRAM_PHONE=tu_telefono
SOURCE_GROUP_IDS=id1,id2,id3
DEST_CHANNEL_ID=tu_canal_destino
BINANCE_API_KEY=tu_api_key (opcional)
BINANCE_API_SECRET=tu_api_secret (opcional)
```

### Paso 4: Deploy

Render desplegará automáticamente.

## 📋 Requisitos

- Python 3.11+
- Telegram API credentials
- Binance API credentials (opcional)

## 🛠️ Instalación Local

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/trading-bot-monitor.git
cd trading-bot-monitor

# Instalar dependencias
pip install -r requirements.txt

# Configurar .env
cp .env.example .env
# Editar .env con tus credenciales

# Ejecutar
python monitor_grupos.py
```

## 📖 Documentación

- `DEPLOY_RENDER_FACIL.md` - Guía completa de despliegue
- `GUIA_DESPLIEGUE_PASO_A_PASO.md` - Guía detallada paso a paso
- `ARCHITECTURE.md` - Arquitectura del sistema
- `USAGE.md` - Uso y configuración

## 🔒 Seguridad

- ⚠️ **NUNCA** subas tu archivo `.env` al repositorio
- ⚠️ Mantén el repositorio **PRIVADO** si subes `session_name.session`
- ⚠️ Usa variables de entorno en producción

## 📊 Sistema de Clasificación

### Perfiles soportados:
- **FIBO**: Señales de Fibonacci (1H/4H/1D)
- **VOLUMEN**: Señales de volumen (1M)

### Escala de prioridad:
- 🚀 **ALTA PRIORIDAD**: ≥75 puntos
- 💪 **FUERTE**: 60-74 puntos
- 👀 **INTERESANTE**: 50-59 puntos
- 📉 **RUIDO**: <50 puntos

### Métricas evaluadas:
- Open Interest
- CVD (Cumulative Volume Delta)
- Delta
- Order Book (solo VOLUMEN)
- Momentum Decay (solo VOLUMEN)
- Liquidity Sweeps
- Funding Rate
- VWAP
- Volume (solo FIBO)

## 🎯 Filtrado de Mensajes

Solo se envían al canal destino:
- ✅ ALTA PRIORIDAD (score ≥75)
- ✅ FUERTE (score 60-74)

Mensajes filtrados:
- ❌ INTERESANTE (50-59)
- ❌ RUIDO (<50)
- ❌ ENTRADA_EXPIRADA
- ❌ INVALIDADA

## 📈 Intervalos de Verificación

- **VOLUMEN**: 5 segundos
- **FIBO**: 10 segundos

## 🔄 Observación Extendida

Señales con score ≥60:
- ⏱️ Observación extendida: hasta 20 minutos
- 🛡️ Protección contra descarte prematuro

## 📝 Logs

Los logs muestran:
- 📩 Mensajes recibidos
- 🔍 Eventos detectados
- ⚙️ Clasificación y scoring
- 📤 Mensajes enviados al canal
- 🔄 Estado de tracking

## 🤝 Contribuir

Este es un proyecto privado. Si tienes acceso y quieres contribuir:

1. Crea un branch
2. Haz tus cambios
3. Envía un pull request

## 📄 Licencia

Privado - Todos los derechos reservados

## 👤 Autor

Tu nombre aquí

## 📞 Soporte

Para soporte, abre un issue en GitHub.

---

**Nota**: Este bot requiere una sesión activa de Telegram. La primera vez que se ejecute, te pedirá un código de verificación.
