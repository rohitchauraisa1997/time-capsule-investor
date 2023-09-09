from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase,sessionmaker
from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime, Float
from sqlalchemy import text
import json
import requests
from datetime import datetime

fmp_api_key = ""
with open("env.json","r") as json_file:
    json_content = json.load(json_file)
    fmp_api_key = json_content["fmp_api"]["api_key"]

class Base(DeclarativeBase):
    # sqlalchemy.exc.InvalidRequestError: Cannot use 'DeclarativeBase'
    # directly as a declarative base class. Create a Base by creating a subclass of it.
    pass

class StocksListCron(Base):
    __tablename__ = "Stockslist"
    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    sector = Column(String(50), nullable=False)
    subSector = Column(String(50), nullable=False)
    headQuarter = Column(String(100), nullable=True)
    dateFirstAdded = Column(Date, nullable=True)
    cik = Column(String(10), nullable=False)
    founded = Column(Date, nullable=False)
    isTracked = Column(Boolean, nullable=True)
    
    def __init__(self, engine):
        self.engine = engine

    def get_stock_list(self):
        Session = sessionmaker(bind=self.engine)
        stocks_list = []
        with Session() as session:
            stocks_list_in_db = session.query(
                StocksListCron.name,
                StocksListCron.symbol,
            ).all()
        
            for stock in stocks_list_in_db:
                stocks_list.append((stock[1]))

        return stocks_list

class StockCron(Base):
    __tablename__ = (
        "default_value"  # Default table name is necessary, later changed in init call.
    )
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    open = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)

    def __init__(self, stock_index, stock_code, engine):
        self.stock_index = stock_index
        self.stock_code = stock_code
        self.engine = engine
        StockCron.__table__.name = stock_code

    def get_ohlc(self):
        if self.stock_index== "nasdaq":
            fmp_api = "https://financialmodelingprep.com/api/v3/quote/{}?apikey={}".format(
                self.stock_code, fmp_api_key
            )
        else:
            fmp_api = "https://financialmodelingprep.com/api/v3/quote/{}.NS?apikey={}".format(
                self.stock_code, fmp_api_key
            )
        response = requests.get(fmp_api).json()[0]
        # ltp = response["previousClose"]
        return response

    def update_ohlc_in_db(self, ohlc_data):
        open_val = ohlc_data["open"]
        high_val = ohlc_data["dayHigh"]
        low_val = ohlc_data["dayLow"]
        # update close_val with latest price that is fetched from fmpapis.
        close_val = ohlc_data["price"]
        volume_val = ohlc_data["volume"]
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        Session = sessionmaker(bind=self.engine)
        with Session() as session:
            sql_query_final = f"""
                INSERT INTO `{self.stock_code}` (date, open, high, low, close, volume)
                VALUES ('{current_time}', {open_val}, {high_val}, {low_val}, {close_val}, {volume_val})
            """
            final_result = session.execute(text(sql_query_final))
            session.commit()
