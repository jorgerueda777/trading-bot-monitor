# 📊 ESCALA DE PRIORIDADES - Motor v2.0

**Versión:** 2.0  
**Última actualización:** 2026-06-08  
**Umbral unificado:** 75 (FIBO y VOLUMEN)

---

## 🎯 NUEVA ESCALA (Motor v2.0)

### 🚀 ALTA PRIORIDAD
```
Score: >= 75/100
Estado: EJECUTAR
Emoji: 🚀🚀🚀
Color: 🟢 Verde
```

**Significado:**
- Señal de muy alta calidad
- Todas las métricas principales confirmando
- Confluencia fuerte de factores
- **ACCIÓN:** Ejecutar operación

**Características:**
- OI confirmando dirección
- CVD sin divergencias
- Delta agresivo en dirección correcta
- Múltiples factores alineados

**Ejemplo:**
```
BTCUSDT LONG
Score: 78/100 🚀 ALTA PRIORIDAD
- OI: 85/100 (incrementando fuerte)
- CVD: 82/100 (absorción confirmada)
- Delta: 78/100 (compras agresivas)
```

---

### 💪 FUERTE
```
Score: 60-74/100
Estado: OBSERVAR CON INTERÉS
Emoji: 💪💪
Color: 🟡 Amarillo
```

**Significado:**
- Señal de buena calidad
- Mayoría de métricas positivas
- Puede desarrollarse hacia ALTA PRIORIDAD
- **ACCIÓN:** Seguir monitoreando, puede activarse

**Características:**
- Buen setup pero le falta confirmación final
- 2-3 métricas principales confirmando
- Potencial de mejora durante observación
- Puede alcanzar 75+ en minutos

**Ejemplo:**
```
ETHUSDT SHORT
Score: 68/100 💪 FUERTE
- OI: 75/100 (disminuyendo)
- CVD: 65/100 (leve deterioro)
- Delta: 60/100 (ventas incrementando)

Tendencia: MEJORANDO (+2 pts/check)
→ Puede alcanzar ALTA PRIORIDAD
```

---

### 👀 INTERESANTE
```
Score: 50-59/100
Estado: MONITOREAR
Emoji: 👀
Color: 🟡 Amarillo
```

**Significado:**
- Señal con mérito pero no convincente
- Algunos factores positivos
- Mayoría de métricas neutras
- **ACCIÓN:** Monitorear, probabilidad baja

**Características:**
- Setup incompleto
- Faltan confirmaciones clave
- Puede ser solo ruido de mercado
- Baja probabilidad de activación

**Ejemplo:**
```
SOLUSDT LONG
Score: 54/100 👀 INTERESANTE
- OI: 55/100 (neutral)
- CVD: 50/100 (sin tendencia clara)
- Delta: 48/100 (indeciso)

Tendencia: ESTABLE
→ Probabilidad baja de activación
```

---

### 📉 RUIDO
```
Score: < 50/100
Estado: DESCARTAR
Emoji: 📉
Color: 🔴 Rojo
```

**Significado:**
- Señal de baja calidad
- Métricas no confirman
- Falso positivo probable
- **ACCIÓN:** Ignorar completamente

**Características:**
- Setup no válido
- Métricas contradictorias
- Sin confluencia
- Alta probabilidad de falso positivo

**Ejemplo:**
```
DOGEUSDT SHORT
Score: 42/100 📉 RUIDO
- OI: 35/100 (incrementando - contrario)
- CVD: 40/100 (compras dominando)
- Delta: 38/100 (presión compradora)

→ Señal descartada
```

---

## 📈 COMPARACIÓN: Escala Anterior vs Nueva

### Escala Anterior (Motor v1.0)
```
ALTA PRIORIDAD:    >= 85 (VOLUMEN) / >= 80 (FIBO)
PRIORIDAD MEDIA:   60-84 / 60-79
BAJA PRIORIDAD:    < 60
```

### Escala Nueva (Motor v2.0)
```
🚀 ALTA PRIORIDAD:  >= 75  (unificado)
💪 FUERTE:          60-74
👀 INTERESANTE:     50-59
📉 RUIDO:           < 50
```

### Cambios Clave

| Aspecto | Antes | Ahora |
|---------|-------|-------|
| **Umbral ALTA** | 85/80 | 75 (unificado) |
| **Estados** | 3 niveles | 4 niveles |
| **Claridad** | Ambiguo | Descriptivo |
| **VOLUMEN** | 85 | 75 |
| **FIBO** | 80 | 75 |

---

## 🎯 DISTRIBUCIÓN ESPERADA

En condiciones normales de mercado:

