# 🚀 Quick Start - Motor de Clasificación

## En 5 Minutos

### 1️⃣ Clasificar un Evento (Python)

```python
from datetime import datetime
from src.core.classifier import EventClassifier

# Inicializar
classifier = EventClassifier()

# Tu evento
evento = """#BTCUSDT
SESGO ALCISTA
ORIGEN: FIBO 4H
ZONA A: 45000
ZONA B: 44800
OBJETIVO A: 47000
OBJETIVO B: 48500"""

# Datos actuales del mercado (obtenerlos de tu exchange)
datos_mercado = {
    'current_price': 44900,
    'open_interest': {
        'current': 15000000,
        'previous': 12000000,
        'trend': 'INCREASING',
        'change_intensity': 75
    },
    'funding': {
        'current': 0.0085,
        'mean': 0.0010,
        'std_dev': 0.0030,
        'is_extreme': False
    },
    'cvd': {
        'has_divergence': True,
        'slope_change': 'NEGATIVE_TO_POSITIVE',
        'exhaustion_signal': False,
        'alignment_with_bias': True
    },
    'delta': {
        'buyer_intensity': 75,
        'seller_intensity': 25,
        'has_sharp_change': True,
        'bias': 'BULLISH'
    },
    'volume': {
        'current': 8500000,
        'avg_20': 4000000,
        'is_anomaly': True
    },
    'liquidity_sweeps': {
        'sweeps': {'15m': False, '30m': True, '1H': True, '4H': True},
        'sweep_quality': 85,
        'time_since_last_sweep': 1.5
    },
    'vwap': {
        'current_price': 44900,
        'vwap': 44500,
        'std_dev': 200,
        'num_std_devs': 2.0
    }
}

# Clasificar
resultado = classifier.classify_event(evento, datos_mercado, datetime.now())

# Ver resultado
print(f"Score: {resultado.final_score}/100")
print(f"Prioridad: {resultado.priority}")
print(f"Factores clave: {resultado.key_factors[0]}")
```

**Salida esperada:**
```
Score: 94.43/100
Prioridad: ALTA PRIORIDAD
Factores clave: Open Interest: OI increasing, variación: +25.00% (peso: 23.9)
```

---

## 2️⃣ Usando la API REST

### Iniciar servidor
```bash
python -m uvicorn src.api.event_api:app --host 0.0.0.0 --port 8000
```

### Clasificar evento (cURL)
```bash
curl -X POST "http://localhost:8000/classify" \
  -H "Content-Type: application/json" \
  -d '{
    "event_text": "#BTCUSDT\nSESGO ALCISTA\nORIGEN: FIBO 4H\nZONA A: 45000\nZONA B: 44800\nOBJETIVO A: 47000\nOBJETIVO B: 48500",
    "market_data": { ... }
  }'
```

### Clasificar evento (Python requests)
```python
import requests

response = requests.post(
    "http://localhost:8000/classify",
    json={
        "event_text": evento,
        "market_data": datos_mercado
    }
)

resultado = response.json()
print(f"Score: {resultado['final_score']}")
print(f"Prioridad: {resultado['priority']}")
```

---

## 3️⃣ Ejecutar Demo Completa

```bash
# Ver 3 ejemplos de clasificación completos
python demo_completo.py
```

Esto ejecutará:
- ✅ Evento ALTA PRIORIDAD (señales fuertes)
- ✅ Evento PRIORIDAD MEDIA (señales mixtas)
- ✅ Evento BAJA PRIORIDAD (señales débiles)
- 📊 Análisis histórico y estadísticas
- 🔧 Sugerencias de recalibración

---

## 4️⃣ Integración con Exchange Real

### Ejemplo: Binance WebSocket

```python
import websocket
import json
from src.core.classifier import EventClassifier

classifier = EventClassifier()

def on_message(ws, message):
    data = json.loads(message)
    
    # Construir market_data desde el exchange
    market_data = construir_market_data(data)
    
    # Clasificar
    resultado = classifier.classify_event(
        evento_detectado,
        market_data,
        datetime.now()
    )
    
    # Actuar según prioridad
    if resultado.priority == "ALTA PRIORIDAD":
        print(f"🔥 ALERTA: {resultado.symbol} - Score: {resultado.final_score}")
        # Aquí enviar notificación, log, etc.

# Conectar a Binance
ws = websocket.WebSocketApp(
    "wss://fstream.binance.com/ws/btcusdt@aggTrade",
    on_message=on_message
)
ws.run_forever()
```

---

## 5️⃣ Actualizar Outcomes (para recalibración)

