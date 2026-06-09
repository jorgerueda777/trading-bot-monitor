# Arquitectura del Motor de Clasificación

## Visión General

Sistema de clasificación de eventos de mercado basado en scoring multi-dimensional.

**Responsabilidad única:** Clasificar eventos según relevancia, NO ejecutar operaciones ni dar recomendaciones financieras.

## Componentes Principales

### 1. Core Layer

#### Parser (`src/core/parser.py`)
- Interpreta eventos en formato texto
- Normaliza información a estructura interna
- Extrae: símbolo, sesgo, origen, zonas, objetivos

#### Validator (`src/core/validator.py`)
- Valida vigencia temporal de eventos
- Evalúa distancia respecto a precio actual
- Clasifica como: VIGENTE, PARCIALMENTE_VIGENTE, EXPIRADO

#### Classifier (`src/core/classifier.py`)
- Orquestador principal
- Coordina parser, validator y métricas
- Calcula score final ponderado
- Determina nivel de prioridad

### 2. Metrics Layer

Evaluadores especializados por métrica:

- **OpenInterestEvaluator**: Variación, tendencia, intensidad
- **FundingRateEvaluator**: Nivel, desviación, extremos
- **CVDEvaluator**: Divergencias, cambios de pendiente, agotamiento
- **DeltaEvaluator**: Intensidad compradora/vendedora, cambios bruscos
- **VolumeEvaluator**: Comparación con promedio, anomalías
- **LiquiditySweepsEvaluator**: Barridos en múltiples timeframes
- **VWAPEvaluator**: Distancia, desviaciones estándar, retorno a media

Cada evaluador retorna score 0-100.

### 3. Profiles Layer

Define pesos de métricas según origen temporal:

```
FIBO_1H → Énfasis en métricas de corto plazo
FIBO_4H → Balance entre corto y medio plazo  
FIBO_1D → Énfasis en estructuras macro
```

### 4. Storage Layer

#### HistoricalStorage
- Almacena clasificaciones con outcomes reales
- Permite análisis retrospectivo
- Calcula precisión por prioridad
- Sugiere ajustes de pesos basado en correlaciones

### 5. API Layer

FastAPI REST endpoints:

```
POST /classify          - Clasificar evento
POST /outcome           - Actualizar outcome real
GET  /statistics/accuracy - Precisión por prioridad
GET  /statistics/weight-suggestions - Ajustes sugeridos
GET  /health            - Health check
```

## Flujo de Procesamiento

```
1. Recepción de Evento
   ↓
2. Parsing y Normalización (EventParser)
   ↓
3. Validación Temporal (TemporalValidator)
   ↓
4. Selección de Perfil (get_profile)
   ↓
5. Evaluación de Métricas (7 evaluadores)
   ↓
6. Cálculo de Score Ponderado
   ↓
7. Clasificación de Prioridad
   ↓
8. Almacenamiento Histórico
   ↓
9. Retorno de Resultado
```

## Sistema de Scoring

### Fórmula

```
Score Final = Σ(Score_métrica × Peso_métrica) / 100

donde:
- Score_métrica ∈ [0, 100]
- Σ Pesos = 100
```

### Clasificación

- **0-59**: BAJA PRIORIDAD
- **60-79**: PRIORIDAD MEDIA
- **80-100**: ALTA PRIORIDAD

## Recalibración Automática

### Proceso

1. **Acumulación de Datos**
   - Cada clasificación se almacena
   - Outcomes reales se vinculan a clasificaciones

2. **Análisis de Correlaciones**
   - Score por métrica vs éxito del evento
   - Identificación de métricas más predictivas

3. **Ajuste de Pesos**
   - Incrementar peso de métricas con alta correlación
   - Reducir peso de métricas poco predictivas
   - Respeto de restricciones (suma = 100, cambios graduales)

4. **Validación**
   - Mínimo de muestras requerido
   - Límite en magnitud de ajustes
   - Evaluación de mejora real

### Configuración

```json
{
  "min_samples": 100,
  "learning_rate": 0.05,
  "max_weight_adjustment": 5
}
```

## Mejoras Propuestas

### Corto Plazo

1. **Integración con Exchanges**
   - Binance WebSocket para datos real-time
   - Bybit REST API para datos históricos

2. **Cache Layer**
   - Redis para métricas pre-calculadas
   - Reducción de latencia < 100ms

3. **Monitoring**
   - Prometheus metrics
   - Grafana dashboards
   - Alertas por baja precisión

### Medio Plazo

4. **Machine Learning**
   - Modelo XGBoost para scoring
   - Entrenamiento continuo con outcomes
   - A/B testing vs scoring manual

5. **Backtesting Engine**
   - Replay de eventos históricos
   - Evaluación de cambios en perfiles
   - Optimización de pesos

6. **Multi-Symbol Analysis**
   - Análisis de correlaciones entre pares
   - Detección de movimientos sectoriales

### Largo Plazo

7. **Adaptive Profiles**
   - Perfiles que evolucionan por condiciones de mercado
   - Detección de regímenes (trending, ranging, volatile)

8. **Ensemble Scoring**
   - Múltiples modelos en paralelo
   - Votación ponderada de clasificaciones

9. **Real-time Streaming**
   - Apache Kafka para ingesta
   - Apache Flink para procesamiento
   - Escalabilidad a miles de eventos/segundo

## Consideraciones de Arquitectura

### Escalabilidad

- Stateless design permite horizontal scaling
- Métricas evaluadas en paralelo
- Storage separado de lógica de negocio

### Mantenibilidad

- Evaluadores independientes y testeables
- Perfiles externalizados en configuración
- Logging estructurado para debugging

### Extensibilidad

- Interface `MetricEvaluator` para nuevas métricas
- Perfiles configurables sin cambios de código
- API versionada para compatibilidad

### Performance

- Cálculos vectorizados con numpy
- Cache de datos de mercado
- Lazy loading de históricos

## Stack Tecnológico

- **Python 3.11+**: Lenguaje base
- **Pydantic**: Validación y serialización
- **FastAPI**: API REST
- **Numpy/Pandas**: Cálculos numéricos
- **Redis**: Cache (opcional)
- **PostgreSQL**: Storage persistente (opcional)
- **Docker**: Containerización
- **Kubernetes**: Orquestación (producción)

## Deployment

### Local Development
```bash
pip install -r requirements.txt
python example_usage.py
```

### API Server
```bash
uvicorn src.api.event_api:app --reload
```

### Docker
```bash
docker build -t event-classifier .
docker run -p 8000:8000 event-classifier
```

### Kubernetes
```bash
kubectl apply -f k8s/deployment.yaml
```

## Testing

```bash
pytest tests/ -v --cov=src
```

## Monitoreo

Métricas clave:
- Latencia de clasificación (p50, p95, p99)
- Tasa de clasificaciones por prioridad
- Precisión por prioridad (con outcomes)
- Disponibilidad del servicio
