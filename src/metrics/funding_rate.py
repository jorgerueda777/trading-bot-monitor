"""
Evaluador de Funding Rate
Analiza nivel actual, desviación y extremos
"""
from typing import Dict, Any
from .base_metric import MetricEvaluator


class FundingRateEvaluator(MetricEvaluator):
    """Evalúa Funding Rate"""
    
    def evaluate(self, data: Dict[str, Any]) -> float:
        """
        Evalúa FR basado en:
        - Nivel actual
        - Desviación respecto a media
        - Extremos estadísticos
        
        Args:
            data: {
                'current': float,
                'mean': float,
                'std_dev': float,
                'is_extreme': bool
            }
        """
        current = data.get('current', 0)
        mean = data.get('mean', 0)
        std_dev = data.get('std_dev', 0.01)
        is_extreme = data.get('is_extreme', False)
        
        # Calcular desviación en términos de std
        z_score = abs((current - mean) / std_dev) if std_dev > 0 else 0
        
        # Puntuación base por desviación
        deviation_score = min(z_score * 20, 50)
        
        # Bonus por extremo estadístico
        extreme_bonus = 30 if is_extreme else 0
        
        # Penalización si está muy cerca de la media (poco informativo)
        if z_score < 0.5:
            return 20.0
        
        total = deviation_score + extreme_bonus + 20
        return min(total, 100.0)
    
    def get_analysis(self, data: Dict[str, Any]) -> str:
        """Genera análisis textual"""
        current = data.get('current', 0)
        is_extreme = data.get('is_extreme', False)
        
        status = "extremo" if is_extreme else "normal"
        return f"FR {current:.4f}% ({status})"
