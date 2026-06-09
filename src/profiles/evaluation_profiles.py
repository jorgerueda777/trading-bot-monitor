"""
Perfiles de evaluación por origen temporal
Define pesos de métricas según el timeframe
"""
from typing import Dict


class EvaluationProfile:
    """Perfil de pesos para evaluación de métricas"""
    
    def __init__(self, weights: Dict[str, int]):
        """
        Args:
            weights: Diccionario con pesos por métrica (suma debe ser 100)
        """
        if sum(weights.values()) != 100:
            raise ValueError("La suma de pesos debe ser 100")
        self.weights = weights
    
    def get_weight(self, metric: str) -> int:
        """Obtiene el peso de una métrica"""
        return self.weights.get(metric, 0)


# Perfiles predefinidos
PROFILES = {
    'FIBO_1H': EvaluationProfile({
        'open_interest': 25,
        'cvd': 25,
        'delta': 20,
        'volume': 15,
        'liquidity_sweeps': 10,
        'funding': 3,
        'vwap': 2
    }),
    
    'FIBO_4H': EvaluationProfile({
        'open_interest': 25,
        'cvd': 20,
        'delta': 15,
        'volume': 15,
        'liquidity_sweeps': 15,
        'funding': 5,
        'vwap': 5
    }),
    
    'FIBO_1D': EvaluationProfile({
        'open_interest': 20,
        'cvd': 15,
        'delta': 10,
        'volume': 15,
        'liquidity_sweeps': 25,
        'funding': 10,
        'vwap': 5
    }),
    
    'VOLUMEN': EvaluationProfile({
        'open_interest': 25,
        'cvd': 25,
        'delta': 20,
        'order_book': 10,
        'liquidity_sweeps': 10,
        'momentum_decay': 5,
        'funding': 3,
        'vwap': 2
    })
}


def get_profile(origin: str) -> EvaluationProfile:
    """Obtiene el perfil de evaluación para un origen"""
    return PROFILES.get(origin, PROFILES['FIBO_4H'])


class PriorityLevel:
    """
    Niveles de prioridad según puntuación
    
    NUEVA ESCALA (Motor v2.0):
    - ALTA PRIORIDAD: Score >= 75 (umbral unificado FIBO y VOLUMEN)
    - FUERTE: Score 60-74
    - INTERESANTE: Score 50-59
    - RUIDO: Score < 50
    """
    
    # Estados principales
    ALTA = "🚀 ALTA PRIORIDAD"
    FUERTE = "💪 FUERTE"
    INTERESANTE = "👀 INTERESANTE"
    RUIDO = "📉 RUIDO"
    
    # Legacy (mantener compatibilidad temporal)
    MEDIA = "PRIORIDAD MEDIA"
    BAJA = "BAJA PRIORIDAD"
    
    @staticmethod
    def from_score(score: float) -> str:
        """
        Determina el nivel de prioridad según la puntuación
        
        NUEVA ESCALA (Motor v2.0):
        - >= 75: ALTA PRIORIDAD (ejecutar)
        - 60-74: FUERTE (observar con interés)
        - 50-59: INTERESANTE (monitorear)
        - < 50: RUIDO (descartar)
        """
        if score >= 75:
            return PriorityLevel.ALTA
        elif score >= 60:
            return PriorityLevel.FUERTE
        elif score >= 50:
            return PriorityLevel.INTERESANTE
        else:
            return PriorityLevel.RUIDO
