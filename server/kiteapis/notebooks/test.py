from kiteconnect import KiteConnect
import logging
import json

logging.basicConfig(level=logging.DEBUG)

api_key = ""
access_token = ""

with open("../../env.json", "r") as json_file:
    json_content = json.load(json_file)
    api_key = json_content["kite_api"]["api_key"]
    access_token = json_content["kite_api"]["access_token"]

kite = KiteConnect(api_key=api_key)
kite.set_access_token(access_token)

symbol = "IDEA"
instrument_token = f"NSE:{symbol}"

quote = kite.ltp([instrument_token])
# Extract latest price from the response
latest_price = quote[instrument_token]["last_price"]
print(latest_price)
trigger_value = latest_price * 0.9
price_to_buy_stock_at = latest_price * 0.9

orders = [
    {
        "exchange": "NSE",
        "tradingsymbol": symbol,
        "transaction_type": "BUY",
        "quantity": 1,
        "order_type": "LIMIT",
        "product": "CNC",
        "price": price_to_buy_stock_at,
    }
]

# self, trigger_type, tradingsymbol, exchange, trigger_values, last_price, orders

trading_id = kite.place_gtt(
    trigger_type=kite.GTT_TYPE_SINGLE,
    tradingsymbol=symbol,
    exchange="NSE",
    trigger_values=[trigger_value],
    last_price=latest_price,
    orders=orders,
)

print(trading_id)
