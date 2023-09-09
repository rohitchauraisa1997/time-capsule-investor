import json
from fastapi import FastAPI
from kiteconnect import KiteConnect

app = FastAPI()


class KiteConnector:
    def __init__(self):
        self.setup()

    def setup(self):
        with open("../../env.json", "r") as json_file:
            # with open("env.json", "r") as json_file:
            json_content = json.load(json_file)
            self.api_key = json_content["kite_api"]["api_key"]
            self.access_token = json_content["kite_api"]["access_token"]

        self.kite = KiteConnect(api_key=self.api_key)
        self.kite.set_access_token(self.access_token)

    def refresh_token(self):
        # Logic to read the new access token from the JSON file and update self.access_token
        # After updating the access token, refresh the KiteConnect instance
        self.kite.set_access_token(self.access_token)

    def get_latest_price(self, symbol):
        try:
            quote = self.kite.ltp(["NSE:" + symbol])
            latest_price = quote["NSE:" + symbol]["last_price"]
            return latest_price
        except Exception as e:
            print("Error:", e)
            self.refresh_token()
            return None


kite_connector = KiteConnector()
price = kite_connector.get_latest_price("IDEA")
print(price)
