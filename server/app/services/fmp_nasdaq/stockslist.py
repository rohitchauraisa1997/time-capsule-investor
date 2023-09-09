import time
import json
import re
import datetime
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, insert, Date, Boolean
import requests

try:
    from app.database.mysql import NASDAQ_ENGINE
except ModuleNotFoundError:
    # for running code as a script.
    from sqlalchemy import create_engine

    DATABASE_NASDAQ_URI = (
        "mysql+pymysql://root:root@mysqldb:65334/bucket_gains_tracker_mysqldb"
    )
    NASDAQ_ENGINE = create_engine(DATABASE_NASDAQ_URI, echo=True)


class Base(DeclarativeBase):
    # sqlalchemy.exc.InvalidRequestError: Cannot use 'DeclarativeBase'
    # directly as a declarative base class. Create a Base by creating a subclass of it.
    pass


def convert_date_to_correct_format(year):
    """
    convert date to correct format, since for some stocks in s&p 500
    the "founded" parameter is just the year..
    """
    pattern = r"^(\d{4})-\d{2}-\d{2}$"

    if re.match(pattern, year):
        return year  # Year is already in the desired format
    else:
        try:
            year_int = int(year)
            date = datetime.date(year_int, 1, 1)
            formatted_date = date.strftime("%Y-%m-%d")
            return formatted_date
        except ValueError:
            return None


class StocksList(Base):
    __tablename__ = "Stockslist"
    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    sector = Column(String(100), nullable=True)
    subSector = Column(String(100), nullable=True)
    headQuarter = Column(String(100), nullable=True)
    dateFirstAdded = Column(Date, nullable=True, default=None)
    cik = Column(String(10), nullable=True)
    founded = Column(Date, nullable=True, default=None)
    isTracked = Column(Boolean, nullable=True)

    def check_table_already_exists(self):
        from sqlalchemy import inspect

        inspector = inspect(NASDAQ_ENGINE)
        if "Stockslist" in inspector.get_table_names():
            return True

        return False

    def create_table(self):
        session_maker_instance = sessionmaker(bind=NASDAQ_ENGINE)
        with session_maker_instance() as session:
            # Create the table in the database
            Base.metadata.create_all(NASDAQ_ENGINE)

    def populate_table(self):
        # TODO: move access_token logic to database.
        # NOT USING dotenv for loading these keys..
        # because access_token needs to refreshed frequently.
        # Also this populate_table function is only called once when creating the StockList table.
        # so not much need.
        fmp_api_key = ""
        with open("../../../env.json", "r") as json_file:
            json_content = json.load(json_file)
            fmp_api_key = json_content["fmp_api"]["api_key"]

        # fmp_api = f"https://financialmodelingprep.com/api/v3/nasdaq_constituent?apikey={fmp_api_key}"
        fmp_api = f"https://financialmodelingprep.com/api/v3/sp500_constituent?apikey={fmp_api_key}"

        response = requests.get(fmp_api)
        print(f"time fmp_api took {response.elapsed.total_seconds():.2f} seconds")
        stock_details = response.json()
        val = [
            {
                "symbol": stock_detail["symbol"],
                "name": stock_detail["name"],
                "sector": stock_detail["sector"],
                "subSector": stock_detail["subSector"],
                "headQuarter": stock_detail["headQuarter"],
                "dateFirstAdded": convert_date_to_correct_format(
                    stock_detail["dateFirstAdded"]
                ),
                "cik": stock_detail["cik"],
                "founded": convert_date_to_correct_format(stock_detail["founded"]),
                "isTracked": False,
            }
            for stock_detail in stock_details
        ]
        session_maker_instance = sessionmaker(bind=NASDAQ_ENGINE)
        with session_maker_instance() as session:
            start_time = time.time()
            session.execute(insert(StocksList), val)
            session.commit()
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"populating table took {elapsed_time:.2f} seconds")

    @classmethod
    def get_stock_list(cls):
        """
        return stocks list in nasdaq.
        """
        session_maker_instance = sessionmaker(bind=NASDAQ_ENGINE)
        stocks_list = []
        with session_maker_instance() as session:
            stocks_list_in_db = (
                session.query(
                    StocksList.name,
                    StocksList.symbol,
                )
                .order_by(StocksList.name)
                .all()
            )

            for stock in stocks_list_in_db:
                stocks_list.append((stock[0], stock[1]))
                # stocks_list.append(stock[0])

        return stocks_list


if __name__ == "__main__":
    stocklist = StocksList()
    if not stocklist.check_table_already_exists():
        stocklist.create_table()
        stocklist.populate_table()
