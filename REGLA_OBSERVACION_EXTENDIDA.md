# 📋 REGLA DE OBSERVACIÓN EXTENDIDA

**Fecha:** 2026-06-07  
**Versión:** 1.0

---

## 🎯 OBJETIVO

Dar una oportunidad completa de desarrollo a todas las señales que demuestran calidad inicial suficiente.

---

## ⚖️ UMBRAL DE CALIDAD

Una señal que obtenga una puntuación inicial igual o superior a:

```
Score >= 60/100
```

Ha demostrado suficiente calidad para continuar siendo observada.

**Por lo tanto:**
- ❌ NO debe descartarse únicamente por falta de movimiento inicial
- ✅ Debe recibir observación extendida obligatoria

---

## ⏱️ OBSERVACIÓN EXTENDIDA

### Activación Automática

Si `Score Inicial >= 60`:

```
✅ OBSERVACIÓN EXTENDIDA ACTIVADA

Duración máxima: 20 minutos
Checks: 40 (cada 30 segundos)
```

### Durante Este Período

Actualizar continuamente según el perfil:

**VOLUMEN:**
- Open Interest
- CVD
- Delta
- Order Book
- Liquidity Sweeps
- Momentum Decay
- Funding
- VWAP

**FIBONACCI:**
- Open Interest
- CVD
- Delta
- Volume
- Liquidity Sweeps
- Funding
- VWAP

---

## 🎯 TIEMPOS POR PERFIL

### VOLUMEN (Score >= 60)
```
Tiempo mínimo: 2 minutos
Tiempo máximo: 20 minutos
Checks: 40
```

### FIBO_1H (Score >= 60)
```
Tiempo mínimo: 5 minutos
Tiempo máximo: 20 minutos
Checks: 40
```

### FIBO_4H (Score >= 60)
```
Tiempo mínimo: 7 minutos
Tiempo máximo: 20 minutos
Checks: 40
```

### FIBO_1D (Score >= 60)
```
Tiempo mínimo: 10 minutos
Tiempo máximo: 20 minutos
Checks: 40
```

---

## 🚀 ACTIVACIÓN ANTICIPADA

Durante la observación, si el score alcanza el **umbral de ALTA PRIORIDAD**:

### VOLUMEN
```
Score >= 85
→ ALTA PRIORIDAD (LONG AHORA / SHORT AHORA)
```

### FIBONACCI
```
Score >= 80
→ ALTA PRIORIDAD (LONG AHORA / SHORT AHORA)
```

**No es necesario esperar los 20 minutos completos.**

---

## 🏁 FINALIZACIÓN DE OBSERVACIÓN

La observación termina cuando ocurre **cualquiera** de estas condiciones:

### 1. Alta Prioridad Alcanzada
```
Score >= Umbral del perfil
→ Clasificar y notificar inmediatamente
```

### 2. Invalidación Clara
```
Evidencias negativas extremas detectadas
→ Descartar
```

### 3. Tiempo Máximo Completado
```
20 minutos transcurridos sin alcanzar umbral
→ Evaluar estado final
```

---

## ⚠️ INVALIDACIÓN TEMPRANA

Solo permitir descarte anticipado (antes del tiempo mínimo) cuando existan **evidencias claramente negativas**.

### Ejemplos de Invalidación Extrema:

#### Para AMBOS Perfiles:
- ❌ Colapso del Open Interest (score < 20)
- ❌ Deterioro fuerte del CVD (score < 20)
- ❌ Delta completamente contrario (score < 15)
- ❌ Sweep contrario relevante
- ❌ Pérdida de vigencia de la entrada
- ❌ Precio se aleja significativamente de la zona válida
- ❌ Caída de score extrema (>30 puntos)
- ❌ Score cae por debajo de 40

### ✅ NO es Invalidación:
- ✅ Ausencia de movimiento inicial
- ✅ Falta de reacción en primeros minutos
- ✅ Precio consolidando en la zona
- ✅ Métricas estables sin mejorar

