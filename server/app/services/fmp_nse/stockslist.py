import time
import csv
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, insert, Date, Boolean

try:
    from app.database.mysql import NSE_ENGINE
except ModuleNotFoundError:
    # for running code as a script.
    from sqlalchemy import create_engine

    DATABASE_NSE_URI = (
        "mysql+pymysql://root:root@mysqldb2:65334/bucket_gains_tracker_mysqldb"
    )
    NSE_ENGINE = create_engine(DATABASE_NSE_URI, echo=True)


class Base(DeclarativeBase):
    # sqlalchemy.exc.InvalidRequestError: Cannot use 'DeclarativeBase'
    # directly as a declarative base class. Create a Base by creating a subclass of it.
    pass


class StocksList(Base):
    __tablename__ = "Stockslist"
    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    sector = Column(
        String(50), nullable=True
    )  # these can be null for Nse data as no api right now to support this data.
    subSector = Column(
        String(50), nullable=True
    )  # these can be null for Nse data as no api right now to support this data.
    headQuarter = Column(String(100), nullable=True)
    dateFirstAdded = Column(Date, nullable=True)
    cik = Column(
        String(10), nullable=True
    )  # these can be null for Nse data as no api right now to support this data.
    founded = Column(
        Date, nullable=True
    )  # these can be null for Nse data as no api right now to support this data.
    isTracked = Column(Boolean, nullable=True)

    def check_table_already_exists(self):
        from sqlalchemy import inspect

        inspector = inspect(NSE_ENGINE)
        if "Stockslist" in inspector.get_table_names():
            return True
        else:
            return False

    def create_table(self):
        session_maker_instance = sessionmaker(bind=NSE_ENGINE)
        with session_maker_instance() as session:
            # Create the table in the database
            Base.metadata.create_all(NSE_ENGINE)

    def populate_table(self):
        stock_details = []
        with open("stockslist.csv", "r") as csv_file:
            # Create a CSV reader object
            csvreader = csv.DictReader(csv_file)

            # Iterate over each row in the CSV and append it to the list
            for row in csvreader:
                stock_details.append(row)

        val = [
            {
                "symbol": stock_detail["symbol"],
                "name": stock_detail["name"],
            }
            for stock_detail in stock_details
        ]

        session_maker_instance = sessionmaker(bind=NSE_ENGINE)
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
        return stocks list in nse.
        """
        session_maker_instance = sessionmaker(bind=NSE_ENGINE)
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
                # stocks_list.append((stock[1]))

        return stocks_list


if __name__ == "__main__":
    stocklist = StocksList()
    if not stocklist.check_table_already_exists():
        stocklist.create_table()
        stocklist.populate_table()
