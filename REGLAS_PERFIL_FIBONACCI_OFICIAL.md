# 📋 REGLAS OFICIALES DEL PERFIL FIBONACCI

**Última actualización:** 2026-06-07  
**Versión:** 2.0 (Actualización Obligatoria)

---

## 🎯 NATURALEZA DEL PERFIL FIBONACCI

### ⚠️ REGLA CRÍTICA
Las señales FIBONACCI **NO son señales de temporalidad 1 minuto**.

### Características
- Representan **zonas de reacción**
- Derivadas de **temporalidades superiores**
- Requieren **tiempo para desarrollarse**

### El mercado necesita tiempo para:
- ✅ Absorber órdenes
- ✅ Acumular liquidez
- ✅ Mostrar intención
- ✅ Desarrollar una reacción válida

---

## 🛡️ PROHIBICIÓN DE DESCARTE PREMATURO

### ❌ PROHIBIDO descartar una señal FIBONACCI porque:
- ❌ No hubo movimiento en 30 segundos
- ❌ No hubo movimiento en 60 segundos
- ❌ No hubo movimiento en 90 segundos

### ✅ La ausencia de reacción inmediata NO invalida una señal FIBONACCI

---

## ⏰ NUEVA LÓGICA DE OBSERVACIÓN

### FIBO 1H

#### Si Score Inicial ≥ 60:
```
Observación obligatoria activada
Duración mínima: 5 minutos
Duración máxima: 10 minutos
Checks: 20 (cada 30seg)
```

#### Si Score Inicial < 60:
```
Observación reducida pero generosa
Duración mínima: 2.5 minutos
Duración máxima: 5 minutos
Checks: 10 (cada 30seg)
```

### FIBO 4H

#### Si Score Inicial ≥ 60:
```
Observación obligatoria activada
Duración mínima: 7 minutos
Duración máxima: 15 minutos
Checks: 30 (cada 30seg)
```

#### Si Score Inicial < 60:
```
Observación reducida pero generosa
Duración mínima: 4 minutos
Duración máxima: 7 minutos
Checks: 14 (cada 30seg)
```

### FIBO 1D

#### Si Score Inicial ≥ 60:
```
Observación obligatoria activada
Duración mínima: 10 minutos
Duración máxima: 20 minutos
Checks: 40 (cada 30seg)
```

#### Si Score Inicial < 60:
```
Observación reducida pero generosa
Duración mínima: 5 minutos
Duración máxima: 10 minutos
Checks: 20 (cada 30seg)
```

---

## 🔄 DURANTE LA OBSERVACIÓN

### Actualizar continuamente:
- ✅ Open Interest
- ✅ CVD
- ✅ Delta
- ✅ Volume
- ✅ Funding
- ✅ Liquidity Sweeps
- ✅ VWAP

### No descartar antes del tiempo mínimo obligatorio
**EXCEPTO:** Si aparece invalidación extrema

---

## ⚠️ INVALIDACIÓN EXTREMA

Solo se permite finalizar anticipadamente una observación si aparecen **evidencias claramente negativas**.

### Ejemplos de Invalidación Extrema:

#### 1. Open Interest colapsa
```
Score OI < 20
```

#### 2. CVD se deteriora fuertemente
```
Score CVD < 20
```

#### 3. Delta completamente contrario
```
Score Delta < 15
```

#### 4. Caída de score extrema
```
Score inicial - Score actual > 30 puntos
```

#### 5. Score muy bajo
```
Score actual < 40
```

### ✅ Si NO hay invalidación extrema:
**Respetar el tiempo mínimo obligatorio**

---

## 🎯 OBJETIVO DEL MODO OBSERVACIÓN

### ❌ El objetivo NO es:
- ❌ Buscar una reacción instantánea
- ❌ Esperar movimiento en segundos
- ❌ Aplicar lógica de scalping

### ✅ El objetivo SÍ es:
- ✅ Determinar si la zona FIBO atrae interés real del mercado
- ✅ Buscar: Absorción, Acumulación, Distribución
- ✅ Detectar: Divergencias, Cambio progresivo de flujo
- ✅ Observar: Desarrollo gradual de la reacción

---

## 📊 SISTEMA DE PUNTUACIÓN

### Pesos por Perfil

#### FIBO_1H
| Métrica | Peso |
|---------|------|
| Open Interest | 25% |
| CVD | 25% |
| Delta | 20% |
| Volume | 15% |
| Liquidity Sweeps | 10% |
| Funding | 3% |
| VWAP | 2% |

#### FIBO_4H
| Métrica | Peso |
|---------|------|
| Open Interest | 25% |
| CVD | 20% |
| Delta | 15% |
| Volume | 15% |
| Liquidity Sweeps | 15% |
| Funding | 5% |
| VWAP | 5% |

#### FIBO_1D
| Métrica | Peso |
|---------|------|
| Open Interest | 20% |
| CVD | 15% |
| Delta | 10% |
| Volume | 15% |
| Liquidity Sweeps | 25% |
| Funding | 10% |
| VWAP | 5% |

