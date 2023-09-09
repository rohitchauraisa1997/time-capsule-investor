from sqlalchemy import create_engine
import datetime
from utils import StockCron, StocksListCron
import pytz
import time

# DATABASE_NSE_URI = "mysql+pymysql://root:root@localhost:65335/bucket_gains_tracker_mysqldb"
DATABASE_NSE_URI = (
    "mysql+pymysql://root:root@mysqldb2:65334/bucket_gains_tracker_mysqldb"
)
NSE_ENGINE = create_engine(DATABASE_NSE_URI,echo=True)

if __name__=="__main__":
    print("."*70)
    ist = pytz.timezone('Asia/Kolkata')
    current_date = datetime.datetime.now(ist)
    
    # Define the time range in IST
    start_time = datetime.time(9, 0, 0)  # 9:00 AM IST
    end_time = datetime.time(15, 35, 0)  # 3:30 PM IST

    # Get the current time in IST
    ist_current_time = datetime.datetime.now(ist).time()
    
    print("current_date.weekday()",current_date.weekday())
    print("ist_current_time",ist_current_time)

    # Check if the current day is a Saturday (5) or Sunday (6)
    if current_date.weekday() == 5:  # Saturday
        print("It's Saturday! no updation")
    elif current_date.weekday() == 6:  # Sunday
        print("It's Sunday! no updation")
    elif not(start_time <= ist_current_time <= end_time):
        print("market not opened yet")
    else:
        print("script will run for nse")
        stocklist = StocksListCron(engine=NSE_ENGINE)
        stock_codes_list = stocklist.get_stock_list()
        print(stock_codes_list)

        for stock_code in stock_codes_list:
            print("+"*50)
            print("stock_code",stock_code)
            stock_cron = StockCron(stock_index="nse",stock_code=stock_code,engine=NSE_ENGINE)
            ohlc = stock_cron.get_ohlc()
            print("ohlc",ohlc)
            stock_cron.update_ohlc_in_db(ohlc_data=ohlc)
            print("+"*50)
            time.sleep(5)

    print("."*70)
