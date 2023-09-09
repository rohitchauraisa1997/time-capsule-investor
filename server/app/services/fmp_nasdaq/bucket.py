import datetime

from fastapi import responses, status
from app.database.mongo import MONGO_DB_NASDAQ
from app.models.requests.user_schemas import BucketSchema
from app.models.db_models import UsersTable
from app.models.db_models import BucketMongo, BucketStockMongo
from app.services.fmp_nasdaq.stock import Stock as StockNasdaq
from bson import ObjectId
from .stockslist import StocksList

nasdaq_stock_list = StocksList()
stock_symbols = nasdaq_stock_list.get_stock_list()
STOCK_NAME_AND_SYMBOL_DICT = {}

for stock_name, stock_symbol in stock_symbols:
    STOCK_NAME_AND_SYMBOL_DICT[stock_symbol] = stock_name

bucket_gains_collection = MONGO_DB_NASDAQ["bucket-gains"]


def add_nasdaq_bucket(current_user: UsersTable, input_bucket: BucketSchema):
    """
    add nasdaq bucket to bucket_gains_tracker_mongodb database collection bucket-gains.
    """

    bucket_name = input_bucket.bucket_name
    stock_codes = input_bucket.bucket_stocks
    bucket_period = input_bucket.bucket_period
    bucket_investment = input_bucket.investment_amount
    invested_amount_for_each_stock = bucket_investment / len(stock_codes)
    utc_time_now = datetime.datetime.utcnow()
    bucket_buying_date = utc_time_now - datetime.timedelta(days=365 * bucket_period)

    bucket_stocks = []
    for stock_code in stock_codes:
        stock = StockNasdaq(stock_code)
        if not stock.check_table_already_exists():
            stock.create_table()
            stock.populate_table()

        earliest_date_data_available = stock.get_initial_date()
        if bucket_buying_date < earliest_date_data_available:
            raise ValueError(
                f"""bucket_buying_date is older than earliest_date_data_available for stock {stock_code}! Try Decreasing the bucket period."""
            )

        stock_initial_date_and_alloted_stocks = (
            stock.get_initial_allocated_stocks_and_initial_date_to_update_document(
                invested_amount_for_each_stock, bucket_buying_date
            )
        )
        bucket_stock = BucketStockMongo(
            stock_code=stock_code,
            stock_name=STOCK_NAME_AND_SYMBOL_DICT[stock_code],
            stock_buying_date=stock_initial_date_and_alloted_stocks["initial_date"],
            initial_stock_allocated_count=stock_initial_date_and_alloted_stocks[
                "stocks_allocated"
            ],
            initial_investment_in_stock=invested_amount_for_each_stock,
            initial_stock_allocated_price=stock_initial_date_and_alloted_stocks[
                "price_on_initial_date"
            ],
        )
        bucket_stocks.append(bucket_stock)

    bucket_in_db = BucketMongo(
        bucket_name=bucket_name,
        bucket_period=bucket_period,
        bucket_stocks=bucket_stocks,
        investment_amount=bucket_investment,
        created_by=current_user.id,
        created_at=utc_time_now,
        updated_at=utc_time_now,
        soft_deleted_at=None,
    )

    # document must be an instance of dict, bson.son.SON, bson.raw_bson.RawBSONDocument,
    # or a type that inherits from collections.MutableMapping
    bucket_dict = bucket_in_db.model_dump(by_alias=True)

    bucket_gains_collection.insert_one(bucket_dict)
    bucket_dict["_id"] = str(bucket_dict["_id"])
    return bucket_dict


def get_all_nasdaq_buckets(current_user: UsersTable):
    """
    get all nasdaq buckets from bucket_gains_tracker_mongodb database collection bucket-gains.
    """
    all_buckets = []
    cursor = bucket_gains_collection.find(
        {"created_by": current_user.id, "soft_deleted_at": None}
    ).sort("created_at", -1)
    for document in cursor:
        all_buckets.append(document)

    for bucket in all_buckets:
        bucket["_id"] = str(bucket["_id"])
    return all_buckets


def get_nasdaq_bucket(current_user: UsersTable, object_id: str):
    """
    get bucket from bucket_gains_tracker_mongodb database collection
    bucket-gains using objectId in collection.
    """
    bucket = bucket_gains_collection.find_one(
        {
            "_id": ObjectId(object_id),
            "created_by": current_user.id,
        }
    )
    if bucket:
        bucket["_id"] = str(bucket["_id"])
        return bucket

    return responses.JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content="bucket not found"
    )


def soft_delete_nasdaq_bucket(current_user: UsersTable, object_id: str):
    """
    update soft_deleted_at parameter in the bucket-gains collection.
    """
    # Update document in MongoDB
    deleted_at_time = datetime.datetime.utcnow()
    result = bucket_gains_collection.find_one_and_update(
        {
            "_id": ObjectId(object_id),
            "soft_deleted_at": None,
            "created_by": current_user.id,
        },
        {"$set": {"soft_deleted_at": deleted_at_time}},
        return_document=True,
    )

    # Return updated document
    if result:
        result["_id"] = str(result["_id"])
        return result

    return responses.JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content="bucket not found"
    )


