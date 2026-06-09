"""
Clase base para métricas de evaluación
"""
from abc import ABC, abstractmethod
from typing import Dict, Any


class MetricEvaluator(ABC):
    """Interfaz base para evaluadores de métricas"""
    
    @abstractmethod
    def evaluate(self, data: Dict[str, Any]) -> float:
        """
        Evalúa la métrica y retorna una puntuación 0-100
        
        Args:
            data: Datos necesarios para la evaluación
            
        Returns:
            Puntuación de 0 a 100
        """
        pass
    
    @abstractmethod
    def get_analysis(self, data: Dict[str, Any]) -> str:
        """
        Retorna análisis textual de la métrica
        
        Args:
            data: Datos de la métrica
            
        Returns:
            Descripción del análisis
        """
        pass
