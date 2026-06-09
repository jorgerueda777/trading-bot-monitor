# 📋 REGLAS OFICIALES DEL PERFIL VOLUMEN

**Última actualización:** 2026-06-07  
**Versión:** 3.0 (Actualización Obligatoria)

---

## 🎯 AISLAMIENTO TOTAL

### ✅ REGLA FUNDAMENTAL
Si `ORIGEN = VOLUMEN`:
- ✅ Usar **EXCLUSIVAMENTE** `PERFIL_VOLUMEN`
- ❌ **IGNORAR** completamente: FIBO_1H, FIBO_4H, FIBO_1D

### ❌ PROHIBIDO MEZCLAR
- ❌ Scores de FIBONACCI
- ❌ Pesos de FIBONACCI
- ❌ Confirmaciones de FIBONACCI
- ❌ Reglas de FIBONACCI
- ❌ Interpretaciones de FIBONACCI

**Cada perfil funciona como un motor 100% independiente.**

---

## ⏱️ NATURALEZA TEMPORAL

### Señales de 1 MINUTO (1M)
Las señales provienen de un detector en temporalidad **1 MINUTO**.

Por lo tanto:
- ❌ NO usar lógica de swing trading
- ❌ NO usar lógica de largo plazo
- ❌ NO esperar confirmaciones de horas
- ❌ NO esperar cierres de velas de: 15m, 30m, 1H, 4H

### Horizonte de Análisis
- **Mínimo:** 1 minuto
- **Máximo:** 7 minutos

### Objetivo
Determinar si existe:
- ✅ Agotamiento inmediato
- ✅ Absorción inmediata
- ✅ Reversión inmediata
- ✅ Continuación inmediata

---

## 🎯 OBJETIVO DEL PERFIL

### La señal original YA detectó:
- SOBRECOMPRA
- o SOBREVENTA

### Por lo tanto, el sistema NO debe:
- ❌ Recalcular sobrecompra
- ❌ Recalcular sobreventa
- ❌ Volver a ejecutar el detector original

### La misión es ÚNICAMENTE:
Responder:
1. ¿La presión actual se está **agotando**?
2. ¿La presión actual sigue **dominante**?

---

## 📊 SISTEMA DE PUNTUACIÓN

### Pesos Oficiales (Total: 100)

| Métrica | Peso | Categoría |
|---------|------|-----------|
| **Open Interest** | 25 | Principal |
| **CVD** | 25 | Principal |
| **Delta** | 20 | Principal |
| **Order Book** | 10 | Principal |
| **Liquidity Sweeps** | 10 | Principal |
| **Momentum Decay** | 5 | Principal |
| **Funding** | 3 | Contexto |
| **VWAP** | 2 | Contexto |

**Total:** 100 puntos

### Factores Principales (Prioridad ALTA)
1. Open Interest (25%)
2. CVD (25%)
3. Delta (20%)
4. Order Book (10%)
5. Liquidity Sweeps (10%)
6. Momentum Decay (5%)

### Factores Secundarios (Solo contexto)
7. Funding (3%)
8. VWAP (2%)

**NUNCA usar Funding o VWAP como factor principal.**

---

## ⏰ SISTEMA DE OBSERVACIÓN

### Score Inicial < 50
```
Resultado: BAJA PRIORIDAD
Acción: Descartar inmediatamente
```

### Score Inicial 50-69
```
Resultado: Activar observación obligatoria
Duración mínima: 2 minutos
Duración máxima: 5 minutos

PROTECCIÓN:
- Está PROHIBIDO descartar por falta de movimiento inicial
- Evaluar evolución de: OI, CVD, Delta, Order Book
```

### Score Inicial 70-84
```
Resultado: Activar observación obligatoria
Duración mínima: 3 minutos
Duración máxima: 5 minutos

Buscar:
- Absorción
- Agotamiento
- Cambio de dominancia
```

### Score Inicial ≥ 85
```
Resultado: ALTA PRIORIDAD (automático)
Duración: 1-3 minutos (confirmación)
```

---

## 🛡️ PROTECCIÓN CONTRA DESCARTE PREMATURO

### ❌ PROHIBIDO descartar una señal porque:
- No exista movimiento en los primeros 30 segundos
- No exista movimiento en los primeros 60 segundos
- No exista movimiento en los primeros 90 segundos

### ✅ La ausencia de movimiento inmediato NO invalida la señal

### ✅ Evaluación centrada en:
- Evolución de **OI**
- Evolución de **CVD**
- Evolución de **Delta**
- Evolución de **Order Book**

**Durante el período mínimo obligatorio.**

---

## 📈 UMBRAL OFICIAL DE ALTA PRIORIDAD

### ⚠️ IMPORTANTE
```
Score ≥ 85/100
```

**Este es el umbral oficial del PERFIL VOLUMEN.**

**NO utilizar valores diferentes.**

### Clasificación Automática
Cuando el score alcanza **85 o más**:
- ✅ Clasificar inmediatamente como: **ALTA PRIORIDAD**
- ✅ Cambiar estado a: **LONG AHORA** o **SHORT AHORA**

---

## 🔄 REGLA DE RECLASIFICACIÓN

### Durante la observación:

#### Si Score ≥ 85
```
Acción: Cambiar inmediatamente a ALTA PRIORIDAD
Estado: LONG AHORA / SHORT AHORA
```

