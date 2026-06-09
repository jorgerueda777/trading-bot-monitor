"""
Parser de eventos estructurados
Extrae información normalizada de eventos en texto
"""
import re
from typing import Dict, Optional
from pydantic import BaseModel, Field


class ParsedEvent(BaseModel):
    """Estructura normalizada de un evento"""
    symbol: str
    bias: str  # ALCISTA, BAJISTA
    origin: str  # FIBO_1H, FIBO_4H, FIBO_1D, VOLUMEN
    zone_a: float
    zone_b: float
    target_a: float
    target_b: float
    stop_loss: float = 0.0  # Stop loss
    raw_text: str
    event_type: Optional[str] = None  # SOBRECOMPRA, SOBREVENTA (para señales de volumen)


class EventParser:
    """Interpreta eventos en formato texto y los normaliza"""
    
    BIAS_MAP = {
        'ALCISTA': 'BULLISH',
        'BAJISTA': 'BEARISH',
        'BULLISH': 'BULLISH',
        'BEARISH': 'BEARISH',
        'LONG': 'BULLISH',
        'SHORT': 'BEARISH',
        '🟢': 'BULLISH',
        '🔴': 'BEARISH'
    }
    
    ORIGIN_MAP = {
        'FIBO 1H': 'FIBO_1H',
        'FIBO 4H': 'FIBO_4H',
        'FIBO 1D': 'FIBO_1D',
        'FIBO_1H': 'FIBO_1H',
        'FIBO_4H': 'FIBO_4H',
        'FIBO_1D': 'FIBO_1D',
        'VOLUMEN': 'VOLUMEN',
        'VOLUME': 'VOLUMEN',
        'TRADING_SIGNAL': 'TRADING_SIGNAL'
    }
    
    def parse(self, event_text: str) -> ParsedEvent:
        """
        Extrae información estructurada del evento
        
        Soporta múltiples formatos:
        
        FORMATO 1 (FIBO ESTRICTO):
        #ZORAUSDT
        SESGO ALCISTA
        ORIGEN: FIBO 1D
        ZONA A: 0.0083000
        
        FORMATO 2 (FIBO EN TÍTULO):
        📥 #OGUSDT 🔴 SHORT (FIBO 4H)
        
        FORMATO 3 (VOLUMEN EXPLÍCITO):
        #BTCUSDT
        DIRECCIÓN: SHORT
        ORIGEN: VOLUMEN
        TIPO: SOBRECOMPRA
        
        FORMATO 4 (VOLUMEN SIMPLIFICADO):
        📥 #BTWUSDT 🟢 LONG
        🎯 ENTRADA
          1⃣ $ 0.0693470
        🚀 TP'S
          1⃣ 5% ($ 0.0728144)
        """
        lines = event_text.strip().split('\n')
        
        # Extraer símbolo
        symbol = self._extract_symbol(event_text)
        
        # Detectar si es señal de VOLUMEN
        es_volumen_explicito = 'ORIGEN: VOLUMEN' in event_text.upper() or 'ORIGEN:VOLUMEN' in event_text.upper()
        
        # Detectar formato simplificado de volumen (tiene ENTRADA o TP pero NO tiene FIBO)
        tiene_entrada_o_tp = bool(re.search(r'(ENTRADA|🎯|ENTRY|TP|TARGET|🚀)', event_text, re.IGNORECASE))
        # IMPORTANTE: Buscar FIBO con cualquier temporalidad (1H, 4H, 1D, 1W, etc.)
        tiene_fibo = bool(re.search(r'FIBO\s*\d+[HMWD]', event_text, re.IGNORECASE))
        es_volumen_simplificado = tiene_entrada_o_tp and not tiene_fibo
        
        if es_volumen_explicito or es_volumen_simplificado:
            # FORMATO VOLUMEN
            bias = self._extract_bias_volumen(event_text)
            origin = 'VOLUMEN'
            
            # Intentar extraer tipo, si no existe asumir según dirección
            if es_volumen_explicito:
                event_type = self._extract_event_type(event_text)
            else:
                # Para formato simplificado, inferir tipo desde dirección
                event_type = 'SOBREVENTA' if bias == 'BULLISH' else 'SOBRECOMPRA'
            
            # Para señales de volumen, extraer entradas y TPs si existen
            entradas = self._extract_entries(event_text)
            tps = self._extract_targets(event_text)
            
            zone_a = entradas[0] if len(entradas) > 0 else 0.0
            zone_b = entradas[1] if len(entradas) > 1 else zone_a
            target_a = tps[0] if len(tps) > 0 else 0.0
            target_b = tps[1] if len(tps) > 1 else target_a
        
        else:
            # Detectar formato FIBO estricto
            es_formato_fibo_estricto = 'SESGO' in event_text.upper() and 'ORIGEN' in event_text.upper()
            
            if es_formato_fibo_estricto:
                # Formato FIBO estricto original
                bias_line = next((l for l in lines if 'SESGO' in l.upper()), '')
                bias = self._extract_bias(bias_line)
                
                origin_line = next((l for l in lines if 'ORIGEN' in l.upper()), '')
                origin = self._extract_origin(origin_line)
                
                zone_a = self._extract_value(lines, 'ZONA A')
                zone_b = self._extract_value(lines, 'ZONA B')
                target_a = self._extract_value(lines, 'OBJETIVO A')
                target_b = self._extract_value(lines, 'OBJETIVO B')
            else:
                # Formato FIBO flexible (FIBO en el título con SHORT/LONG)
                bias = self._extract_bias_from_signal(event_text)
                origin = self._extract_origin_flexible(event_text)
                
                # Extraer entradas y TPs
                entradas = self._extract_entries(event_text)
                tps = self._extract_targets(event_text)
                
                zone_a = entradas[0] if len(entradas) > 0 else 0.0
                zone_b = entradas[1] if len(entradas) > 1 else zone_a
                target_a = tps[0] if len(tps) > 0 else 0.0
                target_b = tps[1] if len(tps) > 1 else target_a
            
            event_type = None
        
        # Extraer stop loss (común para todos los formatos)
        stop_loss = self._extract_stop_loss(event_text)
        
        return ParsedEvent(
            symbol=symbol,
            bias=bias,
            origin=origin,
            zone_a=zone_a,
            zone_b=zone_b,
            target_a=target_a,
            target_b=target_b,
            stop_loss=stop_loss,
            raw_text=event_text,
            event_type=event_type
        )
    
    def _extract_symbol(self, text: str) -> str:
        """Extrae el símbolo (busca patrón #SYMBOL o #SYMBOLUSDT)"""
        match = re.search(r'#([A-Z0-9]+USDT|[A-Z0-9]+)', text, re.IGNORECASE)
        if match:
            symbol = match.group(1).upper()
            # Asegurar que termine en USDT
            if not symbol.endswith('USDT'):
                symbol += 'USDT'
            return symbol
        raise ValueError(f"No se pudo extraer símbolo del texto")
    
    def _extract_bias(self, line: str) -> str:
        """Extrae y normaliza el sesgo"""
        for key, value in self.BIAS_MAP.items():
            if key in line.upper():
                return value
        raise ValueError(f"No se pudo extraer sesgo de: {line}")
    
    def _extract_origin(self, line: str) -> str:
        """Extrae y normaliza el origen temporal"""
        for key, value in self.ORIGIN_MAP.items():
            if key in line.upper():
                return value
        raise ValueError(f"No se pudo extraer origen de: {line}")
    
    def _extract_origin_flexible(self, text: str) -> str:
        """Extrae origen cuando está en formato (FIBO 4H) o similar"""
        # Buscar patrón (FIBO 1H/4H/1D/1W/etc.) o FIBO 1H/4H/1D/1W en cualquier parte
        match = re.search(r'FIBO\s*(\d+)([HMWD])', text, re.IGNORECASE)
        if match:
            number = match.group(1)
            unit = match.group(2).upper()
            
            # Mapear a los orígenes soportados
            if unit == 'H':
                # 1H, 4H, etc.
                if number == '1':
                    return 'FIBO_1H'
                elif number == '4':
                    return 'FIBO_4H'
                else:
                    # Otras horas -> usar el más cercano
                    return 'FIBO_4H'
            elif unit == 'D':
                # 1D, 2D, etc.
                return 'FIBO_1D'
            elif unit == 'W' or unit == 'M':
                # 1W (semanal) o 1M (mensual) -> mapear a 1D (temporalidad más alta disponible)
                return 'FIBO_1D'
        
        # Por defecto FIBO_4H si no se encuentra
        return 'FIBO_4H'
    
    def _extract_bias_volumen(self, text: str) -> str:
        """Extrae el sesgo/dirección de señales de volumen"""
        # Buscar DIRECCIÓN: SHORT/LONG
        match = re.search(r'DIRECCI[ÓO]N:\s*(SHORT|LONG)', text, re.IGNORECASE)
        if match:
            direction = match.group(1).upper()
            return 'BEARISH' if direction == 'SHORT' else 'BULLISH'
        
        # Fallback a búsqueda general
        return self._extract_bias_from_signal(text)
    
    def _extract_event_type(self, text: str) -> str:
        """Extrae el tipo de evento de volumen (SOBRECOMPRA/SOBREVENTA)"""
        if 'SOBRECOMPRA' in text.upper():
            return 'SOBRECOMPRA'
        elif 'SOBREVENTA' in text.upper():
            return 'SOBREVENTA'
        return 'UNKNOWN'
    
    def _extract_value(self, lines: list, label: str) -> float:
        """Extrae un valor numérico de una línea etiquetada"""
        line = next((l for l in lines if label.upper() in l.upper()), '')
        match = re.search(r':\s*([\d.]+)', line)
        if match:
            return float(match.group(1))
        raise ValueError(f"No se pudo extraer {label}")
    
    def _extract_bias_from_signal(self, text: str) -> str:
        """Extrae el sesgo de señales tipo SHORT/LONG"""
        text_upper = text.upper()
        for key, value in self.BIAS_MAP.items():
            if key in text_upper or key in text:
                return value
        # Por defecto asumir BULLISH si no se encuentra
        return 'BULLISH'
    
    def _extract_entries(self, text: str) -> list:
        """
        Extrae precios de entrada de una señal de trading
        
        Soporta formatos:
        - ENTRADA 1⃣ $ 0.4067000
        - 🎯 ENTRADA 1⃣ $ 0.4067000 2⃣ $ 0.410767
        - ZONA A: 0.0083000
        """
        entries = []
        
        # Buscar líneas después de ENTRADA/ENTRY
        lines = text.split('\n')
        in_entry_section = False
        
        for line in lines:
            if 'ENTRADA' in line.upper() or 'ENTRY' in line.upper() or '🎯' in line:
                in_entry_section = True
                # También buscar en la misma línea
                # Patrón: $ 0.4067000 (con decimales completos)
                matches = re.findall(r'\$\s*([\d]+\.[\d]+)', line)
                if matches:
                    for match in matches:
                        try:
                            price = float(match)
                            if 0.00000001 < price < 1000000:  # Rango válido
                                entries.append(price)
                        except ValueError:
                            continue
                continue
            
            if in_entry_section:
                # Buscar patrones de precio: $ 0.0072600 o $ 95000
                # CRÍTICO: Usar patrón que capture TODOS los decimales O enteros
                # Patrón mejorado: $ seguido de número con o sin decimales
                matches = re.findall(r'\$\s*([\d]+(?:\.[\d]+)?)', line)
                
                if not matches:
                    # Intentar sin símbolo $ pero solo números con decimales
                    # Buscar números con formato: 0.0072600 (al menos 1 decimal)
                    matches = re.findall(r'\b(\d+\.\d+)\b', line)
                
                for match in matches:
                    try:
                        price = float(match)
                        # Validación: Precio debe estar en rango razonable
                        # Cripto puede ir desde $0.00000001 hasta $100,000
                        if 0.00000001 < price < 1000000:
                            entries.append(price)
                    except ValueError:
                        continue
                
                # Salir de la sección de entradas si encuentra TP o STOP
                if any(keyword in line.upper() for keyword in ['TP', 'TARGET', 'OBJETIVO', 'STOP', '🚀', '🛑']):
                    break
        
        return entries[:2]  # Máximo 2 entradas
    
    def _extract_targets(self, text: str) -> list:
        """Extrae targets/TPs de una señal de trading"""
        targets = []
        
        # Buscar líneas después de TP/TARGET/OBJETIVO
        lines = text.split('\n')
        in_tp_section = False
        
        for line in lines:
            if any(keyword in line.upper() for keyword in ['TP', 'TARGET', 'OBJETIVO', '🚀']):
                in_tp_section = True
                continue
            
            if in_tp_section:
                # Buscar precios entre paréntesis: ($ 0.006897)
                matches = re.findall(r'\(\$\s*([\d.]{4,})\)', line)
                
                if not matches:
                    # Buscar precios con $
                    matches = re.findall(r'\$\s*([\d.]{4,})', line)
                
                for match in matches:
                    try:
                        price = float(match)
                        if price > 0 and price < 1000000:
                            targets.append(price)
                    except ValueError:
                        continue
                
                # Salir si encuentra STOP
                if 'STOP' in line.upper() or '🛑' in line:
                    break
        
        return targets[:2]  # Máximo 2 targets
    
    def _extract_stop_loss(self, text: str) -> float:
        """
        Extrae el stop loss de una señal de trading
        
        Soporta formatos:
        - STOP LOSS: 2.5 % ($ 0.0726623)
        - 🛑 STOP LOSS: $ 3350
        - SL: $ 670
        - STOP: $ 98400
        """
        # Buscar líneas con STOP o SL
        lines = text.split('\n')
        
        for line in lines:
            line_upper = line.upper()
            if 'STOP' in line_upper or '🛑' in line or 'SL:' in line_upper:
                # Buscar precio entre paréntesis: ($ 0.0726623)
                matches = re.findall(r'\(\$\s*([\d]+\.[\d]+)\)', line)
                
                if not matches:
                    # Buscar precio con $: $ 0.0726623 o $ 98400
                    matches = re.findall(r'\$\s*([\d]+(?:\.[\d]+)?)', line)
                
                if matches:
                    try:
                        price = float(matches[0])
                        if 0.00000001 < price < 1000000:  # Rango válido
                            return price
                    except ValueError:
                        continue
        
        return 0.0  # No se encontró stop loss
