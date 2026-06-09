# 📱 FLUJO DE MENSAJES AL CANAL J77

**Canal destino:** j77 (ID configurado en .env)  
**Comportamiento:** Mensajes editables (no spam)

---

## 📊 MENSAJES QUE SE ENVÍAN

### 1️⃣ MENSAJE INICIAL (Al detectar evento)

**Cuándo:** Inmediatamente al detectar señal FIBO o VOLUMEN válida

**Estado:** `🔄 EN ANÁLISIS`

**Contenido:**
```markdown
🔄 EN ANÁLISIS 🔄

Origen: [Nombre del Grupo]

━━━━━━━━━━━━━━━━━━━━━━
📊 BTCUSDT 🟢 LONG
⏱️ Timeframe: FIBO_4H
✅ Vigencia: VIGENTE
━━━━━━━━━━━━━━━━━━━━━━

🟡 SCORE: 68.0/100
💪 FUERTE

━━━━━━━━━━━━━━━━━━━━━━
📊 MÉTRICAS:

• OI: 75/100
  OI incrementando sostenidamente

• Funding: 60/100
  FR neutral

• CVD: 70/100
  Absorción visible

• Delta: 65/100
  Compras agresivas incrementando

[... más métricas ...]

━━━━━━━━━━━━━━━━━━━━━━
⭐ TOP 3 FACTORES:
1. OI: Incremento sostenido (18.8 pts)
2. CVD: Absorción visible (17.5 pts)
3. Delta: Compras agresivas (13.0 pts)

⏰ 14:32:18

Motor de Clasificación v2.0 (Umbral: 75)
```

**Frecuencia:** 1 mensaje por señal detectada

---

### 2️⃣ MENSAJE ACTUALIZADO (Al cambiar estado)

**Cuándo:** Cuando el evento termina su análisis y cambia a estado final

**Estados posibles:**
- `🚀 ALTA PRIORIDAD` (Score >= 75)
- `💪 FUERTE` (Score 60-74)
- `👀 INTERESANTE` (Score 50-59)
- `📉 RUIDO` (Score < 50)
- `⏰ ENTRADA EXPIRADA` (precio se alejó >3%)
- `❌ INVALIDADA` (invalidación extrema)

**Contenido:**
```markdown
🚀🚀🚀 ALTA PRIORIDAD 🚀🚀🚀

Origen: [Nombre del Grupo]

━━━━━━━━━━━━━━━━━━━━━━
📊 BTCUSDT 🟢 LONG
⏱️ Timeframe: FIBO_4H
✅ Vigencia: VIGENTE
━━━━━━━━━━━━━━━━━━━━━━

🟢 SCORE: 77.5/100
🚀 ALTA PRIORIDAD

━━━━━━━━━━━━━━━━━━━━━━
⏱️ SEGUIMIENTO EN TIEMPO REAL
📈 FIBO_4H
━━━━━━━━━━━━━━━━━━━━━━

⏱️ Tiempo: 450s / 1200s
🔍 Checks: 30/80
⚡ Intervalo: 15seg
✅ Decisión tomada: 🚀 ALTA PRIORIDAD

📊 SCORES:
• Inicial: 68.0
• Actual: 77.5
• Máximo: 78.2
• Promedio: 73.8
📈 Tendencia: MEJORANDO (+1.2 pts/check)

📈 EVOLUCIÓN:
68 → 70 → 72 → 75 → 78

💰 PRECIO:
• Entrada: $45000.00000000
• Actual: $45120.00000000
• Distancia: +0.27%

━━━━━━━━━━━━━━━━━━━━━━
📊 MÉTRICAS:
[... métricas actualizadas ...]

━━━━━━━━━━━━━━━━━━━━━━
⭐ TOP 3 FACTORES:
[... factores finales ...]

⏰ 14:39:45

Motor de Clasificación v2.0 (Umbral: 75)
```

**Frecuencia:** 1 actualización por señal (edita el mensaje original)

---

## 🔄 COMPORTAMIENTO DEL SISTEMA

### Flujo Completo:

```
1. Señal detectada en grupo fuente
   ↓
2. Parser extrae: símbolo, dirección, entradas
   ↓
3. Binance: obtener datos de mercado
   ↓
4. Classifier: calcular score inicial
   ↓
5. ✅ Mensaje INICIAL enviado a j77
   ↓
6. Event Tracker: monitoreo cada 10/15 seg
   ↓
7. Checks periódicos: recalcular score
   ↓
8. Estado cambia (ALTA_PRIORIDAD/FUERTE/etc.)
   ↓
9. ✅ Mensaje ACTUALIZADO (edita el anterior)
   ↓
10. Tracking terminado
```

---

## ⏱️ TEMPORALIDAD

### VOLUMEN (1M)
```
Mensaje inicial: Inmediato al detectar
Checks: Cada 10 segundos
Actualización: Después de 2-20 minutos
```

