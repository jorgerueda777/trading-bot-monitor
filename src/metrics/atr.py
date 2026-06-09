"""
Evaluador de ATR (Average True Range)
Mide volatilidad actual vs promedio
"""
from .base_metric import MetricEvaluator


class ATREvaluator(MetricEvaluator):
    """Evalúa la volatilidad mediante ATR"""
    
    def evaluate(self, data: dict) -> float:
        """
        Evalúa ATR actual vs promedio
        
        Args:
            data: {
                'current_atr': float,
                'average_atr': float,
                'atr_ratio': float  # current / average
            }
        
        Returns:
            Score 0-100
        """
        current = data.get('current_atr', 0)
        average = data.get('average_atr', 0)
        
        if average == 0:
            return 50.0
        
        ratio = current / average
        
        # Volatilidad normal (ratio cerca de 1.0) = score medio
        # Volatilidad extrema = score alto (más oportunidad de reversión)
        if ratio >= 2.0:
            # ATR el doble o más del promedio = volatilidad extrema
            return 100.0
        elif ratio >= 1.5:
            # ATR 50% mayor = volatilidad alta
            return 80.0
        elif ratio >= 1.2:
            # ATR 20% mayor = volatilidad moderada alta
            return 60.0
        elif ratio >= 0.8:
            # ATR normal
            return 40.0
        else:
            # ATR muy bajo = poca volatilidad
            return 20.0
    
    def get_analysis(self, data: dict) -> str:
        """Genera análisis descriptivo"""
        current = data.get('current_atr', 0)
        average = data.get('average_atr', 0)
        
        if average == 0:
            return "ATR no disponible"
        
        ratio = current / average
        
        if ratio >= 2.0:
            return f"Volatilidad extrema (ATR {ratio:.1f}x promedio)"
        elif ratio >= 1.5:
            return f"Volatilidad alta (ATR {ratio:.1f}x promedio)"
        elif ratio >= 1.2:
            return f"Volatilidad moderada alta (ATR {ratio:.1f}x)"
        elif ratio >= 0.8:
            return f"Volatilidad normal (ATR {ratio:.1f}x)"
        else:
            return f"Volatilidad baja (ATR {ratio:.1f}x promedio)"