```
🚀 ALTA PRIORIDAD:  5-10%   (señales ejecutables)
💪 FUERTE:          15-20%  (seguimiento cercano)
👀 INTERESANTE:     25-30%  (monitoreo ligero)
📉 RUIDO:           40-55%  (descartadas)
```

**Objetivo:** El sistema debe ser selectivo. La mayoría de señales serán RUIDO o INTERESANTE.

---

## 🔄 EVOLUCIÓN DURANTE OBSERVACIÓN

Una señal puede cambiar de prioridad:

### Ejemplo: De FUERTE a ALTA PRIORIDAD ✅
```
Check 0 (inicial):
  Score: 68/100 💪 FUERTE
  OI: 70, CVD: 65, Delta: 60

Check 3 (+45 seg):
  Score: 72/100 💪 FUERTE
  Tendencia: MEJORANDO

Check 5 (+75 seg):
  Score: 77/100 🚀 ALTA PRIORIDAD
  ✅ ACTIVAR OPERACIÓN
```

### Ejemplo: De INTERESANTE a RUIDO ❌
```
Check 0 (inicial):
  Score: 55/100 👀 INTERESANTE
  OI: 55, CVD: 52, Delta: 48

Check 2 (+30 seg):
  Score: 51/100 👀 INTERESANTE
  Tendencia: DETERIORÁNDOSE

Check 4 (+60 seg):
  Score: 46/100 📉 RUIDO
  ❌ DESCARTADA
```

---

## 📊 CRITERIOS POR PERFIL

### VOLUMEN (1M)
```
🚀 >= 75:  Alta presión + confluencia
💪 60-74:  Presión visible + 2-3 factores
👀 50-59:  Señal débil + factores neutros
📉 < 50:   Sin presión o contraria
```

**Métricas clave:**
1. OI (25%)
2. CVD (25%)
3. Delta (20%)

### FIBONACCI (1H/4H/1D)
```
🚀 >= 75:  Zona validada + múltiples confirmaciones
💪 60-74:  Zona con interés + algunas confirmaciones
👀 50-59:  Zona tocada + reacción débil
📉 < 50:   Zona sin interés
```

**Métricas clave:**
1. OI (25%)
2. CVD (25/20/15%)
3. Sweeps (10/15/25%)

---

## 🎬 CASOS DE USO

### Trader Agresivo
```
Actúa en: 🚀 ALTA PRIORIDAD (>=75)
Monitorea: 💪 FUERTE (60-74)
Ignora: 👀 INTERESANTE, 📉 RUIDO
```

### Trader Conservador
```
Actúa en: 🚀 ALTA PRIORIDAD (>=80)
Monitorea: 🚀 ALTA PRIORIDAD (75-80)
Ignora: 💪 FUERTE y menores
```

### Trader Oportunista
```
Actúa en: 🚀 ALTA PRIORIDAD + 💪 FUERTE con tendencia MEJORANDO
Monitorea: Todo >= 50
Ignora: 📉 RUIDO
```

---

## ✅ VENTAJAS DE LA NUEVA ESCALA

### 1. Más Granular
- 4 niveles vs 3 anteriores
- Mejor diferenciación de calidad

### 2. Más Clara
- Nombres descriptivos (FUERTE vs MEDIA)
- Emojis visuales
- Significado obvio

### 3. Más Oportuna
- Umbral 75 vs 80/85
- Captura más oportunidades válidas
- Sin sacrificar calidad

### 4. Unificada
- Mismo umbral FIBO y VOLUMEN
- Menos complejidad
- Más consistente

---

## 🔧 IMPLEMENTACIÓN TÉCNICA

```python
class PriorityLevel:
    ALTA = "🚀 ALTA PRIORIDAD"
    FUERTE = "💪 FUERTE"
    INTERESANTE = "👀 INTERESANTE"
    RUIDO = "📉 RUIDO"
    
    @staticmethod
    def from_score(score: float) -> str:
        if score >= 75:
            return PriorityLevel.ALTA
        elif score >= 60:
            return PriorityLevel.FUERTE
        elif score >= 50:
            return PriorityLevel.INTERESANTE
        else:
            return PriorityLevel.RUIDO
```

---

## 📝 NOTAS IMPORTANTES

1. **Score es dinámico:** Puede cambiar durante observación
2. **Tendencia importa:** FUERTE con tendencia MEJORANDO puede llegar a ALTA
3. **Contexto cuenta:** Una señal FUERTE en mercado fuerte > INTERESANTE en mercado débil
4. **No todas las ALTA se ejecutan:** Puede expirar entrada antes de activación
5. **RUIDO es normal:** 40-50% de señales son ruido, esto es esperado

---

**Status:** ✅ IMPLEMENTADO  
**Versión:** Motor v2.0  
**Fecha:** 2026-06-08  
**Umbral unificado:** 75 para ambos perfiles
