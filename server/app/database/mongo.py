"""
db connection string
"""
from pymongo import MongoClient

NASDAQ_CONN_STRING = (
    "mongodb://bucket-user:bucket-pwd@mongodb:27017/?authSource=bucket_gains_tracker_mongodb"
    # use following one when running web server in local not as a docker compose service.
    # "mongodb://bucket-user:bucket-pwd@localhost:27021/?authSource=bucket_gains_tracker_mongodb"
)

NASDAQ_CLIENT = MongoClient(NASDAQ_CONN_STRING)

MONGO_DB_NASDAQ = NASDAQ_CLIENT["bucket_gains_tracker_mongodb"]

NSE_CONN_STRING = (
    "mongodb://bucket-user:bucket-pwd@mongodb2:27017/?authSource=bucket_gains_tracker_mongodb"
    # use following one when running web server in local not as a docker compose service.
    # "mongodb://bucket-user:bucket-pwd@localhost:27022/?authSource=bucket_gains_tracker_mongodb"
)

NSE_CLIENT = MongoClient(NSE_CONN_STRING)

MONGO_DB_NSE = NSE_CLIENT["bucket_gains_tracker_mongodb"]