### FIBO_1H
```
Mensaje inicial: Inmediato al detectar
Checks: Cada 15 segundos
Actualización: Después de 5-20 minutos
```

### FIBO_4H
```
Mensaje inicial: Inmediato al detectar
Checks: Cada 15 segundos
Actualización: Después de 7-20 minutos
```

### FIBO_1D
```
Mensaje inicial: Inmediato al detectar
Checks: Cada 15 segundos
Actualización: Después de 10-20 minutos
```

---

## 📋 TIPOS DE MENSAJES FINALES

### ✅ EJECUTABLES (Recibir notificación)

#### 🚀 ALTA PRIORIDAD (Score >= 75)
```
Estado: EJECUTAR
Emoji: 🚀🚀🚀
Color: 🟢 Verde
Acción: Revisar y ejecutar operación
```

**Ejemplo:**
```
🚀🚀🚀 ALTA PRIORIDAD 🚀🚀🚀
BTCUSDT 🟢 LONG
Score: 77.5/100
Tendencia: MEJORANDO
→ Señal ejecutable
```

---

### 📊 INFORMATIVOS (Solo monitoreo)

#### 💪 FUERTE (Score 60-74)
```
Estado: OBSERVAR
Emoji: 💪💪
Color: 🟡 Amarillo
Acción: Informativo (no alcanzó umbral)
```

**Ejemplo:**
```
💪💪 FUERTE 💪💪
ETHUSDT 🔴 SHORT
Score: 68.0/100
Tendencia: ESTABLE
→ No alcanzó 75, solo informativo
```

#### 👀 INTERESANTE (Score 50-59)
```
Estado: MONITOREAR
Emoji: 👀
Color: 🟡 Amarillo
Acción: Informativo (señal débil)
```

---

### ❌ DESCARTADAS (Ignorar)

#### 📉 RUIDO (Score < 50)
```
Estado: DESCARTAR
Emoji: 📉
Color: 🔴 Rojo
Acción: Ignorar completamente
```

#### ⏰ ENTRADA EXPIRADA
```
Estado: EXPIRADA
Emoji: ⏰
Color: 🔴 Rojo
Acción: Precio se alejó >3%, ya no válida
```

#### ❌ INVALIDADA
```
Estado: INVALIDADA
Emoji: ❌
Color: 🔴 Rojo
Acción: Invalidación extrema detectada
```

---

## 📈 VOLUMEN DE MENSAJES

### Estimación Diaria (Mercado Normal)

**Señales detectadas:** ~50-100/día

**Distribución:**
- 🚀 ALTA PRIORIDAD: 5-10 (ejecutables)
- 💪 FUERTE: 10-15 (informativos)
- 👀 INTERESANTE: 15-20 (informativos)
- 📉 RUIDO: 20-50 (descartadas)
- ⏰/❌ OTRAS: 5-10

**Mensajes en j77:** 50-100/día (1 inicial + 1 actualización por señal)

### Mercado Volátil
- Puede aumentar a 150-200 señales/día
- Mayor proporción de RUIDO
- Más señales ALTA PRIORIDAD

---

## 🎯 CONFIGURACIÓN ACTUAL

### Canal Destino
```python
DEST_CHANNEL_ID = [ID de j77 desde .env]
```

### Comportamiento
- ✅ Edita mensajes (no spam)
- ✅ 1 mensaje por señal máximo
- ✅ Información completa en cada mensaje
- ✅ Historial de evolución visible

### Formato
- ✅ Markdown para formato
- ✅ Emojis para claridad visual
- ✅ Métricas detalladas
- ✅ Evolución de scores
- ✅ Información de tracking

---

## 🔧 PERSONALIZACIÓN

### Filtrar Mensajes (Futuro)

Si solo quieres recibir ALTA PRIORIDAD:

```python
# En tracking_callback, agregar:
if evento_tracked.status != EventStatus.ALTA_PRIORIDAD:
    return  # No enviar mensaje
```

### Notificaciones
- Todas las señales se envían
- Solo ALTA PRIORIDAD requiere acción
- El resto es informativo

---

## 📊 RESUMEN

### ¿Qué mensajes recibes en j77?

1. **Mensaje inicial** cuando se detecta señal (EN ANÁLISIS)
2. **Mensaje actualizado** cuando termina análisis (estado final)

### ¿Cuáles son accionables?

Solo: **🚀 ALTA PRIORIDAD** (Score >= 75)

### ¿Cuáles ignoras?

- 💪 FUERTE (informativo)
- 👀 INTERESANTE (informativo)
- 📉 RUIDO (descartar)
- ⏰ ENTRADA EXPIRADA (descartar)
- ❌ INVALIDADA (descartar)

### Frecuencia

- **Diaria:** 50-100 mensajes
- **Ejecutables:** 5-10 ALTA PRIORIDAD
- **Spam:** NO (edita mensajes)

---

**Configuración:** ✅ ACTIVA  
**Canal:** j77  
**Formato:** Markdown con edición  
**Umbral ejecución:** 75 puntos
