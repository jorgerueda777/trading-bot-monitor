"""
Evaluador de Volumen Relativo
Compara volumen actual vs promedio de 20 períodos
"""
from typing import Dict, Any
from .base_metric import MetricEvaluator


class VolumeEvaluator(MetricEvaluator):
    """Evalúa Volumen Relativo"""
    
    def evaluate(self, data: Dict[str, Any]) -> float:
        """
        Evalúa volumen basado en:
        - Comparación con promedio de 20 períodos
        - Detección de actividad anómala
        
        Args:
            data: {
                'current': float,
                'avg_20': float,
                'is_anomaly': bool
            }
        """
        current = data.get('current', 0)
        avg_20 = data.get('avg_20', 1)
        is_anomaly = data.get('is_anomaly', False)
        
        if avg_20 == 0:
            return 50.0
        
        # Calcular ratio respecto al promedio
        ratio = current / avg_20
        
        # Puntuación base por ratio
        if ratio < 0.8:
            # Volumen bajo
            score = 20
        elif ratio < 1.2:
            # Volumen normal
            score = 50
        elif ratio < 2.0:
            # Volumen alto
            score = 75
        else:
            # Volumen muy alto
            score = 90
        
        # Bonus por anomalía detectada
        if is_anomaly:
            score = min(score + 10, 100)
        
        return float(score)
    
    def get_analysis(self, data: Dict[str, Any]) -> str:
        """Genera análisis textual"""
        current = data.get('current', 0)
        avg_20 = data.get('avg_20', 1)
        
        if avg_20 > 0:
            ratio = current / avg_20
            if ratio > 2.0:
                return f"Volumen: {ratio:.1f}x promedio (muy alto)"
            elif ratio > 1.2:
                return f"Volumen: {ratio:.1f}x promedio (alto)"
            elif ratio < 0.8:
                return f"Volumen: {ratio:.1f}x promedio (bajo)"
        
        return "Volumen: normal"
