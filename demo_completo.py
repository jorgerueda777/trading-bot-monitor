"""
Demo completo del Motor de Clasificación
Muestra todas las capacidades del sistema
"""
from datetime import datetime, timedelta
from src.core.classifier import EventClassifier
from src.storage.historical_storage import HistoricalStorage

print("=" * 80)
print("DEMO COMPLETO - MOTOR DE CLASIFICACIÓN DE EVENTOS DE MERCADO")
print("=" * 80)
print()

# Inicializar sistema
classifier = EventClassifier()
storage = HistoricalStorage()

# ============================================================================
# EJEMPLO 1: Evento de ALTA PRIORIDAD
# ============================================================================
print("\n" + "=" * 80)
print("EJEMPLO 1: Evento con señales fuertes - Esperamos ALTA PRIORIDAD")
print("=" * 80)

event1 = """#BTCUSDT
SESGO ALCISTA
ORIGEN: FIBO 4H
ZONA A: 45000
ZONA B: 44800
OBJETIVO A: 47000
OBJETIVO B: 48500"""

market_data1 = {
    'current_price': 44900,
    'open_interest': {
        'current': 15000000,
        'previous': 12000000,
        'trend': 'INCREASING',
        'change_intensity': 85
    },
    'funding': {
        'current': 0.0120,
        'mean': 0.0010,
        'std_dev': 0.0030,
        'is_extreme': True
    },
    'cvd': {
        'has_divergence': True,
        'slope_change': 'NEGATIVE_TO_POSITIVE',
        'exhaustion_signal': False,
        'alignment_with_bias': True
    },
    'delta': {
        'current': 5000,
        'buyer_intensity': 85,
        'seller_intensity': 15,
        'has_sharp_change': True,
        'bias': 'BULLISH'
    },
    'volume': {
        'current': 8500000,
        'avg_20': 3000000,
        'is_anomaly': True
    },
    'liquidity_sweeps': {
        'sweeps': {
            '15m': True,
            '30m': True,
            '1H': True,
            '4H': True
        },
        'sweep_quality': 90,
        'time_since_last_sweep': 0.5
    },
    'vwap': {
        'current_price': 44900,
        'vwap': 44000,
        'std_dev': 300,
        'num_std_devs': 2.5
    }
}

result1 = classifier.classify_event(event1, market_data1, datetime.now())
print(classifier.format_output(result1))

# Guardar con outcome simulado exitoso
storage.save_classification(
    result1.model_dump(),
    {
        'reached_target': True,
        'max_favorable_move': 18.5,
        'time_to_target': 8.2,
        'drawdown': 1.5
    }
)

# ============================================================================
# EJEMPLO 2: Evento de PRIORIDAD MEDIA
# ============================================================================
print("\n" + "=" * 80)
print("EJEMPLO 2: Evento con señales mixtas - Esperamos PRIORIDAD MEDIA")
print("=" * 80)

event2 = """#ETHUSDT
SESGO BAJISTA
ORIGEN: FIBO 1H
ZONA A: 3200
ZONA B: 3180
OBJETIVO A: 3050
OBJETIVO B: 2980"""

market_data2 = {
    'current_price': 3190,
    'open_interest': {
        'current': 8000000,
        'previous': 8200000,
        'trend': 'DECREASING',
        'change_intensity': 35
    },
    'funding': {
        'current': -0.0015,
        'mean': 0.0010,
        'std_dev': 0.0030,
        'is_extreme': False
    },
    'cvd': {
        'has_divergence': False,
        'slope_change': 'STABLE',
        'exhaustion_signal': False,
        'alignment_with_bias': True
    },
    'delta': {
        'current': -2000,
        'buyer_intensity': 40,
        'seller_intensity': 60,
        'has_sharp_change': False,
        'bias': 'BEARISH'
    },
    'volume': {
        'current': 4500000,
        'avg_20': 4000000,
        'is_anomaly': False
    },
    'liquidity_sweeps': {
        'sweeps': {
            '15m': True,
            '30m': False,
            '1H': False,
            '4H': False
        },
        'sweep_quality': 60,
        'time_since_last_sweep': 2.0
    },
    'vwap': {
        'current_price': 3190,
        'vwap': 3200,
        'std_dev': 50,
        'num_std_devs': 0.8
    }
}

result2 = classifier.classify_event(event2, market_data2, datetime.now())
print(classifier.format_output(result2))

# Guardar con outcome simulado parcial
storage.save_classification(
    result2.model_dump(),
    {
        'reached_target': True,
        'max_favorable_move': 8.3,
        'time_to_target': 3.5,
        'drawdown': 3.2
    }
)

