"""
Sistema de Seguimiento de Eventos
Monitorea eventos cada 30 segundos para decidir si ejecutar o descartar
"""
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum

from src.core.classifier import EventClassifier
from src.data_sources.binance_client import BinanceClient


class EventStatus(Enum):
    """Estados posibles de un evento"""
    EN_ANALISIS = "🔄 EN ANÁLISIS"
    ALTA_PRIORIDAD = "🚀 ALTA PRIORIDAD"  # Score >= 75
    FUERTE = "💪 FUERTE"  # Score 60-74
    INTERESANTE = "👀 INTERESANTE"  # Score 50-59
    RUIDO = "📉 RUIDO"  # Score < 50
    ENTRADA_EXPIRADA = "⏰ ENTRADA EXPIRADA"
    INVALIDADA = "❌ INVALIDADA"


@dataclass
class TrackedEvent:
    """Evento en seguimiento"""
    event_id: str
    symbol: str
    bias: str  # BULLISH/BEARISH
    original_message: str
    market_data_inicial: dict
    status: EventStatus
    score_inicial: float
    created_at: datetime
    last_check: datetime
    check_count: int = 0
    scores_historico: List[float] = field(default_factory=list)
    score_maximo: float = 0.0  # Score máximo alcanzado
    tendencia: str = "ESTABLE"  # MEJORANDO, ESTABLE, DETERIORÁNDOSE
    max_checks: int = 10  # Variable según origen y score
    tiempo_maximo: int = 300  # Segundos máximos (variable según origen)
    tiempo_minimo: int = 0  # Segundos mínimos obligatorios
    origin: str = "FIBO_4H"  # FIBO_1H, FIBO_4H, FIBO_1D, VOLUMEN
    entry_price: float = 0.0  # Precio de entrada sugerido
    current_price: float = 0.0  # Precio actual
    distance_to_entry: float = 0.0  # Distancia % al precio de entrada


