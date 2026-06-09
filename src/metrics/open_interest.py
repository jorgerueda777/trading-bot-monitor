"""
Evaluador de Open Interest
Analiza variación, tendencia e intensidad
"""
from typing import Dict, Any
from .base_metric import MetricEvaluator


class OpenInterestEvaluator(MetricEvaluator):
    """Evalúa Open Interest"""
    
    def evaluate(self, data: Dict[str, Any]) -> float:
        """
        Evalúa OI basado en:
        - Variación porcentual
        - Tendencia reciente
        - Intensidad del cambio
        
        Args:
            data: {
                'current': float,
                'previous': float,
                'trend': str ('INCREASING', 'DECREASING', 'STABLE'),
                'change_intensity': float (0-100)
            }
        """
        current = data.get('current', 0)
        previous = data.get('previous', 0)
        trend = data.get('trend', 'STABLE')
        intensity = data.get('change_intensity', 0)
        
        if previous == 0:
            return 50.0
        
        # Calcular variación porcentual
        change_pct = ((current - previous) / previous) * 100
        
        # Puntuación base por variación
        variation_score = min(abs(change_pct) * 10, 40)
        
        # Bonus por tendencia alcista con sesgo alcista
        trend_score = 30 if trend == 'INCREASING' else 15
        
        # Intensidad del cambio
        intensity_score = min(intensity * 0.3, 30)
        
        total = variation_score + trend_score + intensity_score
        return min(total, 100.0)
    
    def get_analysis(self, data: Dict[str, Any]) -> str:
        """Genera análisis textual"""
        current = data.get('current', 0)
        previous = data.get('previous', 0)
        trend = data.get('trend', 'STABLE')
        
        if previous > 0:
            change = ((current - previous) / previous) * 100
            return f"OI {trend.lower()}, variación: {change:+.2f}%"
        return f"OI {trend.lower()}"
