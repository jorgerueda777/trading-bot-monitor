# 🚀 ACTUALIZACIÓN MOTOR DE CLASIFICACIÓN V2.0

**Fecha:** 2026-06-08  
**Status:** ✅ COMPLETADO

---

## 📋 CAMBIOS IMPLEMENTADOS

### 1. NUEVA ESCALA DE CLASIFICACIÓN

Escala anterior (v1.0):
- ALTA PRIORIDAD: 85+ (VOLUMEN) / 80+ (FIBO)
- PRIORIDAD MEDIA: 60-84 / 60-79
- BAJA PRIORIDAD: <60

**Nueva escala (v2.0):**
```
🚀 ALTA PRIORIDAD:     Score >= 75    (Ambos perfiles)
💪 FUERTE:             Score 60-74
👀 INTERESANTE:        Score 50-59
📉 RUIDO:              Score < 50
```

### 2. UMBRAL UNIFICADO

**Antes:**
- VOLUMEN: 85 para ALTA PRIORIDAD
- FIBO: 80 para ALTA PRIORIDAD

**Ahora:**
- **AMBOS: 75 para ALTA PRIORIDAD** ✅

Razón: Simplifica la lógica y permite capturar oportunidades válidas más temprano.

---

## ⚡ INTERVALOS DE CHECK ACTUALIZADOS

### Antes (v1.0)
```
Todos los perfiles: 30 segundos
```

### Ahora (v2.0)
```
VOLUMEN:   10 segundos  ⚡ (checks más frecuentes)
FIBONACCI: 15 segundos  ⚡ (balance velocidad/calidad)
```

**Beneficios:**
- VOLUMEN detecta cambios más rápido (temporalidad 1M)
- FIBO tiene más calidad en cada observación
- Mejor uso de recursos API

---

## 📊 NUEVOS ESTADOS

### Estados Eliminados
- ❌ `LONG_AHORA` (reemplazado por ALTA_PRIORIDAD)
- ❌ `SHORT_AHORA` (reemplazado por ALTA_PRIORIDAD)
- ❌ `DESCARTADO` (reemplazado por RUIDO/INTERESANTE/FUERTE según score)

### Estados Nuevos
```python
EN_ANALISIS           # 🔄 Evaluación en curso
ALTA_PRIORIDAD        # 🚀 Score >= 75
FUERTE                # 💪 Score 60-74
INTERESANTE           # 👀 Score 50-59
RUIDO                 # 📉 Score < 50
ENTRADA_EXPIRADA      # ⏰ Precio se alejó > 3%
INVALIDADA            # ❌ Invalidación extrema detectada
```

---

## 📈 TRACKING MEJORADO

### Nuevos Campos en TrackedEvent

```python
score_maximo: float            # Score máximo alcanzado durante observación
tendencia: str                 # "MEJORANDO" / "ESTABLE" / "DETERIORÁNDOSE"
entry_price: float            # Precio de entrada sugerido
current_price: float          # Precio actual
distance_to_entry: float      # Distancia % al precio de entrada
check_interval: int           # Intervalo dinámico (10 o 15 seg)
```

### Cálculos Automáticos

**Tendencia:**
- MEJORANDO: +2 pts/check o más
- DETERIORÁNDOSE: -2 pts/check o menos
- ESTABLE: Entre -2 y +2 pts/check

**Distancia a Entrada:**
- Calcula % de alejamiento del precio de entrada
- Si > 3%: Estado ENTRADA_EXPIRADA
- Para SHORT: Se invierte el signo (subida = alejamiento)

---

## 🎯 LÓGICA DE DECISIÓN ACTUALIZADA

### Nueva Lógica Unificada

```python
# 1. VERIFICAR ENTRADA EXPIRADA
if abs(distance_to_entry) > 3.0:
    → ENTRADA_EXPIRADA

# 2. VERIFICAR ALTA PRIORIDAD (umbral 75)
if score >= 75:
    → ALTA_PRIORIDAD

# 3. PROTECCIÓN TIEMPO MÍNIMO
if tiempo < tiempo_minimo:
    → Continuar EN_ANALISIS

# 4. DESPUÉS DEL TIEMPO MÍNIMO: Clasificar
if score >= 60 and tendencia >= -1:
    → FUERTE
elif 50 <= score < 60:
    → INTERESANTE
elif score < 50:
    → RUIDO

# 5. INVALIDACIÓN EXTREMA (solo FIBO)
if origen != VOLUMEN and invalidacion_extrema:
    → INVALIDADA
```

