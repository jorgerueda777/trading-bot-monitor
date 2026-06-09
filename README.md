# Motor de Clasificación de Eventos de Mercado

Sistema de scoring y clasificación de eventos estructurados provenientes de detectores externos de oportunidades de mercado.

## Propósito

Sistema que **NO** ejecuta operaciones ni genera recomendaciones financieras.

**Función exclusiva:**
- Interpretar eventos recibidos
- Identificar categorías
- Analizar métricas complementarias
- Asignar puntuación de confianza
- Clasificar por prioridad

## Arquitectura

```
event-classifier/
├── src/
│   ├── core/
│   │   ├── parser.py          # Interpretación de eventos
│   │   ├── classifier.py      # Clasificación y scoring
│   │   └── validator.py       # Validación temporal
│   ├── metrics/
│   │   ├── open_interest.py
│   │   ├── funding_rate.py
│   │   ├── cvd.py
│   │   ├── delta.py
│   │   ├── volume.py
│   │   ├── liquidity_sweeps.py
│   │   └── vwap.py
│   ├── profiles/
│   │   └── evaluation_profiles.py
│   ├── storage/
│   │   └── historical_storage.py
│   └── api/
│       └── event_api.py
├── tests/
├── config/
└── requirements.txt
```

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

```python
from src.core.classifier import EventClassifier

classifier = EventClassifier()
result = classifier.classify_event(event_text)
print(result)
```
