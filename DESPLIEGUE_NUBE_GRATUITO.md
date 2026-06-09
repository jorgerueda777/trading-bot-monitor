# Despliegue en la Nube - Opciones Gratuitas

**Fecha**: 2026-06-09  
**Objetivo**: Mantener el bot corriendo 24/7 sin costo

---

## Opciones Recomendadas (Mejores Primero)

### 🥇 OPCIÓN 1: Railway.app (RECOMENDADO)
**Nivel gratuito**: $5 crédito mensual (~550 horas = 23 días)

**✅ PROS**:
- Más fácil de configurar
- Soporte Python nativo
- Variables de entorno fáciles
- Persistencia de sesión Telegram
- 512MB RAM (suficiente)
- 1 vCPU compartido
- Despliegue desde GitHub automático

**❌ CONTRAS**:
- Se acaba después de ~23 días/mes
- Requiere tarjeta para verificación (no cobra)

**Ideal para**: Comenzar rápido, testing en producción

---

### 🥈 OPCIÓN 2: Render.com
**Nivel gratuito**: Ilimitado pero con suspensión

**✅ PROS**:
- 750 horas/mes (31 días completos)
- 512MB RAM
- Python nativo
- Despliegue desde GitHub
- Variables de entorno
- SSL gratis

**❌ CONTRAS**:
- Se suspende después de 15 min de inactividad
- Tu bot es "siempre activo" así que funciona bien
- Lento para arrancar (puede tardar 1-2 min)

**Ideal para**: Uso continuo sin costo

---

### 🥉 OPCIÓN 3: Fly.io
**Nivel gratuito**: 3 VMs pequeñas, 160GB transferencia

**✅ PROS**:
- Realmente gratis indefinidamente
- 256MB RAM x 3 máquinas
- Despliegue con Dockerfile
- No se suspende
- Buena latencia global

**❌ CONTRAS**:
- Configuración más compleja (Dockerfile)
- Menos RAM (256MB puede ser justo)
- Requiere tarjeta de crédito para verificación

**Ideal para**: Despliegue permanente sin límites

---

### 🏅 OPCIÓN 4: Oracle Cloud Always Free
**Nivel gratuito**: 4 ARM cores, 24GB RAM (GENEROSO)

**✅ PROS**:
- Realmente gratis PARA SIEMPRE
- Recursos muy generosos (24GB RAM!)
- 2 VMs gratuitas
- No se suspende nunca
- Máximo control

**❌ CONTRAS**:
- Configuración manual completa (Linux VM)
- Requiere conocimientos de servidor
- Debes mantener la VM (updates, seguridad)
- Proceso de registro puede rechazar (alta demanda)

**Ideal para**: Si sabes manejar servidores Linux

---

### ⚡ OPCIÓN 5: Replit
**Nivel gratuito**: Limitado pero funcional

**✅ PROS**:
- Super fácil (copiar y pegar código)
- No requiere Docker ni Git
- IDE en navegador
- Gratis básico

**❌ CONTRAS**:
- Se suspende después de inactividad
- Recursos muy limitados
- No ideal para producción
- Puede perder sesión de Telegram

**Ideal para**: Pruebas rápidas, no producción

---

### 🔵 OPCIÓN 6: Google Cloud Run
**Nivel gratuito**: 2M requests/mes, siempre gratis

**✅ PROS**:
- Realmente gratis para siempre
- Escala automáticamente
- 1GB RAM
- 180K vCPU-seconds/mes

**❌ CONTRAS**:
- Tu bot es "long-running" no "request-based"
- Puede ser complicado para bots persistentes
- Requiere configuración de "minimum instances"

**Ideal para**: APIs, no tanto para bots 24/7

---

## Comparación Rápida

| Plataforma | RAM | Tiempo activo | Facilidad | Persistencia | Mejor para |
|------------|-----|---------------|-----------|--------------|------------|
| **Railway** | 512MB | 23 días/mes | ⭐⭐⭐⭐⭐ | ✅ | Empezar rápido |
| **Render** | 512MB | 31 días/mes | ⭐⭐⭐⭐ | ✅ | Uso continuo |
| **Fly.io** | 256MB | Ilimitado | ⭐⭐⭐ | ✅ | Long-term gratis |
| **Oracle** | 24GB | Ilimitado | ⭐⭐ | ✅ | Máximo control |
| **Replit** | 128MB | Limitado | ⭐⭐⭐⭐⭐ | ❌ | Testing rápido |

---

## 🎯 MI RECOMENDACIÓN

### Para empezar HOY (5 minutos):
➡️ **Railway.app** - La más fácil, funciona perfectamente 23 días/mes

### Para producción GRATIS permanente:
➡️ **Fly.io** - Balance perfecto entre facilidad y gratuidad

### Si sabes manejar servidores:
➡️ **Oracle Cloud** - Recursos masivos gratis para siempre

---

## Próximos Pasos

¿Qué prefieres?

1. **Rápido y fácil** → Te ayudo con Railway (5 min)
2. **Gratis permanente** → Te ayudo con Fly.io (15 min)
3. **Máximo control** → Te ayudo con Oracle Cloud (30 min)

---

## Archivos que necesitarás

Para cualquier opción, necesitaremos crear:

### 1. `Procfile` o `start.sh`
```bash
python monitor_grupos.py
```

### 2. `Dockerfile` (para Fly.io/Render)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "monitor_grupos.py"]
```

### 3. Variables de entorno
Tu `.env` debe estar configurado en la plataforma

### 4. Persistencia de sesión
La sesión de Telegram (`session_name.session`) debe persistir

---

## ⚠️ CONSIDERACIÓN IMPORTANTE

Tu bot usa **Telethon UserBot**, que requiere:
- Sesión persistente (archivo `.session`)
- Conexión continua a Telegram
- No puede reiniciarse frecuentemente

**Mejor opción para tu caso**: 
1. **Fly.io** (no se reinicia, sesión persiste)
2. **Railway** (fácil, sesión persiste)
3. **Oracle Cloud** (máximo control)

**Evitar**:
- Replit (pierde sesión)
- Plataformas que reinician cada hora

---

## Necesidades de tu Bot

- **RAM**: ~200-300MB (cualquier opción funciona)
- **CPU**: Mínima (checks cada 5-10 seg)
- **Red**: Conexión estable a Telegram + Binance
- **Almacenamiento**: Persistir `.session` y logs
- **Tiempo activo**: 24/7 sin interrupciones

**Conclusión**: Railway o Fly.io son tus mejores opciones.
