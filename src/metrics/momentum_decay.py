"""
Momentum Decay Evaluator
Detecta desaceleración y pérdida de impulso en temporalidad 1M
"""
from .base_metric import MetricEvaluator


class MomentumDecayEvaluator(MetricEvaluator):
    """Evalúa la pérdida de momentum"""
    
    def evaluate(self, data: dict) -> float:
        """
        Evalúa si el momentum está decayendo
        
        Args:
            data: {
                'price_changes': list,  # [+1.2, +0.8, +0.4, +0.1] últimos movimientos
                'velocity': float,  # Velocidad actual del movimiento
                'acceleration': float,  # Aceleración (positiva o negativa)
                'bias': str  # BULLISH o BEARISH
            }
        
        Returns:
            Score 0-100 (100 = decay fuerte, favorece reversión)
        """
        price_changes = data.get('price_changes', [])
        velocity = data.get('velocity', 0)
        acceleration = data.get('acceleration', 0)
        bias = data.get('bias', 'BULLISH')
        
        if len(price_changes) < 3:
            return 50  # Sin datos suficientes
        
        score = 50
        
        # Analizar si hay desaceleración progresiva
        is_decaying = self._detect_decay(price_changes, bias)
        
        if is_decaying:
            score += 40
        
        # Aceleración negativa (desacelerando)
        if acceleration < -0.1:
            score += 10
        elif acceleration < 0:
            score += 5
        
        # Velocidad muy baja
        if abs(velocity) < 0.1:
            score += 10
        
        return max(0, min(100, score))
    
    def _detect_decay(self, price_changes: list, bias: str) -> bool:
        """Detecta si hay un patrón de decay en los cambios de precio"""
        if len(price_changes) < 3:
            return False
        
        # Para BEARISH: buscamos que la caída se desacelere
        # Ejemplo: -1.2%, -0.8%, -0.4% (cada vez cae menos)
        if bias == 'BEARISH':
            # Verificar que los valores absolutos disminuyen
            for i in range(len(price_changes) - 1):
                if abs(price_changes[i]) < abs(price_changes[i + 1]):
                    return False  # No hay decay
            return True
        
        # Para BULLISH: buscamos que la subida se desacelere
        # Ejemplo: +1.2%, +0.8%, +0.4% (cada vez sube menos)
        else:
            for i in range(len(price_changes) - 1):
                if abs(price_changes[i]) < abs(price_changes[i + 1]):
                    return False
            return True
    
    def get_analysis(self, data: dict) -> str:
        """Genera análisis descriptivo"""
        price_changes = data.get('price_changes', [])
        acceleration = data.get('acceleration', 0)
        bias = data.get('bias', 'BULLISH')
        
        if len(price_changes) < 3:
            return "Datos insuficientes para evaluar momentum"
        
        is_decaying = self._detect_decay(price_changes, bias)
        
        if is_decaying and acceleration < 0:
            return "Momentum decayendo (agotamiento detectado)"
        elif is_decaying:
            return "Desaceleración progresiva del movimiento"
        elif acceleration < -0.1:
            return "Aceleración negativa (perdiendo fuerza)"
        else:
            return "Momentum manteniéndose o acelerando"
