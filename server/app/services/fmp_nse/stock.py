# TODO: move nse logic to common fmp package as it supports nse stocks as well.
import time
import json
from sqlalchemy import Column, Float, Integer, DateTime, text, insert
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.sql import func
import requests
import pytz

try:
    from app.database.mysql import NSE_ENGINE
except ModuleNotFoundError:
    # for running code as a script.
    from stockslist import StocksList
    from sqlalchemy import create_engine

    DATABASE_NSE_URI = (
        "mysql+pymysql://root:root@mysqldb2:65334/bucket_gains_tracker_mysqldb"
    )
    NSE_ENGINE = create_engine(DATABASE_NSE_URI, echo=True)


def get_stock_dml(table_name):
    """
    using this function to resolve the issue of getting dmls
    for each new table in insert function.
    """
    # TODO: find a better way of getting table: _DMLTableArgument for the bulk insert function
    from sqlalchemy.orm import declarative_base

    class Stock(declarative_base()):
        __tablename__ = table_name
        __table_args__ = {"extend_existing": True}
        id = Column(Integer, primary_key=True)
        date = Column(DateTime, nullable=False)
        open = Column(Float, nullable=False)
        low = Column(Float, nullable=False)
        high = Column(Float, nullable=False)
        close = Column(Float, nullable=False)
        volume = Column(Float, nullable=False)

    return Stock


class Base(DeclarativeBase):
    # sqlalchemy.exc.InvalidRequestError: Cannot use 'DeclarativeBase'
    # directly as a declarative base class. Create a Base by creating a subclass of it.
    pass


