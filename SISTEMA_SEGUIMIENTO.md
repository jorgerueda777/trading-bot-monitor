# 🔄 SISTEMA DE SEGUIMIENTO DE EVENTOS

## Descripción

El sistema NO ejecuta operaciones inmediatamente. Cada evento detectado entra en un período de **ANÁLISIS de 2-5 minutos**, durante el cual se monitorea cada **30 segundos** para decidir si debe ejecutarse o descartarse.

---

## 🎯 Estados del Evento

### 1. 🔄 EN ANÁLISIS
- Estado inicial de todos los eventos
- Se monitorea cada 30 segundos
- Duración: 2-5 minutos (dependiendo del score inicial)
- El sistema reevalúa métricas de mercado en cada check

### 2. 🟢 LONG AHORA / 🔴 SHORT AHORA
- **Condiciones para EJECUTAR:**
  - Score actual ≥ 85 **Y** tendencia positiva/estable
  - **O** Score promedio ≥ 80 **Y** últimos 2-3 checks consistentes ≥ 80
  
- **Qué significa:**
  - Las métricas confirman la oportunidad
  - Es momento de considerar la operación
  - El evento ha sido validado

### 3. ❌ DESCARTADO
- **Condiciones para DESCARTAR:**
  - Score actual < 60
  - **O** Tendencia muy negativa (cayendo > 5 pts por check)
  - **O** Score bajó > 15 puntos desde el inicial
  
- **Qué significa:**
  - Las condiciones se deterioraron
  - El evento perdió validez
  - No cumple los criterios mínimos

---

## ⏱️ Línea de Tiempo

```
t=0s    ┌──────────────────────────────────┐
        │  🔍 EVENTO DETECTADO             │
        │  Score inicial: 82/100           │
        │  Estado: 🔄 EN ANÁLISIS          │
        └──────────────────────────────────┘
                      ↓
t=30s   ┌──────────────────────────────────┐
        │  📊 CHECK #1                     │
        │  Reevaluar métricas              │
        │  Score: 84/100 (↑)               │
        │  Decisión: Seguir analizando     │
        └──────────────────────────────────┘
                      ↓
t=60s   ┌──────────────────────────────────┐
        │  📊 CHECK #2                     │
        │  Score: 86/100 (↑)               │
        │  Tendencia: +2 pts/check         │
        │  Decisión: Seguir analizando     │
        └──────────────────────────────────┘
                      ↓
t=90s   ┌──────────────────────────────────┐
        │  📊 CHECK #3                     │
        │  Score: 87/100 (↑)               │
        │  Score promedio: 85/100          │
        │  ✅ Condición cumplida!          │
        │  Estado: 🟢 LONG AHORA           │
        └──────────────────────────────────┘
```

---

## 📊 Lógica de Decisión

### Factores Evaluados

| Factor | Descripción | Impacto |
|--------|-------------|---------|
| **Score Actual** | Puntuación en el check actual | Alto |
| **Tendencia** | Cambio promedio entre checks | Alto |
| **Consistencia** | Últimos 2-3 checks > 80 | Medio |
| **Score Promedio** | Promedio de todos los checks | Medio |
| **Caída desde inicial** | Diferencia vs score inicial | Medio |

### Algoritmo de Decisión

```python
# EJECUTAR (LONG/SHORT AHORA)
if (score_actual >= 85 AND tendencia >= 0) OR
   (score_promedio >= 80 AND ultimos_checks_consistentes):
    → LONG AHORA / SHORT AHORA

# DESCARTAR
elif (score_actual < 60) OR 
     (tendencia < -5) OR
     (caida_desde_inicial > 15):
    → DESCARTADO

# CONTINUAR
else:
    → EN ANÁLISIS (seguir monitoreando)
```

---

## 🎛️ Configuración Adaptativa

El sistema ajusta el número máximo de checks según el score inicial:

| Score Inicial | Max Checks | Duración Total |
|--------------|------------|----------------|
| ≥ 85 (Alta)  | 4 checks   | 2 minutos      |
| 70-84 (Media)| 6 checks   | 3 minutos      |
| < 70 (Baja)  | 10 checks  | 5 minutos      |

**Razón:** Los eventos con score alto se confirman más rápido. Los eventos con score bajo necesitan más tiempo para demostrar validez.

---

## 📱 Mensaje en Telegram

### Estado Inicial (EN ANÁLISIS)

