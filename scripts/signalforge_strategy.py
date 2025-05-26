from hummingbot.strategy.script_strategy_base import ScriptStrategyBase
from hummingbot.core.data_type.common import TradeType, OrderType

class SignalForgeStrategy(ScriptStrategyBase):
    def __init__(self):
        super().__init__()
        self.trading_pair = "BTC-USDT"
        self.exchange = "binance"
        self.order_amount = 0.001
        self.rsi_period = 14
        self.rsi_threshold = 30
        self.rsi_values = []

    def on_tick(self):
        candles = self.get_candles(self.exchange, self.trading_pair, "5m")
        if len(candles) < self.rsi_period + 1:
            return

        closes = [c.close for c in candles[-(self.rsi_period + 1):]]
        rsi = self.calculate_rsi(closes)
        self.logger().info(f"RSI: {rsi:.2f}")

        if rsi < self.rsi_threshold and self.volume_increasing(candles):
            price = self.connectors[self.exchange].get_mid_price(self.trading_pair)
            self.buy(self.exchange, self.trading_pair, self.order_amount, OrderType.MARKET)
            self.logger().info(f"BUY signal! RSI={rsi:.2f}, Price={price:.2f}")

    def calculate_rsi(self, closes):
        gains = []
        losses = []
        for i in range(1, len(closes)):
            diff = closes[i] - closes[i - 1]
            gains.append(max(diff, 0))
            losses.append(max(-diff, 0))
        avg_gain = sum(gains[-self.rsi_period:]) / self.rsi_period
        avg_loss = sum(losses[-self.rsi_period:]) / self.rsi_period
        if avg_loss == 0:
            return 100
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    def volume_increasing(self, candles):
        volumes = [c.volume for c in candles[-4:]]
        return volumes[1] > volumes[0] and volumes[2] > volumes[1] and volumes[3] > volumes[2]