class EventTracker:
    """Gestor de seguimiento de eventos"""
    
    def __init__(self):
        self.classifier = EventClassifier()
        self.binance_client = BinanceClient()
        self.eventos_activos: Dict[str, TrackedEvent] = {}
        self.running = False
    
    def agregar_evento(self, event_id: str, symbol: str, bias: str, 
                      original_message: str, market_data: dict, score: float,
                      origin: str = "FIBO_4H", entry_price: float = 0.0) -> TrackedEvent:
        """Agrega un nuevo evento al seguimiento"""
        
        # Inicializar variables
        tiempo_minimo = 0
        tiempo_maximo = 300
        max_checks = 10
        check_interval = 10  # Default para FIBO
        
        # NUEVA LÓGICA: Intervalos más rápidos (5seg VOLUMEN, 10seg FIBO)
        if origin == "VOLUMEN":
            check_interval = 5  # VOLUMEN: 5 segundos
            # Señales VOLUMEN: Tiempos según score inicial
            # Temporalidad: 1M - Observación con protección contra descarte prematuro
            
            if score < 50:
                # Score muy bajo: clasificar como RUIDO
                max_checks = 1
                tiempo_minimo = 0
                tiempo_maximo = 5
            elif score >= 60:
                # Score >= 60: OBSERVACIÓN EXTENDIDA OBLIGATORIA
                max_checks = 240  # 20 minutos (240 checks * 5seg)
                tiempo_minimo = 120  # 2 minutos mínimos obligatorios
                tiempo_maximo = 1200  # 20 minutos máximo
            elif score >= 50 and score < 60:
                # Score 50-59: INTERESANTE - observación estándar
                max_checks = 60  # 5 minutos (60 checks * 5seg)
                tiempo_minimo = 120  # 2 minutos mínimos obligatorios
                tiempo_maximo = 300
            else:
                # Fallback
                max_checks = 60
                tiempo_minimo = 120
                tiempo_maximo = 300
        else:
            check_interval = 10  # FIBONACCI: 10 segundos
            # SEÑALES FIBONACCI: Tiempos SIGNIFICATIVAMENTE MÁS AMPLIOS
            # Las zonas FIBO necesitan tiempo para atraer interés del mercado
            tiempo_minimo = 0  # Se define específicamente por origen
            
            if score >= 60:
                # Score >= 60: OBSERVACIÓN EXTENDIDA OBLIGATORIA (unificado para todos los FIBO)
                max_checks = 120  # 20 minutos (120 checks * 10seg)
                tiempo_maximo = 1200  # 20 minutos
                
                # Tiempo mínimo según origen FIBO
                if origin == "FIBO_1H":
                    tiempo_minimo = 300  # 5 minutos mínimos
                elif origin == "FIBO_4H":
                    tiempo_minimo = 420  # 7 minutos mínimos
                elif origin == "FIBO_1D":
                    tiempo_minimo = 600  # 10 minutos mínimos
                else:
                    tiempo_minimo = 420  # Default 7 minutos
            
            else:
                # Score < 60: Observación más corta
                if origin == "FIBO_1H":
                    max_checks = 30  # 5 minutos (30 checks * 10seg)
                    tiempo_minimo = 150  # 2.5 minutos mínimos
                    tiempo_maximo = 300
                elif origin == "FIBO_4H":
                    max_checks = 42  # 7 minutos (42 checks * 10seg)
                    tiempo_minimo = 240  # 4 minutos mínimos
                    tiempo_maximo = 420
                elif origin == "FIBO_1D":
                    max_checks = 60  # 10 minutos (60 checks * 10seg)
                    tiempo_minimo = 300  # 5 minutos mínimos
                    tiempo_maximo = 600
                else:
                    # Default FIBO_4H para casos no especificados
                    max_checks = 42
                    tiempo_minimo = 240
                    tiempo_maximo = 420
        
        # Precio de entrada - VALIDACIÓN CRÍTICA
        current_price = market_data.get('current_price', 0.0)
        
        # PROHIBIDO usar valores por defecto silenciosos
        if entry_price == 0.0:
            print(f"   ❌ ERROR CRÍTICO: entry_price es 0.0 para {symbol}")
            print(f"   ⚠️ El sistema NO debe usar precio actual como fallback")
            # Usar precio actual solo si realmente no se proporcionó entrada
            # pero marcar para revisión
            entry_price = current_price
            print(f"   ⚠️ FALLBACK: Usando precio actual ${current_price:.8f}")
        
        # Validación adicional: Detectar valores hardcodeados sospechosos
        if entry_price == 1.0:
            print(f"   ⚠️ WARNING: entry_price = 1.0 detectado para {symbol}")
            print(f"   ⚠️ Posible valor hardcodeado o error de parsing")
        
        evento = TrackedEvent(
            event_id=event_id,
            symbol=symbol,
            bias=bias,
            original_message=original_message,
            market_data_inicial=market_data,
            status=EventStatus.EN_ANALISIS,
            score_inicial=score,
            score_maximo=score,
            tendencia="ESTABLE",
            created_at=datetime.now(),
            last_check=datetime.now(),
            scores_historico=[score],
            max_checks=max_checks,
            tiempo_maximo=tiempo_maximo,
            tiempo_minimo=tiempo_minimo,
            origin=origin,
            entry_price=entry_price,
            current_price=current_price,
            distance_to_entry=0.0
        )
        
        # Guardar el intervalo de check como atributo del evento
        evento.check_interval = check_interval
        
        self.eventos_activos[event_id] = evento
        return evento
    
    def obtener_evento(self, event_id: str) -> Optional[TrackedEvent]:
        """Obtiene un evento por ID"""
        return self.eventos_activos.get(event_id)
    
    def remover_evento(self, event_id: str):
        """Remueve un evento del seguimiento"""
        if event_id in self.eventos_activos:
            del self.eventos_activos[event_id]
    
    async def check_evento(self, event_id: str) -> Optional[TrackedEvent]:
        """Revisa un evento y actualiza su estado - NUEVA LÓGICA CON UMBRAL 75"""
        
        evento = self.eventos_activos.get(event_id)
        if not evento:
            return None
        
        tiempo_transcurrido = (datetime.now() - evento.created_at).total_seconds()
        
        # Verificar si ya pasó el tiempo máximo (específico por origen)
        if tiempo_transcurrido > evento.tiempo_maximo:
            # Clasificar según score final
            score_final = evento.scores_historico[-1] if evento.scores_historico else evento.score_inicial
            evento.status = self._clasificar_por_score(score_final)
            return evento
        
        # Verificar si ya se hicieron todos los checks
        if evento.check_count >= evento.max_checks:
            # Clasificar según score final
            score_final = evento.scores_historico[-1] if evento.scores_historico else evento.score_inicial
            evento.status = self._clasificar_por_score(score_final)
            return evento
        
        try:
            # Obtener datos actualizados de mercado (ejecutar en thread pool para no bloquear)
            import asyncio
            loop = asyncio.get_event_loop()
            market_data = await loop.run_in_executor(
                None, 
                self.binance_client.get_market_data, 
                evento.symbol
            )
            
            # Re-clasificar el evento con datos actuales
            classification = self.classifier.classify_event(
                evento.original_message,
                market_data,
                datetime.now()
            )
            
            nuevo_score = classification.final_score
            evento.scores_historico.append(nuevo_score)
            evento.check_count += 1
            evento.last_check = datetime.now()
            
            # Actualizar score máximo
            if nuevo_score > evento.score_maximo:
                evento.score_maximo = nuevo_score
            
            # Actualizar precio actual y distancia a entrada
            evento.current_price = market_data.get('current_price', evento.current_price)
            evento.distance_to_entry = self._calcular_distancia_entrada(
                evento.entry_price,
                evento.current_price,
                evento.bias
            )
            
            # Debug info
            print(f"      📈 Score: {nuevo_score:.1f} (inicial: {evento.score_inicial:.1f}, máx: {evento.score_maximo:.1f})")
            
            # Calcular tendencia de scores
            tendencia_valor = self._calcular_tendencia(evento.scores_historico)
            score_promedio = sum(evento.scores_historico) / len(evento.scores_historico)
            
            # Actualizar tendencia textual
            if tendencia_valor > 2:
                evento.tendencia = "MEJORANDO"
            elif tendencia_valor < -2:
                evento.tendencia = "DETERIORÁNDOSE"
            else:
                evento.tendencia = "ESTABLE"
            
            print(f"      📊 Tendencia: {evento.tendencia} ({tendencia_valor:+.1f} pts/check), Promedio: {score_promedio:.1f}")
            print(f"      💰 Precio: ${evento.current_price:.4f}, Distancia entrada: {evento.distance_to_entry:+.2f}%")
            
            # VERIFICAR ENTRADA EXPIRADA (aplica a ambos perfiles)
            if abs(evento.distance_to_entry) > 3.0:  # Más de 3% de distancia
                print(f"      ⏰ Entrada expirada: {evento.distance_to_entry:+.2f}% de distancia")
                evento.status = EventStatus.ENTRADA_EXPIRADA
                return evento
            
            # NUEVA LÓGICA UNIFICADA: Umbral 75 para AMBOS perfiles
            print(f"      🔹 Evaluando con NUEVO umbral unificado: 75")
            
            # DECISIÓN: ALTA PRIORIDAD (Score >= 75)
            if nuevo_score >= 75:
                print(f"      ✅ Score >= 75 → ALTA PRIORIDAD")
                evento.status = EventStatus.ALTA_PRIORIDAD
                return evento
            
            # PROTECCIÓN: No clasificar antes del tiempo mínimo (excepto ALTA PRIORIDAD o ENTRADA_EXPIRADA)
            if tiempo_transcurrido < evento.tiempo_minimo:
                print(f"      ⏳ Aún en tiempo mínimo ({tiempo_transcurrido:.0f}s / {evento.tiempo_minimo}s)")
                evento.status = EventStatus.EN_ANALISIS
                return evento
            
            # DESPUÉS DEL TIEMPO MÍNIMO: Evaluar clasificación final
            # Score 60-74: FUERTE
            if 60 <= nuevo_score < 75:
                # Verificar si tendencia es positiva o estable
                if tendencia_valor >= -1:
                    print(f"      💪 Score 60-74 con tendencia estable/positiva → FUERTE")
                    evento.status = EventStatus.FUERTE
                else:
                    # Deterioro significativo
                    print(f"      📉 Deterioro significativo → clasificar según score actual")
                    evento.status = EventStatus.EN_ANALISIS
            
            # Score 50-59: INTERESANTE
            elif 50 <= nuevo_score < 60:
                print(f"      👀 Score 50-59 → INTERESANTE")
                evento.status = EventStatus.INTERESANTE
            
            # Score < 50: RUIDO
            elif nuevo_score < 50:
                print(f"      📉 Score < 50 → RUIDO")
                evento.status = EventStatus.RUIDO
            
            # INVALIDACIÓN EXTREMA (solo para FIBO)
            if evento.origin != "VOLUMEN" and self._es_invalidacion_extrema(evento, classification):
                print(f"      ⚠️ INVALIDACIÓN EXTREMA detectada")
                evento.status = EventStatus.INVALIDADA
            
            return evento
        
        except Exception as e:
            print(f"❌ Error revisando evento {event_id}: {e}")
            return evento
    
    def _clasificar_por_score(self, score: float) -> EventStatus:
        """Clasifica un evento basado en su score final"""
        if score >= 75:
            return EventStatus.ALTA_PRIORIDAD
        elif score >= 60:
            return EventStatus.FUERTE
        elif score >= 50:
            return EventStatus.INTERESANTE
        else:
            return EventStatus.RUIDO
    
    def _calcular_distancia_entrada(self, entry_price: float, current_price: float, bias: str) -> float:
        """
        Calcula distancia porcentual entre precio actual y entrada
        
        Fórmula: ((precio_actual - precio_entrada) / precio_entrada) * 100
        
        Para LONG:
        - Positivo: Precio subió (favorable)
        - Negativo: Precio bajó (desfavorable)
        
        Para SHORT:
        - Positivo: Precio bajó (favorable - invertimos signo)
        - Negativo: Precio subió (desfavorable - invertimos signo)
        """
        if entry_price == 0 or entry_price == 1.0:
            print(f"      ⚠️ WARNING: entry_price sospechoso = {entry_price}")
            return 0.0
        
        # Calcular distancia absoluta
        distancia_pct = ((current_price - entry_price) / entry_price) * 100
        
        # Log de cálculo para auditoría
        print(f"      📐 Cálculo distancia:")
        print(f"         Entry: ${entry_price:.8f}")
        print(f"         Current: ${current_price:.8f}")
        print(f"         Raw distance: {distancia_pct:+.4f}%")
        
        # Para SHORT, invertir el signo (precio sube = alejamiento = positivo)
        if bias.upper() in ["BEARISH", "BAJISTA", "SHORT"]:
            distancia_pct = -distancia_pct
            print(f"         Adjusted (SHORT): {distancia_pct:+.4f}%")
        
        return distancia_pct
    
    def _calcular_tendencia(self, scores: List[float]) -> float:
        """Calcula la tendencia de los scores (cambio promedio)"""
        if len(scores) < 2:
            return 0.0
        
        # Calcular cambio promedio entre checks consecutivos
        cambios = [scores[i] - scores[i-1] for i in range(1, len(scores))]
        return sum(cambios) / len(cambios) if cambios else 0.0
    
    def _es_invalidacion_extrema(self, evento: TrackedEvent, classification) -> bool:
        """
        Detecta si hay invalidación EXTREMA que justifica descarte antes del tiempo mínimo (solo FIBO)
        
        Ejemplos de invalidación extrema:
        - OI colapsa significativamente
        - CVD se deteriora fuertemente
        - Delta completamente contrario
        - Sweep contrario muy relevante
        - Precio se aleja significativamente de zona
        """
        # Caída de score extrema (>30 puntos)
        if evento.score_inicial - classification.final_score > 30:
            return True
        
        # Score cayó por debajo de 40 (muy bajo para FIBO)
        if classification.final_score < 40:
            return True
        
        # OI colapsó (score muy bajo)
        if classification.open_interest.score < 20:
            return True
        
        # CVD muy deteriorado
        if classification.cvd.score < 20:
            return True
        
        # Delta completamente contrario (score muy bajo)
        if classification.delta.score < 15:
            return True
        
        # Sin invalidación extrema detectada
        return False
    
    async def monitor_loop(self, callback=None):
        """Loop principal de monitoreo - INTERVALOS DINÁMICOS (10/15 seg)"""
        self.running = True
        
        print("🔄 Loop de monitoreo iniciado (intervalos dinámicos)")
        
        while self.running:
            try:
                # Determinar el intervalo más corto de eventos activos
                if self.eventos_activos:
                    min_interval = min(
                        evento.check_interval 
                        for evento in self.eventos_activos.values()
                        if hasattr(evento, 'check_interval')
                    ) if any(hasattr(e, 'check_interval') for e in self.eventos_activos.values()) else 15
                else:
                    min_interval = 15  # Default
                
                await asyncio.sleep(min_interval)
                
                # Debug: mostrar eventos activos
                if self.eventos_activos:
                    print(f"\n⏰ Check de monitoreo - Eventos activos: {len(self.eventos_activos)}")
                
                # Revisar todos los eventos activos
                eventos_a_remover = []
                
                for event_id in list(self.eventos_activos.keys()):
                    evento = self.eventos_activos[event_id]
                    
                    # Verificar si es tiempo de hacer check de este evento
                    tiempo_desde_ultimo_check = (datetime.now() - evento.last_check).total_seconds()
                    check_interval = getattr(evento, 'check_interval', 15)
                    
                    if tiempo_desde_ultimo_check < check_interval:
                        continue  # Aún no es tiempo de revisar este evento
                    
                    evento = await self.check_evento(event_id)
                    
                    if evento:
                        # Debug: mostrar estado del evento
                        print(f"   📊 {evento.symbol}: Score={evento.scores_historico[-1]:.1f} (máx:{evento.score_maximo:.1f}), {evento.tendencia}, Estado={evento.status.value}, Check {evento.check_count}/{evento.max_checks}")
                    
                    if evento and evento.status != EventStatus.EN_ANALISIS:
                        # Evento terminó el análisis (ejecutar o descartar)
                        print(f"\n✅ Evento {event_id} finalizó: {evento.status.value}")
                        if callback:
                            print(f"   🔔 Ejecutando callback...")
                            await callback(evento)
                        eventos_a_remover.append(event_id)
                
                # Limpiar eventos terminados
                for event_id in eventos_a_remover:
                    print(f"   🗑️ Removiendo evento {event_id} del tracking")
                    self.remover_evento(event_id)
            
            except Exception as e:
                print(f"❌ Error en loop de monitoreo: {e}")
                import traceback
                traceback.print_exc()
                await asyncio.sleep(5)
    
    def stop(self):
        """Detiene el loop de monitoreo"""
        self.running = False
    
    def obtener_resumen_estado(self, event_id: str) -> str:
        """Genera un resumen del estado actual del evento - NUEVA VERSIÓN"""
        evento = self.eventos_activos.get(event_id)
        if not evento:
            return "Evento no encontrado"
        
        tiempo_transcurrido = int((datetime.now() - evento.created_at).total_seconds())
        tiempo_restante = max(0, evento.tiempo_maximo - tiempo_transcurrido)
        
        tendencia_valor = self._calcular_tendencia(evento.scores_historico)
        
        # Emojis de tendencia
        if evento.tendencia == "MEJORANDO":
            tendencia_emoji = "📈"
        elif evento.tendencia == "DETERIORÁNDOSE":
            tendencia_emoji = "📉"
        else:
            tendencia_emoji = "➡️"
        
        # Calcular score promedio
        score_promedio = sum(evento.scores_historico) / len(evento.scores_historico)
        
        # Determinar próxima acción
        if evento.status == EventStatus.EN_ANALISIS:
            check_interval = getattr(evento, 'check_interval', 15)
            tiempo_desde_ultimo = int((datetime.now() - evento.last_check).total_seconds())
            tiempo_proximo_check = max(0, check_interval - tiempo_desde_ultimo)
            proxima_accion = f"⏳ Próximo check en {tiempo_proximo_check}s"
        else:
            proxima_accion = f"✅ Decisión tomada: {evento.status.value}"
        
        # Mostrar origen del evento
        tipo_senal = "📊 VOLUMEN (1M)" if evento.origin == "VOLUMEN" else f"📈 {evento.origin}"
        check_interval_text = getattr(evento, 'check_interval', 15)
        
        resumen = f"""
━━━━━━━━━━━━━━━━━━━━━━
⏱️ **SEGUIMIENTO EN TIEMPO REAL**
{tipo_senal}
━━━━━━━━━━━━━━━━━━━━━━

⏱️ Tiempo: {tiempo_transcurrido}s / {evento.tiempo_maximo}s
🔍 Checks: {evento.check_count}/{evento.max_checks}
⚡ Intervalo: {check_interval_text}seg
{proxima_accion}

📊 **SCORES:**
• Inicial: {evento.score_inicial:.1f}
• Actual: {evento.scores_historico[-1]:.1f}
• Máximo: {evento.score_maximo:.1f}
• Promedio: {score_promedio:.1f}
{tendencia_emoji} Tendencia: {evento.tendencia} ({tendencia_valor:+.1f} pts/check)

📈 **EVOLUCIÓN:**
{' → '.join([f'{s:.0f}' for s in evento.scores_historico[-5:]])}

💰 **PRECIO:**
• Entrada: ${evento.entry_price:.4f}
• Actual: ${evento.current_price:.4f}
• Distancia: {evento.distance_to_entry:+.2f}%
"""
        
        return resumen