def update_nasdaq_bucket(
    current_user: UsersTable, object_id: str, input_bucket: BucketSchema
):
    """
    update the bucket in bucket-gains collection.
    """
    updated_bucket_name = input_bucket.bucket_name
    updated_stock_codes = input_bucket.bucket_stocks
    updated_bucket_period = input_bucket.bucket_period
    updated_bucket_investment = input_bucket.investment_amount
    updated_invested_amount_for_each_stock = updated_bucket_investment / len(
        updated_stock_codes
    )
    utc_time_now = datetime.datetime.utcnow()
    updated_bucket_buying_date = utc_time_now - datetime.timedelta(
        days=365 * updated_bucket_period
    )

    updated_bucket_stocks = []
    for stock_code in updated_stock_codes:
        stock = StockNasdaq(stock_code)
        if not (stock.check_table_already_exists()):
            stock.create_table()
            stock.populate_table()

        earliest_date_data_available = stock.get_initial_date()
        if updated_bucket_buying_date < earliest_date_data_available:
            raise ValueError(
                f"""update test... bucket_buying_date is older than earliest_date_data_available for stock {stock_code}! Try Decreasing the bucket period."""
            )

        stock_initial_date_and_alloted_stocks = (
            stock.get_initial_allocated_stocks_and_initial_date_to_update_document(
                updated_invested_amount_for_each_stock, updated_bucket_buying_date
            )
        )

        bucket_stock = BucketStockMongo(
            stock_code=stock_code,
            stock_name=STOCK_NAME_AND_SYMBOL_DICT[stock_code],
            stock_buying_date=stock_initial_date_and_alloted_stocks["initial_date"],
            initial_stock_allocated_count=stock_initial_date_and_alloted_stocks[
                "stocks_allocated"
            ],
            initial_investment_in_stock=updated_invested_amount_for_each_stock,
            initial_stock_allocated_price=stock_initial_date_and_alloted_stocks[
                "price_on_initial_date"
            ],
        )
        bucket_stock = dict(bucket_stock)
        updated_bucket_stocks.append(bucket_stock)

    result = bucket_gains_collection.find_one_and_update(
        {
            "_id": ObjectId(object_id),
            "soft_deleted_at": None,
            "created_by": current_user.id,
        },
        {
            "$set": {
                "bucket_name": updated_bucket_name,
                "bucket_period": updated_bucket_period,
                "bucket_stocks": updated_bucket_stocks,
                "investment_amount": updated_bucket_investment,
                "updated_at": utc_time_now,
            }
        },
        return_document=True,
    )

    # Return updated document
    if result:
        result["_id"] = str(result["_id"])
        return result
    return responses.JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content="bucket not found"
    )


def get_nasdaq_bucket_profit(current_user: UsersTable, id: str):
    """
    returns the profit/loss for each stock in the bucket over the time period
    of the bucket along with the profit/loss for the whole bucket.
    """
    bucket = bucket_gains_collection.find_one(
        {"_id": ObjectId(id), "created_by": current_user.id}
    )
    # response = {}
    if bucket is None or len(bucket["bucket_stocks"]) == 0:
        return responses.JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "bucket not found or stock in bucket are empty."},
        )

    bucket["_id"] = str(bucket["_id"])

    bucket_initial_investment = bucket["investment_amount"]

    bucket_final_investment = 0
    for i in range(len(bucket["bucket_stocks"])):
        # get initial count and initial investment from the mongo bucket-gains collection.
        initial_count = bucket["bucket_stocks"][i]["initial_stock_allocated_count"]
        initial_investement = bucket["bucket_stocks"][i]["initial_investment_in_stock"]
        stock = StockNasdaq(bucket["bucket_stocks"][i]["stock_code"])

        # get the latest price and latest date available from the sql database.
        final_price_and_date = stock.get_latest_stock_price_and_date()
        final_price = final_price_and_date["final_price"]
        final_date = final_price_and_date["final_date"]
        final_investment = final_price * initial_count

        bucket["bucket_stocks"][i]["final_price"] = final_price
        bucket["bucket_stocks"][i]["final_date"] = final_date
        bucket["bucket_stocks"][i]["final_investment_in_stock"] = final_investment
        bucket["bucket_stocks"][i]["monetary_gains"] = (
            final_investment - initial_investement
        )
        bucket["bucket_stocks"][i]["percentage_gains"] = (
            (final_investment - initial_investement) / initial_investement
        ) * 100
        bucket_final_investment += final_investment

    bucket["initial_investment"] = bucket_initial_investment
    bucket["final_investment"] = bucket_final_investment
    bucket["monetary_gains"] = bucket_final_investment - bucket_initial_investment
    bucket["percentage_gains"] = (
        (bucket_final_investment - bucket_initial_investment)
        / bucket_initial_investment
    ) * 100

    return bucket