# ============================================================================
# EJEMPLO 3: Evento de BAJA PRIORIDAD
# ============================================================================
print("\n" + "=" * 80)
print("EJEMPLO 3: Evento con señales débiles - Esperamos BAJA PRIORIDAD")
print("=" * 80)

event3 = """#SOLUSDT
SESGO ALCISTA
ORIGEN: FIBO 1D
ZONA A: 180
ZONA B: 178
OBJETIVO A: 195
OBJETIVO B: 205"""

market_data3 = {
    'current_price': 179,
    'open_interest': {
        'current': 5000000,
        'previous': 5100000,
        'trend': 'STABLE',
        'change_intensity': 15
    },
    'funding': {
        'current': 0.0005,
        'mean': 0.0010,
        'std_dev': 0.0030,
        'is_extreme': False
    },
    'cvd': {
        'has_divergence': False,
        'slope_change': 'STABLE',
        'exhaustion_signal': True,
        'alignment_with_bias': False
    },
    'delta': {
        'current': 100,
        'buyer_intensity': 52,
        'seller_intensity': 48,
        'has_sharp_change': False,
        'bias': 'BULLISH'
    },
    'volume': {
        'current': 3000000,
        'avg_20': 4000000,
        'is_anomaly': False
    },
    'liquidity_sweeps': {
        'sweeps': {
            '15m': False,
            '30m': False,
            '1H': False,
            '4H': False
        },
        'sweep_quality': 30,
        'time_since_last_sweep': 12.0
    },
    'vwap': {
        'current_price': 179,
        'vwap': 180,
        'std_dev': 10,
        'num_std_devs': 0.3
    }
}

result3 = classifier.classify_event(event3, market_data3, datetime.now())
print(classifier.format_output(result3))

# Guardar con outcome simulado fallido
storage.save_classification(
    result3.model_dump(),
    {
        'reached_target': False,
        'max_favorable_move': 2.1,
        'time_to_target': 0,
        'drawdown': 5.8
    }
)

# ============================================================================
# ANÁLISIS HISTÓRICO Y ESTADÍSTICAS
# ============================================================================
print("\n" + "=" * 80)
print("ANÁLISIS HISTÓRICO Y ESTADÍSTICAS")
print("=" * 80)

# Calcular precisión por prioridad
accuracy = storage.calculate_accuracy_by_priority()
print("\n📊 Precisión por nivel de prioridad:")
for priority, acc in accuracy.items():
    status = "✅" if acc >= 0.7 else "⚠️" if acc >= 0.5 else "❌"
    print(f"  {status} {priority}: {acc*100:.1f}%")

# Sugerir ajustes de pesos
print("\n🔧 Sugerencias de ajuste de pesos (basado en correlaciones):")
suggestions = storage.suggest_weight_adjustments()
if suggestions:
    for metric, diff in sorted(suggestions.items(), key=lambda x: abs(x[1]), reverse=True):
        direction = "↑ aumentar" if diff > 0 else "↓ disminuir"
        strength = "fuerte" if abs(diff) > 0.3 else "moderada" if abs(diff) > 0.15 else "leve"
        print(f"  {metric.replace('_', ' ').title():20s} → {direction:12s} (correlación {strength}: {abs(diff):.3f})")
else:
    print("  Aún no hay suficientes datos para sugerencias")

# Resumen de eventos procesados
print("\n📈 Resumen de eventos clasificados hoy:")
records = storage.load_historical_data()
total = len(records)
with_outcome = sum(1 for r in records if r.get('outcome') is not None)
successful = sum(1 for r in records if r.get('outcome') and r['outcome'].get('reached_target'))

print(f"  Total eventos: {total}")
print(f"  Con outcome: {with_outcome}")
print(f"  Exitosos: {successful}")
if with_outcome > 0:
    print(f"  Tasa de éxito: {successful/with_outcome*100:.1f}%")

print("\n" + "=" * 80)
print("✅ DEMO COMPLETADO")
print("=" * 80)
print("\nEl sistema ha demostrado:")
print("  ✓ Clasificación automática de eventos")
print("  ✓ Scoring multi-dimensional con 7 métricas")
print("  ✓ Perfiles adaptativos por timeframe")
print("  ✓ Almacenamiento histórico con outcomes")
print("  ✓ Análisis estadístico y recalibración")
print("  ✓ Identificación de factores clave influyentes")
print("\n💡 El sistema está listo para integración en producción!")
print()
