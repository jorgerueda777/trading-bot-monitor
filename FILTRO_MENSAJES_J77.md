# 🔇 FILTRO DE MENSAJES - Canal J77

**Configuración:** Solo ALTA PRIORIDAD y FUERTE  
**Fecha:** 2026-06-08  
**Status:** ✅ ACTIVO

---

## 🎯 REGLA DE FILTRADO

### ✅ SE ENVÍAN A J77:

```
🚀 ALTA PRIORIDAD  (Score >= 75)
💪 FUERTE          (Score 60-74)
```

### 🔇 NO SE ENVÍAN (Filtradas):

```
👀 INTERESANTE     (Score 50-59)  → FILTRADO
📉 RUIDO           (Score < 50)   → FILTRADO
⏰ ENTRADA EXPIRADA               → FILTRADO
❌ INVALIDADA                     → FILTRADO
```

---

## 📊 LÓGICA IMPLEMENTADA

### Filtro 1: Mensaje Inicial

**Condición:**
```python
if resultado.final_score >= 60:
    # Enviar mensaje inicial a j77
else:
    # NO enviar, solo log local
```

**Resultado:**
- Score >= 60: Envía mensaje "EN ANÁLISIS" a j77
- Score < 60: No envía nada, solo procesa localmente

### Filtro 2: Mensaje Final

**Condición:**
```python
if evento.status in [ALTA_PRIORIDAD, FUERTE]:
    # Actualizar mensaje en j77
else:
    # Eliminar mensaje inicial (si existe)
    # NO enviar actualización
```

**Resultado:**
- ALTA PRIORIDAD o FUERTE: Actualiza mensaje
- Otros estados: Elimina mensaje inicial y no notifica

---

## 🔄 FLUJOS POSIBLES

### Caso 1: Score alto desde inicio
```
Detectado: Score = 68 💪
   ↓
✅ Mensaje inicial enviado (EN ANÁLISIS)
   ↓
Tracking: 68 → 70 → 73 → 76
   ↓
Final: Score = 76 🚀
   ↓
✅ Mensaje actualizado (ALTA PRIORIDAD)
```

### Caso 2: Score alto que deteriora
```
Detectado: Score = 62 💪
   ↓
✅ Mensaje inicial enviado (EN ANÁLISIS)
   ↓
Tracking: 62 → 60 → 57 → 54
   ↓
Final: Score = 54 👀
   ↓
🗑️ Mensaje eliminado de j77
🔇 NO se notifica (filtrado)
```

### Caso 3: Score bajo desde inicio
```
Detectado: Score = 48 📉
   ↓
🔇 NO se envía mensaje inicial
   ↓
Tracking local: 48 → 45 → 42
   ↓
Final: Score = 42 📉
   ↓
🔇 NO se notifica (ya estaba filtrado)
```

### Caso 4: Score medio que mejora
```
Detectado: Score = 52 👀
   ↓
🔇 NO se envía mensaje inicial
   ↓
Tracking local: 52 → 58 → 65 → 72
   ↓
Final: Score = 72 💪
   ↓
❌ NO se notifica (no hubo mensaje inicial)
```

**NOTA:** Este último caso podría mejorarse para enviar notificación cuando una señal mejora significativamente.

---

## 📈 IMPACTO EN VOLUMEN

### Antes del Filtro
```
Señales detectadas: 100/día
Mensajes en j77: 100/día (todas)

Distribución:
- 🚀 ALTA: 5-10
- 💪 FUERTE: 10-15
- 👀 INTERESANTE: 15-20
- 📉 RUIDO: 60-70
```

### Después del Filtro
```
Señales detectadas: 100/día
Mensajes en j77: 15-25/día (solo relevantes)

Distribución en j77:
- 🚀 ALTA: 5-10
- 💪 FUERTE: 10-15
- (resto filtrado)
```

**Reducción:** ~75-80% menos mensajes en j77

---

## 🎯 BENEFICIOS

### 1. Menos Ruido
- Solo señales con potencial real
- Canal j77 más limpio
- Fácil revisar historial

