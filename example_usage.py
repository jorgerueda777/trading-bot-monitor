"""
Ejemplo de uso completo del Motor de Clasificación
"""
from datetime import datetime
from src.core.classifier import EventClassifier
from src.storage.historical_storage import HistoricalStorage


def main():
    # Inicializar clasificador
    classifier = EventClassifier()
    storage = HistoricalStorage()
    
    # Evento de ejemplo
    event_text = """#ZORAUSDT
SESGO ALCISTA
ORIGEN: FIBO 1D
ZONA A: 0.0083000
ZONA B: 0.008217
OBJETIVO A: 0.0103743
OBJETIVO B: 0.0116557"""
    
    # Datos de mercado simulados (en producción vendrían de exchange)
    market_data = {
        'current_price': 0.0082500,
        
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
            'current_price': 0.0082500,
            'vwap': 0.0081000,
            'std_dev': 0.0002,
            'num_std_devs': 1.8
        }
    }
    
    # Clasificar evento
    classification = classifier.classify_event(
        event_text,
        market_data,
        datetime.now()
    )
    
    # Mostrar resultado formateado
    print(classifier.format_output(classification))
    
    # Guardar en histórico
    storage.save_classification(classification.model_dump())
    
    # Ejemplo de actualización con outcome real (después de tiempo)
    # outcome = {
    #     'reached_target': True,
    #     'max_favorable_move': 15.5,
    #     'time_to_target': 12.5,
    #     'drawdown': 2.3
    # }
    # storage.save_classification(classification.model_dump(), outcome)
    
    print("\n\n=== ANÁLISIS HISTÓRICO ===")
    
    # Calcular precisión por prioridad
    accuracy = storage.calculate_accuracy_by_priority()
    print("\nPrecisión por nivel de prioridad:")
    for priority, acc in accuracy.items():
        print(f"  {priority}: {acc*100:.1f}%")
    
    # Sugerir ajustes de pesos
    suggestions = storage.suggest_weight_adjustments()
    if suggestions:
        print("\nSugerencias de ajuste de pesos:")
        for metric, diff in suggestions.items():
            direction = "aumentar" if diff > 0 else "disminuir"
            print(f"  {metric}: {direction} peso (correlación: {abs(diff):.2f})")


if __name__ == "__main__":
    main()