### Umbral de Alta Prioridad
```
Score ≥ 80/100
```

**⚠️ IMPORTANTE:** Este umbral es DIFERENTE al de VOLUMEN (85)

**Razón:** Las señales FIBONACCI provienen de temporalidades superiores y necesitan más flexibilidad para desarrollarse.

### Umbral de Descarte (después del tiempo mínimo)
```
Score < 60/100
```

---

## 🔄 REGLA DE RECLASIFICACIÓN

### Durante la observación:

#### Si Score ≥ 80:
```
Acción: Clasificar como ALTA PRIORIDAD
Estado: LONG AHORA / SHORT AHORA
```

**Observación continúa:** Incluso con score ≥80, mantener observación activa durante el tiempo mínimo para confirmar desarrollo.

#### Si Score < 60 (después del tiempo mínimo):
```
Acción: Clasificar como BAJA PRIORIDAD
Estado: DESCARTADO
```

#### Si 60 ≤ Score < 80:
```
Acción: Mantener PRIORIDAD MEDIA
Estado: EN ANÁLISIS
```

### El score debe ser dinámico durante todo el período de observación

---

## 📈 COMPARACIÓN CON VOLUMEN

| Aspecto | FIBONACCI | VOLUMEN |
|---------|-----------|---------|
| **Temporalidad** | 1H/4H/1D | 1M |
| **Tiempo mín (FIBO_1H)** | 5 minutos | 2-3 minutos |
| **Tiempo mín (FIBO_4H)** | 7 minutos | N/A |
| **Tiempo mín (FIBO_1D)** | 10 minutos | N/A |
| **Tiempo máx (FIBO_1H)** | 10 minutos | 5 minutos |
| **Tiempo máx (FIBO_4H)** | 15 minutos | N/A |
| **Tiempo máx (FIBO_1D)** | 20 minutos | N/A |
| **Umbral ALTA** | 85 | 80 |
| **Umbral Descarte** | 60 | 50 |
| **Métricas** | OI, CVD, Delta, Volume, Sweeps, Funding, VWAP | OI, CVD, Delta, OrderBook, Sweeps, Momentum, Funding, VWAP |

---

## 📱 FORMATO DE SALIDA

```
━━━━━━━━━━━━━━━━━━━━━━
📈 EVALUACIÓN FIBONACCI
━━━━━━━━━━━━━━━━━━━━━━

Símbolo: BTCUSDT
Dirección: 🟢 LONG
Timeframe: FIBO 4H
Zona: 45000-45200

━━━━━━━━━━━━━━━━━━━━━━
⏱️ OBSERVACIÓN EN CURSO

Tiempo: 4:30 / 15:00 min
Checks: 9/30
Próximo: 15seg

━━━━━━━━━━━━━━━━━━━━━━
📊 MÉTRICAS:

• OI: 75/100
  OI estable con ligero aumento

• CVD: 70/100
  CVD mostrando absorción gradual

• Delta: 68/100
  Compras pasivas incrementando

• Volume: 65/100
  Volumen por encima del promedio

• Sweeps: 80/100
  Barrido de mínimo 4H detectado

• Funding: 60/100
  FR neutral

• VWAP: 55/100
  Precio cerca del VWAP

━━━━━━━━━━━━━━━━━━━━━━
🎯 PUNTUACIÓN: 72/100
🟡 PRIORIDAD MEDIA

Evolución: 68 → 70 → 72 📈
Tendencia: +2.0 pts/check

━━━━━━━━━━━━━━━━━━━━━━
📝 OBSERVACIÓN:

La zona FIBO está mostrando:
✅ Acumulación gradual de liquidez
✅ Absorción de ventas
🔄 Aún desarrollando reacción

Tiempo mínimo: 7 minutos
Tiempo restante: 2:30 minutos

⏰ Evaluado: 14:45:30
```

---

## ✅ CHECKLIST DE CUMPLIMIENTO

- [x] Tiempos mínimos implementados (5/7/10 min)
- [x] Tiempos máximos implementados (10/15/20 min)
- [x] Protección contra descarte prematuro
- [x] Invalidación extrema definida
- [x] Umbral ALTA PRIORIDAD = 85
- [x] Umbral descarte FIBO = 60
- [x] Separación total de VOLUMEN
- [x] NO aplicar lógica de scalping (1M)
- [x] Permitir desarrollo gradual de reacción
- [x] Actualización cada 30 segundos
- [x] Reclasificación dinámica
- [x] Métricas específicas FIBO

---

## 🚀 ESTADO

✅ **PERFIL FIBONACCI:** Actualizado con tiempos amplios  
✅ **PROTECCIÓN:** Contra descarte prematuro implementada  
✅ **TIEMPOS:** 5-20 minutos según origen  
✅ **INVALIDACIÓN:** Solo por evidencias extremas  
✅ **SISTEMA:** Listo para producción

---

**Versión:** 2.0  
**Fecha:** 2026-06-07  
**Status:** PRODUCCIÓN READY ✅