### 2. Más Foco
- Solo ALTA y FUERTE visibles
- Decisiones más rápidas
- Menos distracción

### 3. Mayor Calidad
- Score mínimo 60 garantizado
- Señales pre-filtradas
- Mayor probabilidad de éxito

---

## ⚙️ CONFIGURACIÓN

### Umbral Actual
```python
UMBRAL_MINIMO_J77 = 60  # Score mínimo para enviar

Estados permitidos:
- ALTA_PRIORIDAD (>= 75)
- FUERTE (60-74)
```

### Cambiar Umbral (si necesario)

**Para solo ALTA PRIORIDAD:**
```python
# En monitor_grupos.py, línea ~513
if resultado.final_score >= 75:  # Cambiar de 60 a 75
```

**Para incluir INTERESANTE:**
```python
# En monitor_grupos.py, línea ~513
if resultado.final_score >= 50:  # Cambiar de 60 a 50
```

---

## 📊 LOGS

### Señal Enviada
```
✅ Score >= 60: Enviando a j77
📤 Enviando estado inicial a j77...
✅ Mensaje enviado al canal
```

### Señal Filtrada (Score inicial bajo)
```
🔇 Score < 60: NO se envía a j77 (filtrado)
ℹ️ Solo se envían señales con score >= 60
```

### Señal Filtrada (Estado final)
```
🔔 Evento cambió a: 👀 INTERESANTE
   🔇 Estado INTERESANTE no se notifica (filtrado)
   🗑️ Mensaje inicial eliminado de j77 (señal filtrada)
```

---

## 🔍 REVISIÓN DE SEÑALES FILTRADAS

### Opción 1: Logs Locales
Todas las señales se procesan y logean localmente, incluso las filtradas.

```
📊 Consultando Binance para SYMBOL...
✅ Clasificado: 48.0/100 - RUIDO
🔇 Score < 60: NO se envía a j77
```

### Opción 2: Archivo de Historial
El sistema guarda todas las clasificaciones en:
```
data/classifications/classifications_YYYY-MM-DD.jsonl
```

Incluye señales filtradas con sus scores.

---

## 🎬 EJEMPLO REAL

### Mensaje en j77:
```markdown
🔄 EN ANÁLISIS 🔄

Origen: Grupo Trading Oficial

━━━━━━━━━━━━━━━━━━━━━━
📊 BTCUSDT 🟢 LONG
⏱️ Timeframe: FIBO_4H
✅ Vigencia: VIGENTE
━━━━━━━━━━━━━━━━━━━━━━

🟡 SCORE: 68.0/100
💪 FUERTE

[... métricas ...]
```

**Después de 7 minutos:**

### Si mejora a ALTA:
```markdown
🚀🚀🚀 ALTA PRIORIDAD 🚀🚀🚀

[... mismo mensaje actualizado ...]

🟢 SCORE: 77.0/100
🚀 ALTA PRIORIDAD

📊 SCORES:
• Inicial: 68.0
• Actual: 77.0
• Máximo: 78.2
• Promedio: 73.5
📈 Tendencia: MEJORANDO
```

### Si deteriora a INTERESANTE:
```
Mensaje eliminado de j77
(Sin notificación de estado final)
```

---

## ✅ RESUMEN

### ¿Qué ves en j77?

Solo señales con **score >= 60**:
- 🚀 ALTA PRIORIDAD (>=75)
- 💪 FUERTE (60-74)

### ¿Qué NO ves?

Todo con score < 60:
- 👀 INTERESANTE (50-59)
- 📉 RUIDO (<50)
- Estados de error

### Volumen esperado

- **15-25 mensajes/día** (vs 100 sin filtro)
- **75-80% reducción de ruido**
- **Solo señales relevantes**

---

**Status:** ✅ FILTRO ACTIVO  
**Umbral:** Score >= 60  
**Estados permitidos:** ALTA PRIORIDAD, FUERTE  
**Reducción ruido:** ~75-80%