---

## ⏱️ TIEMPOS DE OBSERVACIÓN (SIN CAMBIOS)

### VOLUMEN (1M)
```
Score < 50:
  - Checks: 1 (10seg total)
  - Clasificar como RUIDO inmediatamente

Score 50-59:
  - Mínimo: 2 min (120seg)
  - Máximo: 5 min (300seg)
  - Checks: 30

Score >= 60:
  - Mínimo: 2 min (120seg)
  - Máximo: 20 min (1200seg)
  - Checks: 120
```

### FIBO_1H
```
Score < 60:
  - Mínimo: 2.5 min (150seg)
  - Máximo: 5 min (300seg)
  - Checks: 20

Score >= 60:
  - Mínimo: 5 min (300seg)
  - Máximo: 20 min (1200seg)
  - Checks: 80
```

### FIBO_4H
```
Score < 60:
  - Mínimo: 4 min (240seg)
  - Máximo: 7 min (420seg)
  - Checks: 28

Score >= 60:
  - Mínimo: 7 min (420seg)
  - Máximo: 20 min (1200seg)
  - Checks: 80
```

### FIBO_1D
```
Score < 60:
  - Mínimo: 5 min (300seg)
  - Máximo: 10 min (600seg)
  - Checks: 40

Score >= 60:
  - Mínimo: 10 min (600seg)
  - Máximo: 20 min (1200seg)
  - Checks: 80
```

---

## 📱 MENSAJE ACTUALIZADO

### Formato Telegram (v2.0)

```markdown
🚀🚀🚀 **ALTA PRIORIDAD** 🚀🚀🚀

**Origen:** Grupo Ejemplo

━━━━━━━━━━━━━━━━━━━━━━
📊 **BTCUSDT** 🟢 LONG
⏱️ Timeframe: FIBO_4H
✅ Vigencia: VIGENTE
━━━━━━━━━━━━━━━━━━━━━━

🟢 **SCORE: 76.5/100**
**ALTA PRIORIDAD**

━━━━━━━━━━━━━━━━━━━━━━
⏱️ **SEGUIMIENTO EN TIEMPO REAL**
📈 FIBO_4H
━━━━━━━━━━━━━━━━━━━━━━

⏱️ Tiempo: 450s / 1200s
🔍 Checks: 30/80
⚡ Intervalo: 15seg
✅ Decisión tomada: 🚀 ALTA PRIORIDAD

📊 **SCORES:**
• Inicial: 62.0
• Actual: 76.5
• Máximo: 78.2
• Promedio: 70.3
📈 Tendencia: MEJORANDO (+1.5 pts/check)

📈 **EVOLUCIÓN:**
62 → 65 → 70 → 74 → 77

💰 **PRECIO:**
• Entrada: $45000.00
• Actual: $45120.00
• Distancia: +0.27%

━━━━━━━━━━━━━━━━━━━━━━
**📊 MÉTRICAS:**
[... métricas detalladas ...]

━━━━━━━━━━━━━━━━━━━━━━
**⭐ TOP 3 FACTORES:**
1. CVD: Absorción confirmada (19.2 pts)
2. OI: Incremento sostenido (18.5 pts)
3. Sweeps: Barrido 4H detectado (12.0 pts)

⏰ 14:32:18

_Motor de Clasificación v2.0 (Umbral: 75)_
```

---

## 🔧 CAMBIOS TÉCNICOS

### Archivos Modificados

1. **`src/tracking/event_tracker.py`**
   - ✅ Actualizado `EventStatus` enum
   - ✅ Agregados campos a `TrackedEvent`
   - ✅ Intervalos dinámicos (10/15 seg)
   - ✅ Nueva lógica de decisión (umbral 75)
   - ✅ Cálculo de distancia a entrada
   - ✅ Tracking de score máximo y tendencia
   - ✅ Eliminado `check_interval` global
   - ✅ Agregado `check_interval` por evento