**La ausencia de movimiento por sí sola NO constituye una invalidación.**

---

## 📊 TABLA COMPARATIVA

| Aspecto | Score < 60 | Score >= 60 |
|---------|------------|-------------|
| **Tiempo máximo VOLUMEN** | 5 minutos | 20 minutos |
| **Tiempo máximo FIBO_1H** | 5 minutos | 20 minutos |
| **Tiempo máximo FIBO_4H** | 7 minutos | 20 minutos |
| **Tiempo máximo FIBO_1D** | 10 minutos | 20 minutos |
| **Observación extendida** | ❌ No | ✅ Sí |
| **Protección descarte** | Estándar | Reforzada |
| **Checks máximos** | 10-20 | 40 |

---

## 🎯 REGLA FINAL

**Toda señal con score inicial >= 60 debe recibir una oportunidad completa de desarrollo.**

### Principios:

1. **Calidad sobre Velocidad**
   - Priorizar la calidad de la evaluación
   - No apresurarse a descartar señales válidas

2. **Desarrollo Gradual**
   - Las señales válidas pueden necesitar varios minutos
   - Especialmente en temporalidades superiores (FIBO)

3. **Observación Completa**
   - Hasta 20 minutos es obligatorio para score >= 60
   - Permite captar oportunidades que se desarrollan lentamente

4. **Activación Flexible**
   - Si alcanza umbral antes de 20 min → Activar inmediatamente
   - Si no alcanza umbral en 20 min → Evaluar estado final

---

## 📱 EJEMPLO DE LOG

```
🔄 Evento agregado al seguimiento (ID: BTCUSDT_1780880928)
   📈 Tipo: FIBO_4H
   ⏱️ OBSERVACIÓN EXTENDIDA: hasta 20 minutos (mínimo: 7 min)
   🔄 Actualización cada 30seg
   ⭐ Score >= 60: Observación extendida activa
   🛡️ Protección contra descarte prematuro activa

⏰ Check de monitoreo - Eventos activos: 1
   📊 BTCUSDT: Score=63.5, Estado=🔄 EN ANÁLISIS, Check 5/40
      📈 Nuevo score: 63.5 (inicial: 62.0)
      📊 Tendencia: +0.3 pts/check, Promedio: 62.8
      🔹 Evaluando con reglas FIBO (umbral: 80)
      ⏳ Aún en tiempo mínimo (150s / 420s)

[... 15 minutos después ...]

⏰ Check de monitoreo - Eventos activos: 1
   📊 BTCUSDT: Score=81.2, Estado=🔄 EN ANÁLISIS, Check 30/40
      📈 Nuevo score: 81.2 (inicial: 62.0)
      📊 Tendencia: +1.2 pts/check, Promedio: 72.5
      🔹 Evaluando con reglas FIBO (umbral: 80)
      ✅ Score >= 80 o confirmación progresiva → ALTA PRIORIDAD

✅ Evento BTCUSDT_1780880928 finalizó: 🟢 LONG AHORA
   🔔 Ejecutando callback...
```

---

## ✅ BENEFICIOS

1. **Menos Falsos Negativos**
   - Señales válidas que se desarrollan lentamente no se pierden

2. **Mejor Aprovechamiento**
   - Score >= 60 indica calidad suficiente para vigilancia extendida

3. **Flexibilidad Temporal**
   - Diferentes perfiles mantienen sus tiempos mínimos
   - Pero todos comparten el máximo de 20 minutos

4. **Activación Oportunista**
   - Si mejora rápido → Activa antes
   - Si mejora lento → Tiempo completo para desarrollarse

---

**Status:** ✅ IMPLEMENTADO  
**Aplicable a:** TODOS los perfiles (VOLUMEN y FIBONACCI)  
**Umbral de activación:** Score >= 60

