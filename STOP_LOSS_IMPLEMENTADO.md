# Stop Loss - Implementación Completa

**Fecha**: 2026-06-09  
**Estado**: ✅ Completado

## Resumen

Se ha implementado la extracción y visualización del stop loss en todo el flujo del sistema:
- Parser extrae stop loss del mensaje
- Classifier propaga stop loss a EventClassification
- Monitor muestra stop loss en formato compacto

---

## Cambios Realizados

### 1. Parser (`src/core/parser.py`)

**Método agregado**: `_extract_stop_loss(text: str) -> float`

**Formatos soportados**:
```
✅ STOP LOSS: 2.5 % ($ 0.0726623)
✅ ⚠️ STOP LOSS: 2.5 % ($ 98400)
✅ 🛑 STOP LOSS: $ 3350
✅ SL: $ 670
✅ STOP: $ 141.14
```

**Regex utilizado**:
- Con paréntesis (decimales): `\(\$\s*([\d]+\.[\d]+)\)`
- Sin paréntesis (con o sin decimales): `\$\s*([\d]+(?:\.[\d]+)?)`

**Formatos de precio soportados**:
- Con decimales: `$ 0.0726623`
- Sin decimales: `$ 98400`
- En paréntesis: `($ 0.0726623)`

**Validación**: Precio debe estar entre 0.00000001 y 1,000,000

**Mejora adicional**: Se actualizó `_extract_entries()` para soportar precios sin decimales (e.g., `$ 95000`) además de los decimales (e.g., `$ 0.0708900`). Regex mejorado: `\$\s*([\d]+(?:\.[\d]+)?)`

---

### 2. Classifier (`src/core/classifier.py`)

**Campo agregado a EventClassification**:
```python
stop_loss: float = 0.0  # Stop Loss
```

**Propagación**: Se pasa `stop_loss=parsed.stop_loss` en el constructor de EventClassification

---

### 3. Monitor (`monitor_grupos.py`)

**Visualización en formato compacto**:
```python
if classification.stop_loss > 0:
    mensaje += f"\n🛑 SL: ${classification.stop_loss:.4f}"
```

**Ejemplo de mensaje**:
```
🔄 **ESPORTSUSDT** 🟢 LONG | Score: **37**/100

**EN_ANALISIS**

📊 VOLUMEN | Entrada: $0.0709
🛑 SL: $0.0727
⏰ 14:40:59
```

---

## Tests

### Test 1: `test_real_message.py`
- ✅ Extracción con mensaje real de ESPORTSUSDT
- ✅ Stop Loss: $0.0726623

### Test 2: `test_stop_loss_complete.py`
- ✅ Parser extrae correctamente
- ✅ Classifier propaga correctamente
- ✅ Formato Telegram muestra correctamente

### Test 3: `test_stop_loss_variants.py`
- ✅ 5 formatos diferentes probados
- ✅ 100% de tests pasados

---

## Flujo Completo

```
Mensaje Telegram
    ↓
Parser._extract_stop_loss()
    ↓
ParsedEvent.stop_loss
    ↓
EventClassifier.classify_event()
    ↓
EventClassification.stop_loss
    ↓
formatear_resumen_telegram()
    ↓
Mensaje en j77: "🛑 SL: $X.XXXX"
```

---

## Compatibilidad

✅ Compatible con señales FIBO  
✅ Compatible con señales VOLUMEN  
✅ No rompe señales sin stop loss (muestra 0.0)  
✅ Validación de rango de precios  
✅ Formato compacto (4 decimales)

---

## Próximos Pasos (Opcionales)

- [ ] Calcular % de distancia al stop loss
- [ ] Alertar si precio actual alcanza el stop loss
- [ ] Incluir stop loss en cálculo de risk/reward
- [ ] Tracking de señales que activaron stop loss

---

## Notas Técnicas

- **Decimales**: Se muestran 4 decimales para mantener precisión
- **Emoji**: 🛑 indica stop loss
- **Posición**: Se muestra después de la entrada, antes del timestamp
- **Opcional**: Solo se muestra si `stop_loss > 0`
