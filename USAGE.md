# Guía de Uso

## Inicio Rápido

### 1. Instalación

```bash
# Clonar repositorio
git clone <repo-url>
cd event-classifier

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Uso Básico (Python)

```python
from datetime import datetime
from src.core.classifier import EventClassifier

# Inicializar clasificador
classifier = EventClassifier()

# Evento a clasificar
event_text = """#BTCUSDT
SESGO ALCISTA
ORIGEN: FIBO 4H
ZONA A: 45000
ZONA B: 44800
OBJETIVO A: 47000
OBJETIVO B: 48500"""

# Datos de mercado actuales
market_data = {
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
        'current': 5000,
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
        'sweeps': {
            '15m': False,
            '30m': True,
            '1H': True,
            '4H': True
        },
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
result = classifier.classify_event(event_text, market_data, datetime.now())

# Mostrar resultado
print(classifier.format_output(result))
```

### 3. Uso con API REST

#### Iniciar servidor

```bash
uvicorn src.api.event_api:app --reload
```

#### Clasificar evento (cURL)

```bash
curl -X POST "http://localhost:8000/classify" \
  -H "Content-Type: application/json" \
  -d '{
    "event_text": "#BTCUSDT\nSESGO ALCISTA\nORIGEN: FIBO 4H\nZONA A: 45000\nZONA B: 44800\nOBJETIVO A: 47000\nOBJETIVO B: 48500",
    "market_data": {
      "current_price": 44900,
      "open_interest": {
        "current": 15000000,
        "previous": 12000000,
        "trend": "INCREASING",
        "change_intensity": 75
      },
      "funding": {
        "current": 0.0085,
        "mean": 0.0010,
        "std_dev": 0.0030,
        "is_extreme": false
      },
      "cvd": {
        "has_divergence": true,
        "slope_change": "NEGATIVE_TO_POSITIVE",
        "exhaustion_signal": false,
        "alignment_with_bias": true
      },
      "delta": {
        "current": 5000,
        "buyer_intensity": 75,
        "seller_intensity": 25,
        "has_sharp_change": true,
        "bias": "BULLISH"
      },
      "volume": {
        "current": 8500000,
        "avg_20": 4000000,
        "is_anomaly": true
      },
      "liquidity_sweeps": {
        "sweeps": {
          "15m": false,
          "30m": true,
          "1H": true,
          "4H": true
        },
        "sweep_quality": 85,
        "time_since_last_sweep": 1.5
      },
      "vwap": {
        "current_price": 44900,
        "vwap": 44500,
        "std_dev": 200,
        "num_std_devs": 2.0
      }
    }
  }'
```

#### Clasificar evento (Python requests)

```python
import requests

response = requests.post(
    "http://localhost:8000/classify",
    json={
        "event_text": event_text,
        "market_data": market_data
    }
)

result = response.json()
print(f"Prioridad: {result['priority']}")
print(f"Score: {result['final_score']}")
```

#### Obtener estadísticas

```bash
# Precisión por prioridad
curl "http://localhost:8000/statistics/accuracy"

# Sugerencias de ajuste de pesos
curl "http://localhost:8000/statistics/weight-suggestions"
```

### 4. Uso con Docker

```bash
# Build
docker build -t event-classifier .

# Run
docker run -p 8000:8000 event-classifier

