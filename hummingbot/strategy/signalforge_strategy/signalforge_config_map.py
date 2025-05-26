from hummingbot.client.config.config_var import ConfigVar

def market_prompt() -> str:
    connector = signalforge_config_map.get("exchange").value
    return f"Enter the token trading pair on {connector} (e.g. BTC-USDT) >>> "

signalforge_config_map = {
    "strategy":
        ConfigVar(key="strategy",
                  prompt="",
                  default="signalforge"),
    "exchange":
        ConfigVar(key="exchange",
                  prompt="Enter the name of the exchange >>> ",
                  prompt_on_new=True,
                  default="binance"),
    "market":
        ConfigVar(key="market",
                  prompt=market_prompt,
                  prompt_on_new=True,
                  default="BTC-USDT"),
    "order_amount":
        ConfigVar(key="order_amount",
                  prompt="Enter the amount per order (e.g. 0.001) >>> ",
                  prompt_on_new=True,
                  default=0.001),
}
