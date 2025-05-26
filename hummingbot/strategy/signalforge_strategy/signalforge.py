from hummingbot.strategy.script_strategy_base import ScriptStrategyBase
from hummingbot.connector.connector_base import ConnectorBase
from hummingbot.core.data_type.common import TradeType, OrderType

class SignalForgeStrategy(ScriptStrategyBase):
    def __init__(self):
        super().__init__()
        # Настройки стратегии
        self.exchange = "binance"
        self.trading_pair = "BTC-USDT"
        self.order_amount = 0.001
        self.rsi_period = 14
        self.rsi_threshold = 30
        self.price_precision = 2

        # Хранилище индикаторов
        self.rsi_values = []

    def on_tick(self):
        # Получаем свечи
        candles = self.get_candles(self.exchange, self.trading_pair, "5m")
        if len(candles) < self.rsi_period:
            return  # Недостаточно данных

        # Вычисляем RSI
        closes = [c.close for c in candles[-(self.rsi_period + 1):]]
        rsi = self.calculate_rsi(closes)
        self.rsi_values.append(rsi)

        # Логируем
        self.logger().info(f"RSI: {rsi:.2f}")

        # Условия входа
        if rsi < self.rsi_threshold and self.volume_increasing(candles):
            price = self.connectors[self.exchange].get_mid_price(self.trading_pair)
            self.buy(self.exchange, self.trading_pair, self.order_amount, OrderType.MARKET)
            self.logger().info(f"BUY signal at RSI={rsi:.2f} and price={price:.{self.price_precision}f}")

    def calculate_rsi(self, closes):
        gains = []
        losses = []
        for i in range(1, len(closes)):
            diff = closes[i] - closes[i - 1]
            if diff >= 0:
                gains.append(diff)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(-diff)
        avg_gain = sum(gains[-self.rsi_period:]) / self.rsi_period
        avg_loss = sum(losses[-self.rsi_period:]) / self.rsi_period
        if avg_loss == 0:
            return 100
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    def volume_increasing(self, candles):
        if len(candles) < 4:
            return False
        volumes = [c.volume for c in candles[-4:]]
        return volumes[1] > volumes[0] and volumes[2] > volumes[1] and volumes[3] > volumes[2]
