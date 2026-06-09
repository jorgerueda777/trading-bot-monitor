"""
Almacenamiento histórico de clasificaciones
Permite análisis retrospectivo y recalibración
"""
import json
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path


class HistoricalStorage:
    """Gestor de almacenamiento histórico"""
    
    def __init__(self, storage_path: str = "data/classifications"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
    
    def save_classification(
        self,
        classification: Dict[str, Any],
        actual_outcome: Dict[str, Any] = None
    ):
        """
        Guarda una clasificación con su outcome real (si está disponible)
        
        Args:
            classification: Resultado de la clasificación
            actual_outcome: Resultado real del evento (para calibración)
                {
                    'reached_target': bool,
                    'max_favorable_move': float,
                    'time_to_target': float (horas),
                    'drawdown': float
                }
        """
        # Convertir datetime a string para serialización JSON
        if 'evaluated_at' in classification and hasattr(classification['evaluated_at'], 'isoformat'):
            classification['evaluated_at'] = classification['evaluated_at'].isoformat()
        
        record = {
            'timestamp': datetime.now().isoformat(),
            'classification': classification,
            'outcome': actual_outcome
        }
        
        # Guardar en archivo diario
        date_str = datetime.now().strftime('%Y-%m-%d')
        file_path = self.storage_path / f"classifications_{date_str}.jsonl"
        
        with open(file_path, 'a') as f:
            f.write(json.dumps(record) + '\n')
    
    def load_historical_data(
        self,
        start_date: datetime = None,
        end_date: datetime = None
    ) -> List[Dict[str, Any]]:
        """Carga datos históricos en un rango de fechas"""
        records = []
        
        for file_path in sorted(self.storage_path.glob("classifications_*.jsonl")):
            with open(file_path, 'r') as f:
                for line in f:
                    record = json.loads(line)
                    records.append(record)
        
        return records
    
    def calculate_accuracy_by_priority(self) -> Dict[str, float]:
        """
        Calcula precisión por nivel de prioridad
        Útil para recalibración de umbrales
        """
        records = self.load_historical_data()
        
        stats = {
            'ALTA PRIORIDAD': {'total': 0, 'success': 0},
            'PRIORIDAD MEDIA': {'total': 0, 'success': 0},
            'BAJA PRIORIDAD': {'total': 0, 'success': 0}
        }
        
        for record in records:
            if record.get('outcome'):
                priority = record['classification']['priority']
                stats[priority]['total'] += 1
                
                if record['outcome'].get('reached_target'):
                    stats[priority]['success'] += 1
        
        # Calcular tasas de éxito
        accuracy = {}
        for priority, data in stats.items():
            if data['total'] > 0:
                accuracy[priority] = data['success'] / data['total']
            else:
                accuracy[priority] = 0.0
        
        return accuracy
    
    def suggest_weight_adjustments(self) -> Dict[str, float]:
        """
        Sugiere ajustes de pesos basados en datos históricos
        Analiza correlación entre scores de métricas y outcomes exitosos
        """
        records = self.load_historical_data()
        
        # Acumular scores de métricas por outcome
        successful = {metric: [] for metric in [
            'open_interest', 'funding', 'cvd', 'delta', 
            'volume', 'liquidity_sweeps', 'vwap'
        ]}
        
        failed = {metric: [] for metric in successful.keys()}
        
        for record in records:
            if record.get('outcome'):
                classification = record['classification']
                target = successful if record['outcome']['reached_target'] else failed
                
                for metric in successful.keys():
                    score = classification.get(metric, {}).get('score', 0)
                    target[metric].append(score)
        
        # Calcular diferencias promedio
        suggestions = {}
        for metric in successful.keys():
            if successful[metric] and failed[metric]:
                avg_success = sum(successful[metric]) / len(successful[metric])
                avg_fail = sum(failed[metric]) / len(failed[metric])
                
                # Diferencia normalizada
                diff = (avg_success - avg_fail) / 100
                suggestions[metric] = diff
        
        return suggestions