2. **`monitor_grupos.py`**
   - ✅ Extracción de precio de entrada
   - ✅ Actualizado `formatear_resumen_telegram()`
   - ✅ Nuevos emojis por estado
   - ✅ Mensajes actualizados con intervalos dinámicos
   - ✅ Versión del motor: v2.0

### Métodos Nuevos

```python
EventTracker._clasificar_por_score(score)
  → Clasifica score en RUIDO/INTERESANTE/FUERTE/ALTA_PRIORIDAD

EventTracker._calcular_distancia_entrada(entry, current, bias)
  → Calcula % de distancia (invierte para SHORT)
```

---

## ✅ REGLAS PRESERVADAS

### No Cambiaron:
- ✅ Separación FIBO vs VOLUMEN (100% independientes)
- ✅ Pesos de métricas por perfil
- ✅ Protección contra descarte prematuro
- ✅ Tiempos mínimos y máximos por origen
- ✅ Invalidación extrema (solo FIBO)
- ✅ Observación extendida (score >= 60 → 20 min)
- ✅ Métricas específicas por perfil

---

## 🎯 BENEFICIOS

### 1. Más Ágil
- Checks más frecuentes (10/15 seg vs 30 seg)
- Detección más rápida de cambios

### 2. Más Simple
- Umbral unificado (75 para ambos)
- Estados más claros (RUIDO/INTERESANTE/FUERTE)
- Menos casos especiales

### 3. Más Información
- Score máximo tracked
- Tendencia calculada automáticamente
- Distancia a entrada monitoreada
- Detección de entrada expirada

### 4. Mejor UX
- Estados más descriptivos
- Mensajes más informativos
- Claridad sobre el progreso

---

## 📊 EJEMPLOS DE CLASIFICACIÓN

### Ejemplo 1: ALTA PRIORIDAD Rápida
```
Score inicial: 72
Check 1 (10seg): 74
Check 2 (10seg): 76  → ALTA_PRIORIDAD ✅
Tiempo total: 20 segundos
```

### Ejemplo 2: FUERTE sin alcanzar
```
Score inicial: 68
Checks: 68 → 70 → 71 → 72 → 73
Score final: 73 (después de 7 min)
Resultado: FUERTE 💪
```

### Ejemplo 3: INTERESANTE
```
Score inicial: 52
Checks: 52 → 54 → 55 → 56 → 55
Score final: 55 (después de 5 min)
Resultado: INTERESANTE 👀
```

### Ejemplo 4: RUIDO
```
Score inicial: 45
Check 1: 45  → RUIDO 📉
Tiempo total: 10 segundos
```

### Ejemplo 5: ENTRADA EXPIRADA
```
Score inicial: 65
Entry: $45000
Check 1: precio $45100 (+0.22%)
Check 2: precio $45300 (+0.67%)
Check 3: precio $46500 (+3.33%)  → ENTRADA_EXPIRADA ⏰
```

---

## 🚀 PRÓXIMOS PASOS

### Monitoreo
- Validar que intervalos dinámicos funcionan correctamente
- Verificar que umbral 75 captura buenas oportunidades
- Confirmar que distancia a entrada detecta expiraciones

### Ajustes Potenciales
- Afinar umbral de distancia (actualmente 3%)
- Ajustar criterios de tendencia (actualmente ±2 pts/check)
- Revisar tiempos si es necesario

---

## 📝 NOTAS TÉCNICAS

### Compatibilidad
- ✅ Compatible con perfiles FIBO y VOLUMEN
- ✅ No rompe funcionalidad existente
- ✅ Mantiene separación estricta de perfiles

### Performance
- 🟢 Checks más frecuentes pero más eficientes
- 🟢 Mejor uso de API (intervalos optimizados)
- 🟢 Menos eventos en seguimiento (clasificación más rápida)

### Testing
- 📝 Probar con señales VOLUMEN
- 📝 Probar con señales FIBO (1H/4H/1D)
- 📝 Validar detección de entrada expirada
- 📝 Confirmar mensajes Telegram correctos

---

**Status:** ✅ IMPLEMENTADO Y LISTO PARA PRUEBAS  
**Versión Motor:** v2.0  
**Umbral Unificado:** 75 (ambos perfiles)  
**Intervalos:** 10seg (VOLUMEN), 15seg (FIBO)