class Stock(Base):
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

    def __init__(self, stock_code):
        print("init called")
        self.stock_code = stock_code
        Stock.__table__.name = stock_code

    def check_table_already_exists(self):
        """
        helps check if table exists in the database.
        """
        from sqlalchemy import inspect

        inspector = inspect(NSE_ENGINE)
        if self.stock_code in inspector.get_table_names():
            return True

        return False

    def create_table(self):
        """
        creates table for first time data population.
        when module is ran as script.
        """
        session_maker_instance = sessionmaker(bind=NSE_ENGINE)
        with session_maker_instance() as session:
            try:
                # Create the table in the database
                Stock.__table__.name = self.stock_code
                Base.metadata.create_all(NSE_ENGINE)
            except Exception as error:
                session.rollback()  # Rollback the transaction in case of an error
                print(f"Error creating table: {error}")
            finally:
                print(
                    "closing session after creating table for stock ==== ",
                    self.stock_code,
                )
                session.close()

    def populate_table(self):
        """
        populates table for stock.
        when module is ran as script.
        """
        # TODO: move access_token logic to database.
        # NOT USING dotenv for loading these keys..
        # because access_token needs to refreshed frequently.
        # Also this populate_table function is only called once when creating the Stock tables.
        # so not much need.
        fmp_api_key = ""
        try:
            with open("../../../env.json", "r") as json_file:
                json_content = json.load(json_file)
                fmp_api_key = json_content["fmp_api"]["api_key"]
        except Exception as error:
            print(error)
            # as a fallback in case the app calls the populate_table (for non existing stock tables)
            # function rather than the module being executed as a script.
            with open("env.json", "r") as json_file:
                json_content = json.load(json_file)
                fmp_api_key = json_content["fmp_api"]["api_key"]

        fmp_api = f"https://financialmodelingprep.com/api/v3/historical-chart/1day/{self.stock_code}.NS?apikey={fmp_api_key}"
        response = requests.get(fmp_api)
        print(f"time fmp_api took {response.elapsed.total_seconds():.2f} seconds")
        stock_details = response.json()
        stock_details.reverse()
        val = [
            {
                "date": stock_detail["date"],
                "open": stock_detail["open"],
                "low": stock_detail["low"],
                "high": stock_detail["high"],
                "close": stock_detail["close"],
                "volume": stock_detail["volume"],
            }
            for stock_detail in stock_details
        ]
        session_maker_instance = sessionmaker(bind=NSE_ENGINE)

        with session_maker_instance() as session:
            start_time = time.time()

            # TODO: find a better way of getting table: _DMLTableArgument for the bulk insert function
            stock_dml = get_stock_dml(self.stock_code)
            session.execute(insert(stock_dml), val)

            session.commit()
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"populating table took {elapsed_time:.2f} seconds")
            session.close()

    def get_initial_allocated_stocks_and_initial_date_to_update_document(
        self, initial_invested_amount, initial_date
    ):
        """
        helps get the initial stocks that were allocated based on the initial
        investment amount and initial investment date.
        """
        session_maker_instance = sessionmaker(bind=NSE_ENGINE)
        with session_maker_instance() as session:
            sql_query = f"""
            SELECT date, close
            FROM `{self.stock_code}`
            ORDER BY ABS(DATEDIFF(date, :initial_date))
            LIMIT 1
            """
            result = session.execute(
                text(sql_query), {"initial_date": initial_date}
            ).fetchone()
            initial_date = result[0]
            price_on_initial_date = result[1]
            stocks_allocated = initial_invested_amount / price_on_initial_date

            session.close()

            return {
                "stocks_allocated": stocks_allocated,
                "initial_date": initial_date,
                "price_on_initial_date": price_on_initial_date,
            }

    def get_latest_stock_price_and_date(self):
        """
        helps fetch the latest price from db.
        """
        session_maker_instance = sessionmaker(bind=NSE_ENGINE)
        final_price = 0
        with session_maker_instance() as session:
            # Raw SQL query to get the final price and date
            sql_query_final = f"""
                SELECT date, close
                FROM `{self.stock_code}`
                WHERE date = (
                    SELECT MAX(date)
                    FROM `{self.stock_code}`
                )
            """
            final_result = session.execute(text(sql_query_final)).fetchone()
            if not final_result:
                raise Exception("No data found for the stock code.")
            final_date, final_price = final_result
            session.close()

            return {"final_date": final_date, "final_price": final_price}

    def render_data(self):
        """
        returns the data for rendering charts using highcharts api.
        """
        session_maker_instance = sessionmaker(bind=NSE_ENGINE)
        with session_maker_instance() as session:
            sql_query = f"SELECT Date, Close FROM `{self.stock_code}`"
            details = session.execute(text(sql_query)).fetchall()
            details_to_render = []
            for detail in details:
                # Step 1: Convert datetime object to UTC timezone-aware datetime object
                date_and_time = detail[0]
                close_price = detail[1]
                utc_tz = pytz.timezone("UTC")
                utc_dt = utc_tz.localize(date_and_time)

                # Step 2: Convert UTC timezone-aware datetime object to Unix timestamp
                unix_timestamp = int(utc_dt.timestamp())

                details_to_render.append([unix_timestamp * 1000, close_price])
            session.close()

            return details_to_render

    def get_initial_date(self):
        """
        helps validate if stock data is available for the date the user wants to
        create the bucket.
        """
        session_maker_instance = sessionmaker(bind=NSE_ENGINE)
        with session_maker_instance() as session:
            sql_query_to_get_initial_date = f"""
                SELECT date
                FROM `{self.stock_code}`
                WHERE date = (
                    SELECT MIN(date)
                    FROM `{self.stock_code}`
                )
            """
            result = session.execute(text(sql_query_to_get_initial_date)).fetchone()
            earliest_date = result[0]
            print(f"earliest_date for stock {self.stock_code} => {earliest_date}")

            return earliest_date

    def __repr__(self):
        return f"Stock Table: {self.__table__.name}"


if __name__ == "__main__":
    # run as a script for creating and populating nasdaq tables.
    nasdaq_stock_list = StocksList()
    stock_symbols = nasdaq_stock_list.get_stock_list()
    for stock_name, stock_symbol in stock_symbols:
        stock = Stock(stock_symbol)
        if not (stock.check_table_already_exists()):
            print(f"table for {stock_symbol} doesnt exist..")
            stock.create_table()
            stock.populate_table()
