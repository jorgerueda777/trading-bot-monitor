"""
Validador temporal de eventos
Determina si un evento sigue vigente según precio y tiempo
"""
from enum import Enum
from typing import Dict
from datetime import datetime, timedelta


class EventStatus(Enum):
    """Estados de vigencia de un evento"""
    VIGENTE = "VIGENTE"
    PARCIALMENTE_VIGENTE = "PARCIALMENTE_VIGENTE"
    EXPIRADO = "EXPIRADO"


class TemporalValidator:
    """Evalúa la vigencia temporal de eventos"""
    
    # Configuración de ventanas temporales por origen
    VALIDITY_WINDOWS = {
        'FIBO_1H': timedelta(hours=4),
        'FIBO_4H': timedelta(hours=16),
        'FIBO_1D': timedelta(days=3)
    }
    
    # Distancia máxima permitida (% respecto a zona principal)
    MAX_DISTANCE_PERCENT = {
        'FIBO_1H': 2.0,   # 2% para 1H
        'FIBO_4H': 5.0,   # 5% para 4H
        'FIBO_1D': 10.0   # 10% para 1D
    }
    
    def validate(
        self,
        origin: str,
        zone_a: float,
        zone_b: float,
        current_price: float,
        event_timestamp: datetime
    ) -> EventStatus:
        """
        Determina el estado de vigencia del evento
        
        Args:
            origin: Origen temporal del evento
            zone_a: Precio de zona A
            zone_b: Precio de zona B
            current_price: Precio actual del mercado
            event_timestamp: Timestamp de generación del evento
            
        Returns:
            Estado de vigencia
        """
        # Validar tiempo transcurrido
        time_valid = self._is_time_valid(origin, event_timestamp)
        
        # Validar distancia al precio
        distance_valid = self._is_distance_valid(
            origin, zone_a, zone_b, current_price
        )
        
        # Determinar estado
        if time_valid and distance_valid:
            return EventStatus.VIGENTE
        elif time_valid or distance_valid:
            return EventStatus.PARCIALMENTE_VIGENTE
        else:
            return EventStatus.EXPIRADO
    
    def _is_time_valid(self, origin: str, event_timestamp: datetime) -> bool:
        """Verifica si el evento está dentro de la ventana temporal"""
        validity_window = self.VALIDITY_WINDOWS.get(origin, timedelta(hours=1))
        elapsed = datetime.now() - event_timestamp
        return elapsed <= validity_window
    
    def _is_distance_valid(
        self,
        origin: str,
        zone_a: float,
        zone_b: float,
        current_price: float
    ) -> bool:
        """Verifica si el precio actual está cerca de la zona"""
        zone_center = (zone_a + zone_b) / 2
        distance_percent = abs(current_price - zone_center) / zone_center * 100
        
        max_distance = self.MAX_DISTANCE_PERCENT.get(origin, 5.0)
        return distance_percent <= max_distance
    
    def get_distance_score(
        self,
        origin: str,
        zone_a: float,
        zone_b: float,
        current_price: float
    ) -> float:
        """
        Calcula puntuación basada en distancia (0-100)
        100 = precio dentro de la zona
        0 = precio muy alejado
        """
        zone_min = min(zone_a, zone_b)
        zone_max = max(zone_a, zone_b)
        
        # Si está dentro de la zona: 100
        if zone_min <= current_price <= zone_max:
            return 100.0
        
        # Calcular distancia porcentual
        zone_center = (zone_a + zone_b) / 2
        distance_percent = abs(current_price - zone_center) / zone_center * 100
        
        max_distance = self.MAX_DISTANCE_PERCENT.get(origin, 5.0)
        
        # Normalizar: a mayor distancia, menor puntuación
        if distance_percent >= max_distance:
            return 0.0
        
        return 100.0 * (1 - distance_percent / max_distance)
