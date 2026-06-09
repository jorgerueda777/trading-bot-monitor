"""
Clasificador principal de eventos
Coordina parser, validador, métricas y scoring
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel

from .parser import EventParser, ParsedEvent
from .validator import TemporalValidator, EventStatus
from ..profiles.evaluation_profiles import get_profile, PriorityLevel
from ..metrics.open_interest import OpenInterestEvaluator
from ..metrics.funding_rate import FundingRateEvaluator
from ..metrics.cvd import CVDEvaluator
from ..metrics.delta import DeltaEvaluator
from ..metrics.volume import VolumeEvaluator
from ..metrics.liquidity_sweeps import LiquiditySweepsEvaluator
from ..metrics.vwap import VWAPEvaluator
from ..metrics.atr import ATREvaluator
from ..metrics.order_book import OrderBookEvaluator
from ..metrics.momentum_decay import MomentumDecayEvaluator


class MetricScore(BaseModel):
    """Puntuación de una métrica individual"""
    name: str
    score: float
    weight: int
    weighted_score: float
    analysis: str


class EventClassification(BaseModel):
    """Resultado completo de clasificación"""
    symbol: str
    bias: str
    origin: str
    status: str
    event_type: Optional[str] = None  # SOBRECOMPRA, SOBREVENTA (para VOLUMEN)
    
    # Zonas de entrada (crítico para tracking)
    zone_a: float = 0.0  # Entrada 1
    zone_b: float = 0.0  # Entrada 2
    target_a: float = 0.0  # TP 1
    target_b: float = 0.0  # TP 2
    stop_loss: float = 0.0  # Stop Loss
    
    # Scores por métrica
    open_interest: MetricScore
    funding: MetricScore
    cvd: MetricScore
    delta: MetricScore
    volume: Optional[MetricScore] = None  # Solo para FIBO
    liquidity_sweeps: MetricScore
    vwap: MetricScore
    atr: Optional[MetricScore] = None  # Ya no se usa (legacy)
    order_book: Optional[MetricScore] = None  # Solo para VOLUMEN
    momentum_decay: Optional[MetricScore] = None  # Solo para VOLUMEN
    
    # Score final
    final_score: float
    priority: str
    
    # Factores principales
    key_factors: List[str]
    
    # Timestamp
    evaluated_at: datetime


class EventClassifier:
    """Motor de clasificación de eventos"""
    
    def __init__(self):
        self.parser = EventParser()
        self.validator = TemporalValidator()
        
        # Inicializar evaluadores de métricas
        self.evaluators = {
            'open_interest': OpenInterestEvaluator(),
            'funding': FundingRateEvaluator(),
            'cvd': CVDEvaluator(),
            'delta': DeltaEvaluator(),
            'volume': VolumeEvaluator(),
            'liquidity_sweeps': LiquiditySweepsEvaluator(),
            'vwap': VWAPEvaluator(),
            'atr': ATREvaluator(),
            'order_book': OrderBookEvaluator(),
            'momentum_decay': MomentumDecayEvaluator()
        }
    
    def classify_event(
        self,
        event_text: str,
        market_data: Dict[str, Any],
        event_timestamp: datetime = None
    ) -> EventClassification:
        """
        Clasifica un evento completo
        
        Args:
            event_text: Texto del evento a clasificar
            market_data: Datos de mercado actuales
            event_timestamp: Timestamp del evento (default: now)
        
        Returns:
            Clasificación completa del evento
        """
        # Paso 1: Parsear evento
        parsed = self.parser.parse(event_text)
        
        # Paso 2: Validar vigencia temporal
        if event_timestamp is None:
            event_timestamp = datetime.now()
        
        status = self.validator.validate(
            parsed.origin,
            parsed.zone_a,
            parsed.zone_b,
            market_data['current_price'],
            event_timestamp
        )
        
        # Paso 3: Obtener perfil de evaluación
        profile = get_profile(parsed.origin)
        
        # Paso 4: Evaluar todas las métricas
        metric_scores = self._evaluate_metrics(
            parsed,
            market_data,
            profile
        )
        
        # Paso 5: Calcular score final
        final_score = sum(m.weighted_score for m in metric_scores.values())
        
        # Paso 6: Determinar prioridad
        priority = PriorityLevel.from_score(final_score)
        
        # Paso 7: Identificar factores clave
        key_factors = self._identify_key_factors(metric_scores)
        
        return EventClassification(
            symbol=parsed.symbol,
            bias=parsed.bias,
            origin=parsed.origin,
            status=status.value,
            event_type=parsed.event_type,
            zone_a=parsed.zone_a,  # Entrada 1
            zone_b=parsed.zone_b,  # Entrada 2
            target_a=parsed.target_a,  # TP 1
            target_b=parsed.target_b,  # TP 2
            stop_loss=parsed.stop_loss,  # Stop Loss
            open_interest=metric_scores['open_interest'],
            funding=metric_scores['funding'],
            cvd=metric_scores['cvd'],
            delta=metric_scores['delta'],
            volume=metric_scores.get('volume'),
            liquidity_sweeps=metric_scores['liquidity_sweeps'],
            vwap=metric_scores['vwap'],
            atr=metric_scores.get('atr'),  # Legacy
            order_book=metric_scores.get('order_book'),
            momentum_decay=metric_scores.get('momentum_decay'),
            final_score=round(final_score, 2),
            priority=priority,
            key_factors=key_factors,
            evaluated_at=datetime.now()
        )
    
    def _evaluate_metrics(
        self,
        parsed: ParsedEvent,
        market_data: Dict[str, Any],
        profile
    ) -> Dict[str, MetricScore]:
        """Evalúa todas las métricas según el perfil"""
        scores = {}
        
        for metric_name, evaluator in self.evaluators.items():
            # Obtener datos específicos de la métrica
            metric_data = market_data.get(metric_name, {})
            
            # Agregar contexto del evento
            metric_data['bias'] = parsed.bias
            
            # Evaluar
            raw_score = evaluator.evaluate(metric_data)
            weight = profile.get_weight(metric_name)
            weighted = (raw_score * weight) / 100
            analysis = evaluator.get_analysis(metric_data)
            
            scores[metric_name] = MetricScore(
                name=metric_name.replace('_', ' ').title(),
                score=round(raw_score, 2),
                weight=weight,
                weighted_score=round(weighted, 2),
                analysis=analysis
            )
        
        return scores
    
    def _identify_key_factors(
        self,
        metric_scores: Dict[str, MetricScore]
    ) -> List[str]:
        """
        Identifica los factores más influyentes
        Retorna los top 3 por weighted_score
        """
        sorted_metrics = sorted(
            metric_scores.values(),
            key=lambda x: x.weighted_score,
            reverse=True
        )
        
        return [
            f"{m.name}: {m.analysis} (peso: {m.weighted_score:.1f})"
            for m in sorted_metrics[:3]
        ]
    
    def format_output(self, classification: EventClassification) -> str:
        """Formatea la clasificación en texto legible"""
        lines = [
            "=" * 60,
            "EVALUACIÓN DE EVENTO",
            "=" * 60,
            f"Símbolo: {classification.symbol}",
            f"Sesgo: {classification.bias}",
            f"Origen: {classification.origin}",
            f"Estado de vigencia: {classification.status}",
            "",
            "MÉTRICAS EVALUADAS:",
            "-" * 60,
            f"Open Interest: {classification.open_interest.score:.1f}/100 (peso: {classification.open_interest.weight}%)",
            f"  {classification.open_interest.analysis}",
            f"Funding: {classification.funding.score:.1f}/100 (peso: {classification.funding.weight}%)",
            f"  {classification.funding.analysis}",
            f"CVD: {classification.cvd.score:.1f}/100 (peso: {classification.cvd.weight}%)",
            f"  {classification.cvd.analysis}",
            f"Delta: {classification.delta.score:.1f}/100 (peso: {classification.delta.weight}%)",
            f"  {classification.delta.analysis}",
            f"Volumen: {classification.volume.score:.1f}/100 (peso: {classification.volume.weight}%)",
            f"  {classification.volume.analysis}",
            f"Liquidity Sweeps: {classification.liquidity_sweeps.score:.1f}/100 (peso: {classification.liquidity_sweeps.weight}%)",
            f"  {classification.liquidity_sweeps.analysis}",
            f"VWAP: {classification.vwap.score:.1f}/100 (peso: {classification.vwap.weight}%)",
            f"  {classification.vwap.analysis}",
            "",
            "=" * 60,
            f"Puntuación Final: {classification.final_score:.2f}/100",
            f"Clasificación: {classification.priority}",
            "=" * 60,
            "",
            "Factores principales que influyeron en la clasificación:",
        ]
        
        for i, factor in enumerate(classification.key_factors, 1):
            lines.append(f"{i}. {factor}")
        
        lines.extend([
            "",
            f"Evaluado: {classification.evaluated_at.strftime('%Y-%m-%d %H:%M:%S')}",
            "=" * 60
        ])
        
        return "\n".join(lines)
