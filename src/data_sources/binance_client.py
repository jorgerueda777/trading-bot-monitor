"""
Cliente para obtener datos de mercado de Binance
"""
import os
import requests
import hmac
import hashlib
import time
from typing import Dict, Optional
from datetime import datetime
from dotenv import load_dotenv
import statistics

load_dotenv()


class BinanceClient:
    """Cliente para consultar datos de Binance Futures"""
    
    BASE_URL = "https://fapi.binance.com"
    REQUEST_TIMEOUT = 5  # Timeout de 5 segundos
    MAX_RETRIES = 2  # Máximo 2 reintentos
    
    def __init__(self):
        self.session = requests.Session()
        self.api_key = os.getenv('BINANCE_API_KEY')
        self.api_secret = os.getenv('BINANCE_API_SECRET')
        
        # Circuit breaker simple
        self.failure_count = 0
        self.last_failure_time = None
        self.circuit_open = False
        
        # Configurar headers
        headers = {'Content-Type': 'application/json'}
        if self.api_key:
            headers['X-MBX-APIKEY'] = self.api_key
            print(f"✅ Binance API Key configurada")
        
        self.session.headers.update(headers)
        
        # Configurar retry adapter
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry
        
        retry_strategy = Retry(
            total=self.MAX_RETRIES,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
    
    def _check_circuit_breaker(self):
        """Verifica si el circuit breaker está abierto"""
        if not self.circuit_open:
            return True
        
        # Si han pasado 60 segundos, intentar cerrar el circuit breaker
        if self.last_failure_time:
            elapsed = time.time() - self.last_failure_time
            if elapsed > 60:
                print("🔄 Circuit breaker: Reintentando conexión...")
                self.circuit_open = False
                self.failure_count = 0
                return True
        
        return False
    
    def _record_failure(self):
        """Registra un fallo y abre el circuit breaker si hay muchos"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= 5:
            self.circuit_open = True
            print(f"⚠️ Circuit breaker ABIERTO: {self.failure_count} fallos consecutivos")
    
    def _record_success(self):
        """Registra un éxito y resetea el contador"""
        if self.failure_count > 0:
            print(f"✅ Circuit breaker: Conexión restaurada")
        self.failure_count = 0
        self.circuit_open = False
    
    def _sign_request(self, params: dict) -> dict:
        """Firma una petición con la API secret"""
        if not self.api_secret:
            return params
        
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        params['signature'] = signature
        return params
    
    def get_market_data(self, symbol: str) -> Dict:
        """
        Obtiene datos completos de mercado para un símbolo
        
        Args:
            symbol: Símbolo (ej: BTCUSDT)
        
        Returns:
            Diccionario con datos de mercado
        """
        # Verificar circuit breaker
        if not self._check_circuit_breaker():
            print(f"⚠️ Circuit breaker abierto, usando datos de respaldo para {symbol}")
            return self._get_fallback_data()
        
        try:
            # Asegurar formato correcto
            if not symbol.endswith('USDT'):
                symbol = f"{symbol}USDT"
            
            symbol = symbol.upper()
            
            # Obtener datos con timeout
            current_price = self._get_current_price(symbol)
            open_interest_data = self._get_open_interest(symbol)
            funding_data = self._get_funding_rate(symbol)
            volume_data = self._get_volume(symbol)
            
            # Datos adicionales con API key (si está disponible)
            orderbook_data = self._get_orderbook_analysis(symbol) if self.api_key else None
            
            # Registrar éxito
            self._record_success()
            
            return {
                'current_price': current_price,
                'open_interest': open_interest_data,
                'funding': funding_data,
                'volume': volume_data,
                # CVD, Delta y Liquidity Sweeps requieren análisis más complejo
                'cvd': self._get_cvd_analysis(symbol, orderbook_data),
                'delta': self._get_delta_analysis(symbol, orderbook_data),
                'liquidity_sweeps': self._get_sweep_analysis(symbol),
                'vwap': self._calculate_vwap(symbol, current_price)
            }
        
        except requests.exceptions.Timeout:
            print(f"⚠️ Timeout obteniendo datos de Binance para {symbol}")
            self._record_failure()
            return self._get_fallback_data()
        except Exception as e:
            print(f"⚠️ Error obteniendo datos de Binance para {symbol}: {e}")
            self._record_failure()
            return self._get_fallback_data()
    
    def _get_current_price(self, symbol: str) -> float:
        """Obtiene precio actual"""
        url = f"{self.BASE_URL}/fapi/v1/ticker/price"
        params = {'symbol': symbol}
        
        response = self.session.get(url, params=params, timeout=self.REQUEST_TIMEOUT)
        response.raise_for_status()
        
        data = response.json()
        return float(data['price'])
    
    def _get_open_interest(self, symbol: str) -> Dict:
        """Obtiene Open Interest y calcula tendencia"""
        # OI actual
        url = f"{self.BASE_URL}/fapi/v1/openInterest"
        params = {'symbol': symbol}
        
        response = self.session.get(url, params=params, timeout=5)
        response.raise_for_status()
        
        current_oi = float(response.json()['openInterest'])
        
        # OI histórico (últimas 24h)
        url_hist = f"{self.BASE_URL}/futures/data/openInterestHist"
        params_hist = {
            'symbol': symbol,
            'period': '5m',
            'limit': 288  # 24 horas en intervalos de 5min
        }
        
        response_hist = self.session.get(url_hist, params=params_hist, timeout=5)
        response_hist.raise_for_status()
        
        hist_data = response_hist.json()
        
        if hist_data:
            # Calcular OI de hace 24h
            previous_oi = float(hist_data[0]['sumOpenInterest'])
            
            # Calcular cambio
            change_pct = ((current_oi - previous_oi) / previous_oi) * 100
            
            # Determinar tendencia
            if change_pct > 5:
                trend = 'INCREASING'
                intensity = min(100, int(abs(change_pct) * 10))
            elif change_pct < -5:
                trend = 'DECREASING'
                intensity = min(100, int(abs(change_pct) * 10))
            else:
                trend = 'STABLE'
                intensity = 50
            
            return {
                'current': current_oi,
                'previous': previous_oi,
                'trend': trend,
                'change_intensity': intensity,
                'change_pct': change_pct
            }
        
        # Si no hay datos históricos
        return {
            'current': current_oi,
            'previous': current_oi,
            'trend': 'STABLE',
            'change_intensity': 50,
            'change_pct': 0
        }
    
    def _get_funding_rate(self, symbol: str) -> Dict:
        """Obtiene Funding Rate y estadísticas"""
        # Funding rate actual
        url = f"{self.BASE_URL}/fapi/v1/premiumIndex"
        params = {'symbol': symbol}
        
        response = self.session.get(url, params=params, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        current_fr = float(data['lastFundingRate'])
        
        # Funding rates históricos
        url_hist = f"{self.BASE_URL}/fapi/v1/fundingRate"
        params_hist = {
            'symbol': symbol,
            'limit': 100  # Últimos 100 funding rates
        }
        
        response_hist = self.session.get(url_hist, params=params_hist, timeout=5)
        response_hist.raise_for_status()
        
        hist_data = response_hist.json()
        
        if hist_data:
            rates = [float(item['fundingRate']) for item in hist_data]
            mean_fr = statistics.mean(rates)
            std_dev = statistics.stdev(rates) if len(rates) > 1 else 0.0001
            
            # Determinar si es extremo (> 2 std devs)
            is_extreme = abs(current_fr - mean_fr) > (2 * std_dev)
            
            return {
                'current': current_fr,
                'mean': mean_fr,
                'std_dev': std_dev,
                'is_extreme': is_extreme
            }
        
        return {
            'current': current_fr,
            'mean': current_fr,
            'std_dev': 0.0001,
            'is_extreme': False
        }
    
    def _get_volume(self, symbol: str) -> Dict:
        """Obtiene volumen y compara con promedio"""
        url = f"{self.BASE_URL}/fapi/v1/klines"
        params = {
            'symbol': symbol,
            'interval': '1h',
            'limit': 24  # Últimas 24 horas
        }
        
        response = self.session.get(url, params=params, timeout=5)
        response.raise_for_status()
        
        klines = response.json()
        
        if klines:
            # Volumen actual (última vela)
            current_volume = float(klines[-1][5])
            
            # Promedio de las últimas 20 velas
            volumes = [float(k[5]) for k in klines[:-1]]
            avg_volume = statistics.mean(volumes) if volumes else current_volume
            
            # Detectar anomalía
            is_anomaly = current_volume > (avg_volume * 1.5)
            
            return {
                'current': current_volume,
                'avg_20': avg_volume,
                'is_anomaly': is_anomaly,
                'ratio': current_volume / avg_volume if avg_volume > 0 else 1.0
            }
        
        return {
            'current': 0,
            'avg_20': 0,
            'is_anomaly': False,
            'ratio': 1.0
        }
    
    def _calculate_vwap(self, symbol: str, current_price: float) -> Dict:
        """Calcula VWAP aproximado"""
        url = f"{self.BASE_URL}/fapi/v1/klines"
        params = {
            'symbol': symbol,
            'interval': '5m',
            'limit': 100
        }
        
        response = self.session.get(url, params=params, timeout=5)
        response.raise_for_status()
        
        klines = response.json()
        
        if klines:
            # VWAP = suma(precio_típico * volumen) / suma(volumen)
            typical_prices = []
            volumes = []
            
            for k in klines:
                high = float(k[2])
                low = float(k[3])
                close = float(k[4])
                volume = float(k[5])
                
                typical_price = (high + low + close) / 3
                typical_prices.append(typical_price)
                volumes.append(volume)
            
            total_volume = sum(volumes)
            if total_volume > 0:
                vwap = sum(tp * v for tp, v in zip(typical_prices, volumes)) / total_volume
                
                # Calcular desviación estándar
                std_dev = statistics.stdev(typical_prices) if len(typical_prices) > 1 else 0
                
                # Calcular cuántas desviaciones estándar está el precio actual
                num_std_devs = abs(current_price - vwap) / std_dev if std_dev > 0 else 0
                
                return {
                    'current_price': current_price,
                    'vwap': vwap,
                    'std_dev': std_dev,
                    'num_std_devs': num_std_devs
                }
        
        return {
            'current_price': current_price,
            'vwap': current_price,
            'std_dev': 0,
            'num_std_devs': 0
        }
    
    def _get_neutral_cvd(self) -> Dict:
        """CVD neutral (requiere análisis más complejo)"""
        return {
            'has_divergence': False,
            'slope_change': 'STABLE',
            'exhaustion_signal': False,
            'alignment_with_bias': True
        }
    
    def _get_neutral_delta(self) -> Dict:
        """Delta neutral (requiere tape reading)"""
        return {
            'current': 0,
            'buyer_intensity': 50,
            'seller_intensity': 50,
            'has_sharp_change': False,
            'bias': 'NEUTRAL'
        }
    
    def _get_neutral_sweeps(self) -> Dict:
        """Liquidity sweeps neutral (requiere análisis de niveles)"""
        return {
            'sweeps': {
                '15m': False,
                '30m': False,
                '1H': False,
                '4H': False
            },
            'sweep_quality': 0,
            'time_since_last_sweep': 999
        }
    
    def _get_orderbook_analysis(self, symbol: str) -> Optional[Dict]:
        """Analiza el order book para detectar presión de compra/venta"""
        try:
            url = f"{self.BASE_URL}/fapi/v1/depth"
            params = {'symbol': symbol, 'limit': 1000}
            
            response = self.session.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            # Calcular liquidez en bids vs asks
            bids = data['bids']
            asks = data['asks']
            
            # Sumar volumen de bids y asks
            bid_volume = sum(float(bid[1]) for bid in bids)
            ask_volume = sum(float(ask[1]) for ask in asks)
            
            total_volume = bid_volume + ask_volume
            
            buyer_intensity = int((bid_volume / total_volume) * 100) if total_volume > 0 else 50
            seller_intensity = 100 - buyer_intensity
            
            return {
                'bid_volume': bid_volume,
                'ask_volume': ask_volume,
                'buyer_intensity': buyer_intensity,
                'seller_intensity': seller_intensity,
                'imbalance': bid_volume - ask_volume
            }
            
        except Exception as e:
            print(f"   ⚠️ No se pudo analizar orderbook: {e}")
            return None
    
    def _get_cvd_analysis(self, symbol: str, orderbook_data: Optional[Dict]) -> Dict:
        """Analiza CVD (Cumulative Volume Delta) usando orderbook"""
        if not orderbook_data:
            return self._get_neutral_cvd()
        
        # Si hay un fuerte desequilibrio, podría indicar divergencia
        imbalance = orderbook_data['imbalance']
        buyer_intensity = orderbook_data['buyer_intensity']
        
        has_divergence = abs(imbalance) > (orderbook_data['bid_volume'] * 0.3)
        
        if buyer_intensity > 60:
            slope_change = 'NEGATIVE_TO_POSITIVE'
        elif buyer_intensity < 40:
            slope_change = 'POSITIVE_TO_NEGATIVE'
        else:
            slope_change = 'STABLE'
        
        return {
            'has_divergence': has_divergence,
            'slope_change': slope_change,
            'exhaustion_signal': buyer_intensity > 85 or buyer_intensity < 15,
            'alignment_with_bias': True
        }
    
    def _get_delta_analysis(self, symbol: str, orderbook_data: Optional[Dict]) -> Dict:
        """Analiza Delta usando orderbook"""
        if not orderbook_data:
            return self._get_neutral_delta()
        
        buyer_intensity = orderbook_data['buyer_intensity']
        seller_intensity = orderbook_data['seller_intensity']
        imbalance = orderbook_data['imbalance']
        
        # Determinar sesgo
        if buyer_intensity > 60:
            bias = 'BULLISH'
        elif seller_intensity > 60:
            bias = 'BEARISH'
        else:
            bias = 'NEUTRAL'
        
        # Detectar cambio brusco (si hay mucho desequilibrio)
        has_sharp_change = abs(buyer_intensity - 50) > 30
        
        return {
            'current': imbalance,
            'buyer_intensity': buyer_intensity,
            'seller_intensity': seller_intensity,
            'has_sharp_change': has_sharp_change,
            'bias': bias
        }
    
    def _get_sweep_analysis(self, symbol: str) -> Dict:
        """Analiza liquidity sweeps basándose en volatilidad reciente"""
        try:
            url = f"{self.BASE_URL}/fapi/v1/klines"
            
            # Obtener velas de diferentes timeframes
            timeframes = {
                '15m': 15,
                '30m': 30,
                '1H': 60,
                '4H': 240
            }
            
            sweeps = {}
            total_quality = 0
            
            for tf_name, minutes in timeframes.items():
                # Obtener las últimas velas
                interval_map = {'15m': '15m', '30m': '30m', '1H': '1h', '4H': '4h'}
                params = {
                    'symbol': symbol,
                    'interval': interval_map[tf_name],
                    'limit': 5
                }
                
                response = self.session.get(url, params=params, timeout=5)
                response.raise_for_status()
                
                klines = response.json()
                
                if klines:
                    # Detectar sweep: cuando el precio toca un extremo y rebota
                    last_kline = klines[-1]
                    high = float(last_kline[2])
                    low = float(last_kline[3])
                    close = float(last_kline[4])
                    open_price = float(last_kline[1])
                    
                    # Calcular rango
                    range_pct = ((high - low) / low) * 100
                    
                    # Sweep si hay volatilidad alta (>2% de rango) y rebote
                    has_sweep = range_pct > 2.0 and abs(close - open_price) < (high - low) * 0.3
                    sweeps[tf_name] = has_sweep
                    
                    if has_sweep:
                        total_quality += 25  # 25 puntos por cada timeframe con sweep
            
            return {
                'sweeps': sweeps,
                'sweep_quality': min(100, total_quality),
                'time_since_last_sweep': 1.0 if any(sweeps.values()) else 999
            }
            
        except Exception as e:
            print(f"   ⚠️ No se pudo analizar sweeps: {e}")
            return self._get_neutral_sweeps()
    
    def _get_fallback_data(self) -> Dict:
        """Datos de respaldo en caso de error"""
        return {
            'current_price': 0,
            'open_interest': {
                'current': 0,
                'previous': 0,
                'trend': 'STABLE',
                'change_intensity': 50
            },
            'funding': {
                'current': 0,
                'mean': 0,
                'std_dev': 0.0001,
                'is_extreme': False
            },
            'cvd': self._get_neutral_cvd(),
            'delta': self._get_neutral_delta(),
            'volume': {
                'current': 0,
                'avg_20': 0,
                'is_anomaly': False
            },
            'liquidity_sweeps': self._get_neutral_sweeps(),
            'vwap': {
                'current_price': 0,
                'vwap': 0,
                'std_dev': 0,
                'num_std_devs': 0
            }
        }
