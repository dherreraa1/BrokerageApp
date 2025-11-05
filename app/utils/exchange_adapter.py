from datetime import datetime, timezone
import random
from typing import List, Dict
from app.schemas import TradeCreate

class MockExchange:
    def __init__(self):
        self._market_prices = {
            "BTCUSDT": 68000.50,
            "ETHUSDT": 3700.25,
            "AAPL": 230.10,
            "TSLA": 245.30,
        }
        self._exec_counter = 0

    def list_instruments(self) -> List[Dict]:
        return [{"symbol": s, "price": p} for s, p in self._market_prices.items()]

    def get_price(self, symbol: str) -> float:
        price = self._market_prices.get(symbol.upper())
        if price is None:
            raise ValueError(f"Symbol '{symbol}' not supported or not found.")
        return price

    def execute_trade(self, user_id: int, trade: TradeCreate) -> Dict:
        market_price = self.get_price(trade.symbol)
        executed_price = trade.price if trade.price else market_price
        executed_value = round(executed_price * trade.quantity, 8)
        self._exec_counter += 1
        return {
            "execution_id": f"MOCK-{self._exec_counter}",
            "symbol": trade.symbol,
            "side": trade.side,
            "quantity": trade.quantity,
            "price": executed_price,
            "executed_value": executed_value,
            "executed_at": datetime.now(timezone.utc).isoformat(),
            "exchange": "MockExchange",
            "user_id": user_id,
        }

# singleton
exchange = MockExchange()
