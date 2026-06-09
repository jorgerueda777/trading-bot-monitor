"""
Order Book Imbalance Evaluator
Analiza desequilibrios en bid/ask para señales de 1 minuto
"""
from .base_metric import MetricEvaluator


class OrderBookEvaluator(MetricEvaluator):
    """Evalúa el desequilibrio del order book"""
    
    def evaluate(self, data: dict) -> float:
        """
        Evalúa el desequilibrio bid/ask
        
        Args:
            data: {
                'bid_liquidity': float,  # Liquidez en bids
                'ask_liquidity': float,  # Liquidez en asks
                'imbalance_ratio': float,  # Ratio bid/ask
                'large_orders': list,  # Órdenes grandes detectadas
                'bias': str  # BULLISH o BEARISH
            }
        
        Returns:
            Score 0-100
        """
        bid_liq = data.get('bid_liquidity', 0)
        ask_liq = data.get('ask_liquidity', 0)
        imbalance_ratio = data.get('imbalance_ratio', 1.0)
        large_orders = data.get('large_orders', [])
        bias = data.get('bias', 'BULLISH')
        
        score = 50  # Neutral
        
        # Para BEARISH (SHORT / SOBRECOMPRA):
        # Buscamos muros de venta (asks dominantes) que confirmen rechazo
        if bias == 'BEARISH':
            # Ask dominance favorece el short
            if imbalance_ratio < 0.8:  # Más asks que bids
                score += 30
            elif imbalance_ratio < 1.0:
                score += 15
            
            # Órdenes grandes de venta
            sell_orders = [o for o in large_orders if o.get('side') == 'SELL']
            if len(sell_orders) >= 3:
                score += 20
            elif len(sell_orders) >= 1:
                score += 10
        
        # Para BULLISH (LONG / SOBREVENTA):
        # Buscamos muros de compra (bids dominantes) que confirmen soporte
        else:
            # Bid dominance favorece el long
            if imbalance_ratio > 1.2:  # Más bids que asks
                score += 30
            elif imbalance_ratio > 1.0:
                score += 15
            
            # Órdenes grandes de compra
            buy_orders = [o for o in large_orders if o.get('side') == 'BUY']
            if len(buy_orders) >= 3:
                score += 20
            elif len(buy_orders) >= 1:
                score += 10
        
        return max(0, min(100, score))
    
    def get_analysis(self, data: dict) -> str:
        """Genera análisis descriptivo"""
        imbalance_ratio = data.get('imbalance_ratio', 1.0)
        large_orders = data.get('large_orders', [])
        bias = data.get('bias', 'BULLISH')
        
        if bias == 'BEARISH':
            if imbalance_ratio < 0.8:
                return "Muros de venta dominantes (rechazo probable)"
            elif len([o for o in large_orders if o.get('side') == 'SELL']) >= 2:
                return "Órdenes grandes de venta detectadas"
            else:
                return "Order book neutral o levemente bajista"
        else:
            if imbalance_ratio > 1.2:
                return "Muros de compra dominantes (soporte fuerte)"
            elif len([o for o in large_orders if o.get('side') == 'BUY']) >= 2:
                return "Órdenes grandes de compra detectadas"
            else:
                return "Order book neutral o levemente alcista"
