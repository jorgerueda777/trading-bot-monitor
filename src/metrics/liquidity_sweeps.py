"""
Evaluador de Liquidity Sweeps
Analiza barridos de liquidez en múltiples timeframes
"""
from typing import Dict, Any, List
from .base_metric import MetricEvaluator


class LiquiditySweepsEvaluator(MetricEvaluator):
    """Evalúa Liquidity Sweeps"""
    
    TIMEFRAMES = ['15m', '30m', '1H', '4H']
    
    def evaluate(self, data: Dict[str, Any]) -> float:
        """
        Evalúa sweeps basado en:
        - Barridos recientes en diferentes timeframes
        - Relevancia de los extremos barridos
        
        Args:
            data: {
                'sweeps': {
                    '15m': bool,
                    '30m': bool,
                    '1H': bool,
                    '4H': bool
                },
                'sweep_quality': float (0-100),
                'time_since_last_sweep': float (horas)
            }
        """
        sweeps = data.get('sweeps', {})
        quality = data.get('sweep_quality', 50)
        time_since = data.get('time_since_last_sweep', 999)
        
        # Contar sweeps detectados
        sweep_count = sum(1 for tf in self.TIMEFRAMES if sweeps.get(tf, False))
        
        # Puntuación base por cantidad
        count_score = sweep_count * 15
        
        # Bonus por calidad del sweep
        quality_score = quality * 0.3
        
        # Penalización por tiempo transcurrido
        time_penalty = 0
        if time_since > 4:
            time_penalty = 20
        elif time_since > 2:
            time_penalty = 10
        
        total = count_score + quality_score - time_penalty
        return min(max(total, 0), 100.0)
    
    def get_analysis(self, data: Dict[str, Any]) -> str:
        """Genera análisis textual"""
        sweeps = data.get('sweeps', {})
        detected = [tf for tf in self.TIMEFRAMES if sweeps.get(tf, False)]
        
        if detected:
            return f"Liquidity sweeps: {', '.join(detected)}"
        return "Liquidity sweeps: ninguno reciente"