```
🔄 EN ANÁLISIS 🔄

Origen: Analítica Trading VIP 🤖

━━━━━━━━━━━━━━━━━━━━━━
📊 BTCUSDT
📈 Sesgo: BULLISH
⏱️ Timeframe: FIBO_4H
✅ Estado: VIGENTE
━━━━━━━━━━━━━━━━━━━━━━

🟡 SCORE: 82.0/100
ALTA PRIORIDAD

━━━━━━━━━━━━━━━━━━━━━━
⏱️ SEGUIMIENTO EN TIEMPO REAL
━━━━━━━━━━━━━━━━━━━━━━

⏱️ Tiempo: 0s / 300s
🔍 Checks: 0/6
⏳ Próximo check en 30s

📊 SCORES:
• Inicial: 82.0
• Actual: 82.0
• Promedio: 82.0
➡️ Tendencia: 0.0 pts/check

📈 EVOLUCIÓN:
82

━━━━━━━━━━━━━━━━━━━━━━
... (métricas completas)
```

### Estado Final (EJECUTAR)

```
🚀🚀🚀 LONG AHORA 🚀🚀🚀

Origen: Analítica Trading VIP 🤖

━━━━━━━━━━━━━━━━━━━━━━
📊 BTCUSDT
📈 Sesgo: BULLISH
⏱️ Timeframe: FIBO_4H
✅ Estado: VIGENTE
━━━━━━━━━━━━━━━━━━━━━━

🟢 SCORE: 87.0/100
ALTA PRIORIDAD

━━━━━━━━━━━━━━━━━━━━━━
⏱️ SEGUIMIENTO EN TIEMPO REAL
━━━━━━━━━━━━━━━━━━━━━━

⏱️ Tiempo: 90s / 300s
🔍 Checks: 3/6
✅ Decisión tomada: LONG AHORA

📊 SCORES:
• Inicial: 82.0
• Actual: 87.0
• Promedio: 85.0
📈 Tendencia: +2.5 pts/check

📈 EVOLUCIÓN:
82 → 84 → 86 → 87

━━━━━━━━━━━━━━━━━━━━━━
... (métricas completas)
```

---

## 🔧 Configuración Técnica

### Parámetros Clave

```python
# En src/tracking/event_tracker.py

check_interval = 30  # segundos entre checks
decision_threshold = 85.0  # score mínimo para ejecutar
descarte_threshold = 60.0  # score bajo el cual descartar
max_checks = 4-10  # variable según score inicial
```

### Personalización

Para ajustar el comportamiento, modifica:

```python
@dataclass
class TrackedEvent:
    decision_threshold: float = 85.0  # Más alto = más conservador
    descarte_threshold: float = 60.0   # Más bajo = descartar antes
    max_checks: int = 10               # Más checks = más tiempo
```

---

## 📈 Ventajas del Sistema

1. **Reduce Falsos Positivos:** No actúa en el primer impulso
2. **Confirma Tendencias:** Valida que las condiciones se mantienen
3. **Adaptativo:** Ajusta duración según confianza inicial
4. **Transparente:** Muestra evolución en tiempo real
5. **Reversible:** Puede descartar eventos que se deterioran

---

## 🎯 Casos de Uso

### Caso 1: Confirmación Rápida (IDEAL)
- Score inicial: 82
- Checks: 82 → 85 → 87 → 88
- Resultado: **LONG AHORA** en 90 segundos

### Caso 2: Mejora Gradual
- Score inicial: 75
- Checks: 75 → 76 → 78 → 81 → 83
- Resultado: **LONG AHORA** en 150 segundos

### Caso 3: Deterioro (DESCARTAR)
- Score inicial: 78
- Checks: 78 → 72 → 65 → 58
- Resultado: **DESCARTADO** en 120 segundos

### Caso 4: Indecisión (TIMEOUT)
- Score inicial: 70
- Checks: 70 → 72 → 71 → 73 → 72 → 74...
- Resultado: **DESCARTADO** por timeout (300s)

---

## ⚙️ Integración con Motor de Clasificación

El sistema de seguimiento trabaja con el motor de clasificación:

1. **Parser** extrae evento del mensaje
2. **Validator** verifica vigencia temporal
3. **Classifier** calcula score inicial (0-100)
4. **Tracker** monitorea evolución por 2-5 min
5. **Decision** determina ejecutar o descartar

Cada 30 segundos, el Tracker:
- Obtiene datos actualizados de Binance
- Re-ejecuta el Classifier
- Compara con scores anteriores
- Decide: continuar, ejecutar o descartar

---

## 📝 Notas Importantes

- El sistema **NO ejecuta operaciones automáticamente**
- Solo **clasifica y recomienda** basado en análisis cuantitativo
- La decisión final de operar es siempre del usuario
- Los mensajes en Telegram son **editados en vivo** durante el seguimiento

---

**Sistema implementado según prompt del Motor de Clasificación de Eventos**  
*Versión 1.0 - Junio 2026*