#### Si Score < 50 (después del tiempo mínimo)
```
Acción: Cambiar a BAJA PRIORIDAD
Estado: DESCARTADO
Finalizar: Terminar evaluación
```

#### Si 50 ≤ Score < 85
```
Acción: Mantener en PRIORIDAD MEDIA
Estado: EN ANÁLISIS
Continuar: Seguir evaluando
```

---

## 📊 ANÁLISIS DE MÉTRICAS

### 1. Open Interest (25%)
**Analizar:**
- Variación reciente
- Intensidad
- Velocidad del cambio

**Determinar:**
- Continuación
- Agotamiento
- Posible reversión

### 2. CVD (25%)
**Analizar:**
- Divergencias precio/CVD
- Absorción
- Pérdida de impulso

**Ejemplo:**
- Precio → nuevo máximo
- CVD → NO confirma
- **Resultado:** Posible agotamiento

### 3. Delta (20%)
**Analizar:**
- Compras agresivas vs ventas agresivas
- Cambio de dominancia
- Debilitamiento de agresión

### 4. Order Book Imbalance (10%)
**Analizar:**
- Bid Liquidity vs Ask Liquidity
- Muros de compra/venta
- Desequilibrios

**Ejemplo (SOBRECOMPRA):**
- Aparecen grandes órdenes pasivas de venta
- **Resultado:** Mayor probabilidad de rechazo

**Ejemplo (SOBREVENTA):**
- Aparecen grandes órdenes pasivas de compra
- **Resultado:** Mayor probabilidad de rebote

### 5. Liquidity Sweeps (10%)
**Analizar:** Barridos en 15m, 30m, 1H, 4H

**IMPORTANTE:**
- ❌ NO esperar cierre de velas
- ✅ Solo confirmar si el sweep YA ocurrió

**Prioridad de timeframes:**
1. 4H (mayor peso)
2. 1H
3. 30m
4. 15m (menor peso)

### 6. Momentum Decay (5%)
**Analizar:**
- Velocidad del movimiento
- Desaceleración
- Pérdida progresiva de impulso

**Ejemplo:**
```
+1.2% → +0.8% → +0.4% → +0.1%
```
**Resultado:** Agotamiento progresivo

### 7. Funding Rate (3%)
**Uso:** Solo contexto adicional  
**NUNCA como factor principal**

### 8. VWAP (2%)
**Uso:** Solo contexto adicional  
**NUNCA como factor principal**

---

## 📱 FORMATO DE SALIDA

```
━━━━━━━━━━━━━━━━━━━━━━
📊 EVALUACIÓN VOLUMEN (1M)
━━━━━━━━━━━━━━━━━━━━━━

Símbolo: BTCUSDT
Dirección: 🔴 SHORT
Tipo: SOBRECOMPRA

━━━━━━━━━━━━━━━━━━━━━━
📊 MÉTRICAS:

• OI: 80/100
  OI disminuyendo (agotamiento)

• CVD: 85/100
  Divergencia bajista detectada

• Delta: 75/100
  Agresión compradora debilitándose

• Order Book: 80/100
  Muros de venta dominantes

• Sweeps: 70/100
  Barrido 1H detectado

• Momentum: 75/100
  Desaceleración progresiva

• Funding: 60/100
  FR neutral

• VWAP: 55/100
  Precio 1.5σ sobre VWAP

━━━━━━━━━━━━━━━━━━━━━━
🎯 PUNTUACIÓN FINAL: 87/100
🔴 ALTA PRIORIDAD

━━━━━━━━━━━━━━━━━━━━━━
⭐ FACTORES PRINCIPALES:

1. CVD: Divergencia bajista (21.3 pts)
2. Order Book: Muros venta (8.0 pts)
3. OI: Disminuyendo (20.0 pts)

━━━━━━━━━━━━━━━━━━━━━━
📝 CONCLUSIÓN:

La condición observada sugiere:
✅ AGOTAMIENTO de presión compradora
✅ ABSORCIÓN por vendedores
✅ Probabilidad de REVERSIÓN a corto plazo (1-5 min)

⏰ Evaluado: 14:32:18
```

---

## ✅ CHECKLIST DE CUMPLIMIENTO

- [x] Pesos suman exactamente 100
- [x] Umbral ALTA PRIORIDAD = 85
- [x] Umbral descarte VOLUMEN = 50
- [x] Observación mínima implementada (2-3 min)
- [x] Protección contra descarte prematuro
- [x] Separación total de FIBO
- [x] NO mezcla scores
- [x] NO mezcla pesos
- [x] NO mezcla confirmaciones
- [x] NO usa VOLUME en VOLUMEN
- [x] NO usa Order Book/Momentum en FIBO
- [x] Temporalidad 1M respetada
- [x] NO espera cierres de velas 15m/30m/1H/4H
- [x] Funding y VWAP solo como contexto

---

## 🚀 ESTADO

✅ **PERFIL VOLUMEN:** Actualizado con reglas oficiales  
✅ **AISLAMIENTO:** 100% independiente de FIBO  
✅ **UMBRALES:** Correctos (85 ALTA, 50 descarte)  
✅ **PROTECCIÓN:** Contra descarte prematuro implementada  
✅ **SISTEMA:** Listo para producción

---

**Versión:** 3.0  
**Fecha:** 2026-06-07  
**Status:** PRODUCCIÓN READY ✅