# Con volumen para persistir datos
docker run -p 8000:8000 -v $(pwd)/data:/app/data event-classifier
```

## Formato de Entrada

### Evento (texto)

```
#<SYMBOL>
SESGO <ALCISTA|BAJISTA>
ORIGEN: FIBO <1H|4H|1D>
ZONA A: <precio>
ZONA B: <precio>
OBJETIVO A: <precio>
OBJETIVO B: <precio>
```

### Market Data (JSON)

```json
{
  "current_price": float,
  
  "open_interest": {
    "current": float,
    "previous": float,
    "trend": "INCREASING" | "DECREASING" | "STABLE",
    "change_intensity": float (0-100)
  },
  
  "funding": {
    "current": float,
    "mean": float,
    "std_dev": float,
    "is_extreme": bool
  },
  
  "cvd": {
    "has_divergence": bool,
    "slope_change": "POSITIVE_TO_NEGATIVE" | "NEGATIVE_TO_POSITIVE" | "STABLE",
    "exhaustion_signal": bool,
    "alignment_with_bias": bool
  },
  
  "delta": {
    "current": float,
    "buyer_intensity": float (0-100),
    "seller_intensity": float (0-100),
    "has_sharp_change": bool,
    "bias": "BULLISH" | "BEARISH"
  },
  
  "volume": {
    "current": float,
    "avg_20": float,
    "is_anomaly": bool
  },
  
  "liquidity_sweeps": {
    "sweeps": {
      "15m": bool,
      "30m": bool,
      "1H": bool,
      "4H": bool
    },
    "sweep_quality": float (0-100),
    "time_since_last_sweep": float (horas)
  },
  
  "vwap": {
    "current_price": float,
    "vwap": float,
    "std_dev": float,
    "num_std_devs": float
  }
}
```

## Formato de Salida

```json
{
  "symbol": "BTCUSDT",
  "bias": "BULLISH",
  "origin": "FIBO_4H",
  "status": "VIGENTE",
  
  "open_interest": {
    "name": "Open Interest",
    "score": 85.0,
    "weight": 25,
    "weighted_score": 21.25,
    "analysis": "OI increasing, variación: +25.00%"
  },
  
  // ... otras métricas ...
  
  "final_score": 78.5,
  "priority": "PRIORIDAD MEDIA",
  
  "key_factors": [
    "Open Interest: OI increasing (peso: 21.3)",
    "CVD: divergencia detectada (peso: 18.0)",
    "Delta: dominancia compradora (peso: 15.8)"
  ],
  
  "evaluated_at": "2024-01-15T10:30:00"
}
```

## Actualización de Outcomes

Para mejorar la precisión del sistema, actualiza los outcomes reales:

```python
from src.storage.historical_storage import HistoricalStorage

storage = HistoricalStorage()

outcome = {
    'reached_target': True,
    'max_favorable_move': 15.5,  # %
    'time_to_target': 12.5,       # horas
    'drawdown': 2.3               # %
}

storage.save_classification(classification.dict(), outcome)
```

## Análisis Histórico

```python
# Calcular precisión por prioridad
accuracy = storage.calculate_accuracy_by_priority()
print(accuracy)
# {'ALTA PRIORIDAD': 0.78, 'PRIORIDAD MEDIA': 0.62, 'BAJA PRIORIDAD': 0.41}

# Obtener sugerencias de ajuste
suggestions = storage.suggest_weight_adjustments()
print(suggestions)
# {'open_interest': 0.15, 'cvd': -0.05, ...}
```

## Testing

```bash
# Ejecutar todos los tests
pytest tests/ -v

# Con coverage
pytest tests/ -v --cov=src --cov-report=html

# Test específico
pytest tests/test_classifier.py -v
```

## Integración con Sistemas Externos

### Ejemplo: Telegram Bot

```python
from telegram import Update
from telegram.ext import Updater, CommandHandler
from src.core.classifier import EventClassifier

classifier = EventClassifier()

def classify_command(update: Update, context):
    event_text = update.message.text
    # Obtener market_data desde exchange
    market_data = get_market_data()
    
    result = classifier.classify_event(event_text, market_data)
    update.message.reply_text(classifier.format_output(result))

updater = Updater("TOKEN")
updater.dispatcher.add_handler(CommandHandler("classify", classify_command))
updater.start_polling()
```

### Ejemplo: WebSocket Stream

```python
import asyncio
import websockets
from src.core.classifier import EventClassifier

classifier = EventClassifier()

async def process_events(websocket, path):
    async for message in websocket:
        event_text = message
        market_data = get_market_data()
        
        result = classifier.classify_event(event_text, market_data)
        await websocket.send(result.json())

start_server = websockets.serve(process_events, "localhost", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
```

## Troubleshooting

### Error: "No se pudo extraer símbolo"

Verifica que el evento comience con `#SYMBOL` o `SYMBOL`.

### Error: "La suma de pesos debe ser 100"

Al crear perfiles personalizados, asegúrate de que los pesos sumen exactamente 100.

### Clasificaciones inconsistentes

Verifica que `market_data` contenga todos los campos requeridos.

## Soporte

Para reportar issues o solicitar features, abre un issue en el repositorio.
