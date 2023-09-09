from sqlalchemy import create_engine

# use localhost:65333, localhost:65334, localhost:65335 when running web server in local not as a docker compose service.

# DATABASE_USER_URI = "mysql+pymysql://root:root@localhost:65333/users_db"
DATABASE_USER_URI = "mysql+pymysql://root:root@usermysqldb:65334/users_db"
USERS_ENGINE = create_engine(DATABASE_USER_URI, echo=True)

# DATABASE_NASDAQ_URI = "mysql+pymysql://root:root@localhost:65334/bucket_gains_tracker_mysqldb"
DATABASE_NASDAQ_URI = (
    "mysql+pymysql://root:root@mysqldb:65334/bucket_gains_tracker_mysqldb"
)
NASDAQ_ENGINE = create_engine(DATABASE_NASDAQ_URI, echo=True)

# DATABASE_NSE_URI = "mysql+pymysql://root:root@localhost:65335/bucket_gains_tracker_mysqldb"
DATABASE_NSE_URI = (
    "mysql+pymysql://root:root@mysqldb2:65334/bucket_gains_tracker_mysqldb"
)
NSE_ENGINE = create_engine(DATABASE_NSE_URI, echo=True)
