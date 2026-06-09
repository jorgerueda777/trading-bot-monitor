"""
Evaluador de VWAP
Analiza distancia, desviaciones estándar y retorno a la media
"""
from typing import Dict, Any
from .base_metric import MetricEvaluator


class VWAPEvaluator(MetricEvaluator):
    """Evalúa VWAP"""
    
    def evaluate(self, data: Dict[str, Any]) -> float:
        """
        Evalúa VWAP basado en:
        - Distancia respecto al VWAP
        - Desviaciones estándar
        - Probabilidad de retorno a la media
        
        Args:
            data: {
                'current_price': float,
                'vwap': float,
                'std_dev': float,
                'num_std_devs': float
            }
        """
        price = data.get('current_price', 0)
        vwap = data.get('vwap', 0)
        std_dev = data.get('std_dev', 0)
        num_stds = data.get('num_std_devs', 0)
        
        if vwap == 0:
            return 50.0
        
        # Distancia porcentual
        distance_pct = abs(price - vwap) / vwap * 100
        
        # Puntuación por desviaciones estándar
        # Más alejado = mayor probabilidad de retorno
        if abs(num_stds) >= 2.5:
            score = 90
        elif abs(num_stds) >= 2.0:
            score = 75
        elif abs(num_stds) >= 1.5:
            score = 60
        elif abs(num_stds) >= 1.0:
            score = 45
        else:
            score = 30
        
        return float(score)
    
    def get_analysis(self, data: Dict[str, Any]) -> str:
        """Genera análisis textual"""
        price = data.get('current_price', 0)
        vwap = data.get('vwap', 0)
        num_stds = data.get('num_std_devs', 0)
        
        if vwap > 0:
            position = "por encima" if price > vwap else "por debajo"
            return f"VWAP: {abs(num_stds):.1f}σ {position}"
        
        return "VWAP: no disponible"
