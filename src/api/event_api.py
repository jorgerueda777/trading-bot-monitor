"""
API REST para clasificación de eventos
FastAPI para integración con sistemas externos
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime

from ..core.classifier import EventClassifier
from ..storage.historical_storage import HistoricalStorage


app = FastAPI(
    title="Motor de Clasificación de Eventos",
    description="API para clasificar eventos de mercado según relevancia",
    version="1.0.0"
)

classifier = EventClassifier()
storage = HistoricalStorage()


class EventRequest(BaseModel):
    """Petición de clasificación"""
    event_text: str
    market_data: Dict[str, Any]
    event_timestamp: Optional[str] = None


class OutcomeUpdate(BaseModel):
    """Actualización de outcome real"""
    classification_id: str
    reached_target: bool
    max_favorable_move: float
    time_to_target: float
    drawdown: float


@app.post("/classify")
async def classify_event(request: EventRequest):
    """
    Clasifica un evento de mercado
    
    Retorna clasificación completa con score y prioridad
    """
    try:
        # Parsear timestamp si está presente
        timestamp = None
        if request.event_timestamp:
            timestamp = datetime.fromisoformat(request.event_timestamp)
        
        # Clasificar
        classification = classifier.classify_event(
            request.event_text,
            request.market_data,
            timestamp
        )
        
        # Guardar en histórico
        storage.save_classification(classification.model_dump())
        
        return classification.model_dump()
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/outcome")
async def update_outcome(outcome: OutcomeUpdate):
    """
    Actualiza el outcome real de un evento clasificado
    Usado para recalibración del sistema
    """
    try:
        # Aquí se implementaría la lógica para actualizar el registro
        # Por ahora solo retornamos confirmación
        return {
            "status": "success",
            "message": "Outcome actualizado correctamente"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/statistics/accuracy")
async def get_accuracy_stats():
    """
    Obtiene estadísticas de precisión por prioridad
    """
    try:
        accuracy = storage.calculate_accuracy_by_priority()
        return accuracy
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/statistics/weight-suggestions")
async def get_weight_suggestions():
    """
    Obtiene sugerencias de ajuste de pesos
    Basado en análisis histórico
    """
    try:
        suggestions = storage.suggest_weight_adjustments()
        return suggestions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
