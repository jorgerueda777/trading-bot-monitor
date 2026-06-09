"""
Evaluador de Cumulative Volume Delta (CVD)
Analiza divergencias, cambios de pendiente y agotamiento
"""
from typing import Dict, Any
from .base_metric import MetricEvaluator


class CVDEvaluator(MetricEvaluator):
    """Evalúa CVD"""
    
    def evaluate(self, data: Dict[str, Any]) -> float:
        """
        Evalúa CVD basado en:
        - Divergencias con precio
        - Cambios de pendiente
        - Señales de agotamiento
        
        Args:
            data: {
                'has_divergence': bool,
                'slope_change': str ('POSITIVE_TO_NEGATIVE', 'NEGATIVE_TO_POSITIVE', 'STABLE'),
                'exhaustion_signal': bool,
                'alignment_with_bias': bool
            }
        """
        has_divergence = data.get('has_divergence', False)
        slope_change = data.get('slope_change', 'STABLE')
        exhaustion = data.get('exhaustion_signal', False)
        alignment = data.get('alignment_with_bias', True)
        
        score = 0
        
        # Divergencia es señal fuerte
        if has_divergence:
            score += 40
        
        # Cambio de pendiente favorable
        if slope_change == 'NEGATIVE_TO_POSITIVE':
            score += 30
        elif slope_change == 'POSITIVE_TO_NEGATIVE':
            score += 15
        
        # Alineación con sesgo del evento
        if alignment:
            score += 20
        
        # Señal de agotamiento
        if exhaustion:
            score += 10
        
        return min(score, 100.0)
    
    def get_analysis(self, data: Dict[str, Any]) -> str:
        """Genera análisis textual"""
        has_div = data.get('has_divergence', False)
        slope = data.get('slope_change', 'STABLE')
        
        parts = []
        if has_div:
            parts.append("divergencia detectada")
        if slope != 'STABLE':
            parts.append(f"cambio de pendiente")
        
        return "CVD: " + (", ".join(parts) if parts else "estable")
