from sqlalchemy import create_engine
import datetime
from utils import StockCron, StocksListCron
import pytz
import time
# DATABASE_NASDAQ_URI = "mysql+pymysql://root:root@localhost:65334/bucket_gains_tracker_mysqldb"
DATABASE_NASDAQ_URI = (
    "mysql+pymysql://root:root@mysqldb:65334/bucket_gains_tracker_mysqldb"
)
NASDAQ_ENGINE = create_engine(DATABASE_NASDAQ_URI,echo=True)


if __name__=="__main__":
    print("."*70)
    usa = pytz.timezone('US/Eastern')
    current_date = datetime.datetime.now(usa)
    
    # Define the time range in IST
    start_time = datetime.time(9, 0, 0)  # 9:00 AM IST
    end_time = datetime.time(15, 30, 0)  # 3:30 PM IST

    # Get the current time in IST
    usa_current_time = datetime.datetime.now(usa).time()
    
    print("current_date.weekday()",current_date.weekday())
    print("usa_current_time",usa_current_time)

    # Check if the current day is a Saturday (5) or Sunday (6)
    if current_date.weekday() == 5:  # Saturday
        print("It's Saturday! no updation")
    elif current_date.weekday() == 6:  # Sunday
        print("It's Sunday! no updation")
    elif not(start_time <= usa_current_time <= end_time):
        print("market not opened yet")
    else:
        print("script will run for nasdaq")
        stocklist = StocksListCron(engine=NASDAQ_ENGINE)
        stock_codes_list = stocklist.get_stock_list()
        print(stock_codes_list)

        for stock_code in stock_codes_list:
            print("+"*50)
            print("stock_code",stock_code)
            stock_cron = StockCron(stock_index="nasdaq", stock_code=stock_code, engine=NASDAQ_ENGINE)
            ohlc = stock_cron.get_ohlc()
            print("ohlc",ohlc)
            stock_cron.update_ohlc_in_db(ohlc_data=ohlc)
            print("+"*50)
            time.sleep(1)
    print("."*70)