```python
from src.storage.historical_storage import HistoricalStorage

storage = HistoricalStorage()

# Después de que el evento se resuelva, actualizar con el outcome real
outcome = {
    'reached_target': True,      # ¿Se alcanzó el objetivo?
    'max_favorable_move': 18.5,  # % de movimiento favorable máximo
    'time_to_target': 8.2,       # Horas hasta alcanzar objetivo
    'drawdown': 1.5              # % de drawdown máximo
}

storage.save_classification(resultado.model_dump(), outcome)
```

---

## 📋 Checklist de Integración

### Preparación
- [ ] Instalar dependencias: `pip install -r requirements.txt`
- [ ] Ejecutar tests: `python -m pytest tests/ -v`
- [ ] Ejecutar demo: `python demo_completo.py`

### Configuración
- [ ] Copiar `.env.example` a `.env`
- [ ] Configurar conexión a exchange (API keys)
- [ ] Ajustar perfiles en `config/profiles_config.json` si es necesario

### Integración
- [ ] Implementar función para obtener `market_data` desde exchange
- [ ] Implementar lógica de detección de eventos
- [ ] Conectar clasificador al flujo de eventos
- [ ] Configurar almacenamiento de resultados

### Producción
- [ ] Configurar logging estructurado
- [ ] Implementar monitoring (Prometheus/Grafana)
- [ ] Configurar alertas para alta prioridad
- [ ] Setup de backup para datos históricos
- [ ] Dockerizar aplicación: `docker build -t event-classifier .`

---

## 🎯 Casos de Uso Comunes

### 1. Bot de Trading (solo clasificación, NO ejecución)
```python
# El bot detecta un evento
evento = detector.detectar_setup()

# Clasificar
score = classifier.classify_event(evento, obtener_market_data(), now())

# Tomar decisión HUMANA basada en clasificación
if score.priority == "ALTA PRIORIDAD" and score.final_score > 85:
    notificar_trader(f"Setup de alta calidad: {evento.symbol}")
```

### 2. Sistema de Alertas
```python
# Clasificar múltiples eventos
eventos = obtener_eventos_pendientes()

for evento in eventos:
    resultado = classifier.classify_event(evento, market_data, now())
    
    if resultado.priority == "ALTA PRIORIDAD":
        enviar_telegram(f"🔥 {resultado.symbol}: {resultado.final_score}")
    elif resultado.priority == "PRIORIDAD MEDIA":
        enviar_email(f"⚠️ {resultado.symbol}: {resultado.final_score}")
```

### 3. Backtesting
```python
# Evaluar eventos históricos
resultados = []

for evento_historico in dataset:
    resultado = classifier.classify_event(
        evento_historico.text,
        evento_historico.market_data,
        evento_historico.timestamp
    )
    
    resultados.append({
        'score': resultado.final_score,
        'priority': resultado.priority,
        'success': evento_historico.alcanzó_objetivo
    })

# Analizar correlación score vs éxito
calcular_metricas(resultados)
```

---

## 🔧 Troubleshooting

### Error: "No se pudo extraer símbolo"
**Solución:** Verifica que el evento comience con `#SYMBOL`

### Error: "La suma de pesos debe ser 100"
**Solución:** Al modificar perfiles, asegúrate que los pesos sumen exactamente 100

### Clasificaciones inconsistentes
**Solución:** Verifica que `market_data` contenga todos los campos requeridos

### API no responde
**Solución:** Verifica que el puerto 8000 esté disponible: `netstat -an | findstr :8000`

---

## 📚 Recursos Adicionales

- **Documentación completa:** Ver `USAGE.md`
- **Arquitectura:** Ver `ARCHITECTURE.md`
- **Roadmap:** Ver `ROADMAP.md`
- **API docs:** Acceder a `http://localhost:8000/docs` cuando la API esté corriendo

---

## ⚡ Pro Tips

1. **Cache de métricas:** Las métricas de exchange no cambian cada segundo. Cachea OI, Funding durante 30-60 segundos.

2. **Batch processing:** Si tienes múltiples eventos, procésalos en lote para mejor performance.

3. **Monitoring:** Monitorea el `final_score` distribution. Si la mayoría está en 40-60, ajusta los pesos.

4. **Históricos:** Mantén al menos 30 días de datos históricos para recalibración efectiva.

5. **A/B Testing:** Mantén el sistema actual y compara con el motor de clasificación durante 2 semanas antes de confiar 100%.

---

**¿Listo para empezar? Ejecuta:** `python demo_completo.py` 🚀
