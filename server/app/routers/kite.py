from kiteconnect import KiteConnect, exceptions as kite_exceptions
from fastapi import APIRouter, HTTPException, status
import json

kite_router = APIRouter()


class KiteConnector:
    def __init__(self):
        self.setup()

    def setup(self):
        with open("env.json", "r") as json_file:
            json_content = json.load(json_file)
            self.api_key = json_content["kite_api"]["api_key"]
            # TODO: move access_token logic to database.
            # TODO: implement refresh kite token automatically.
            self.access_token = json_content["kite_api"]["access_token"]

        self.kite = KiteConnect(api_key=self.api_key)
        self.kite.set_access_token(self.access_token)

    def get_latest_price(self, symbol):
        try:
            quote = self.kite.ltp(["NSE:" + symbol])
            latest_price = quote["NSE:" + symbol]["last_price"]
            return latest_price
        except kite_exceptions.InputException:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"error": "Invalid API key or access token"},
            )
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"error": str(error)},
            )

    def place_gtt_order(self, symbol):
        try:
            instrument_token = f"NSE:{symbol}"
            quote = self.kite.ltp([instrument_token])
            # Extract latest price from the response
            latest_price = quote[instrument_token]["last_price"]
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

            trade = self.kite.place_gtt(
                trigger_type=self.kite.GTT_TYPE_SINGLE,
                tradingsymbol=symbol,
                exchange="NSE",
                trigger_values=[trigger_value],
                last_price=latest_price,
                orders=orders,
            )
            trigger_id = trade["trigger_id"]

            return trigger_id

        except kite_exceptions.InputException:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"error": "Invalid API key or access token"},
            )
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"error": str(error)},
            )


kite_connector = KiteConnector()


@kite_router.get("/ltp")
def get_current_price(symbol: str):
    latest_price = kite_connector.get_latest_price(symbol)
    print(f"Latest Price: {latest_price}")
    return latest_price


@kite_router.get("/gtt/buy")
def place_gtt_buy_order(symbol: str):
    trigger_id = kite_connector.place_gtt_order(symbol)
    print(f"trigger_id: {trigger_id}")
    return trigger_id
