"""
Evaluador de Delta
Analiza intensidad compradora/vendedora y cambios bruscos
"""
from typing import Dict, Any
from .base_metric import MetricEvaluator


class DeltaEvaluator(MetricEvaluator):
    """Evalúa Delta"""
    
    def evaluate(self, data: Dict[str, Any]) -> float:
        """
        Evalúa Delta basado en:
        - Intensidad compradora
        - Intensidad vendedora
        - Cambios bruscos
        
        Args:
            data: {
                'current': float,
                'buyer_intensity': float (0-100),
                'seller_intensity': float (0-100),
                'has_sharp_change': bool,
                'bias': str ('BULLISH', 'BEARISH')
            }
        """
        buyer_intensity = data.get('buyer_intensity', 50)
        seller_intensity = data.get('seller_intensity', 50)
        sharp_change = data.get('has_sharp_change', False)
        bias = data.get('bias', 'BULLISH')
        
        # Determinar dominancia
        if bias == 'BULLISH':
            dominance_score = min(buyer_intensity, 50)
        else:
            dominance_score = min(seller_intensity, 50)
        
        # Bonus por cambio brusco (indica movimiento fuerte)
        sharp_bonus = 30 if sharp_change else 0
        
        # Balance score
        balance = abs(buyer_intensity - seller_intensity)
        balance_score = min(balance * 0.3, 20)
        
        total = dominance_score + sharp_bonus + balance_score
        return min(total, 100.0)
    
    def get_analysis(self, data: Dict[str, Any]) -> str:
        """Genera análisis textual"""
        buyer = data.get('buyer_intensity', 50)
        seller = data.get('seller_intensity', 50)
        
        if buyer > seller + 20:
            return f"Delta: dominancia compradora ({buyer:.0f}%)"
        elif seller > buyer + 20:
            return f"Delta: dominancia vendedora ({seller:.0f}%)"
        return "Delta: equilibrado"
