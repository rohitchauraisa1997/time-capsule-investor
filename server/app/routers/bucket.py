from fastapi import APIRouter, Depends
from app.models.requests.user_schemas import User, BucketSchema
from app.utils.jwt import get_current_user
from app.services.fmp_nasdaq.bucket import (
    add_nasdaq_bucket,
    get_all_nasdaq_buckets,
    get_nasdaq_bucket,
    get_nasdaq_bucket_profit,
    soft_delete_nasdaq_bucket,
    update_nasdaq_bucket,
)
from app.services.fmp_nse.bucket import (
    add_nse_bucket,
    get_all_nse_buckets,
    get_nse_bucket,
    get_nse_bucket_profit,
    soft_delete_nse_bucket,
    update_nse_bucket,
)

bucket_router = APIRouter()


@bucket_router.get("/me", response_model=User)
async def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user


@bucket_router.post("/add", response_description="Add new bucket", response_model=None)
def add_bucket_route(
    stock_index: str,
    bucket: BucketSchema,
    current_user: User = Depends(get_current_user),
):
    """
    add new bucket
    """
    result = None
    if stock_index == "nasdaq":
        result = add_nasdaq_bucket(current_user, bucket)
    if stock_index == "nse":
        result = add_nse_bucket(current_user, bucket)

    return result


@bucket_router.get("/all", response_description="Get all buckets")
def get_all_buckets_route(
    stock_index: str, current_user: User = Depends(get_current_user)
):
    """
    get all buckets
    """
    result = None

    if stock_index == "nasdaq":
        result = get_all_nasdaq_buckets(current_user)

    if stock_index == "nse":
        result = get_all_nse_buckets(current_user)

    return result


@bucket_router.get("/", response_description="Get bucket by id")
def get_bucket_by_id(
    stock_index: str,
    id: str,
    current_user: User = Depends(get_current_user),
):
    """
    get a bucket by objectId of the document in collection.
    """
    result = None
    if stock_index == "nasdaq":
        result = get_nasdaq_bucket(current_user, id)

    if stock_index == "nse":
        result = get_nse_bucket(current_user, id)

    if result is None:
        return
    return result


@bucket_router.delete("/delete", response_description="Get bucket by id")
def soft_delete_bucket_by_id(
    stock_index: str,
    id: str,
    current_user: User = Depends(get_current_user),
):
    """
    delete a bucket by objectId of the document in collection.
    """
    result = None
    if stock_index == "nasdaq":
        result = soft_delete_nasdaq_bucket(current_user, id)
    if stock_index == "nse":
        result = soft_delete_nse_bucket(current_user, id)

    return result


@bucket_router.put("/update", response_description="Update bucket by id")
def update_bucket_by_id(
    stock_index: str,
    id: str,
    bucket: BucketSchema,
    current_user: User = Depends(get_current_user),
):
    """
    update a bucket by objectId of the document in collection.
    """
    result = None
    if stock_index == "nasdaq":
        result = update_nasdaq_bucket(current_user, id, bucket)
    if stock_index == "nse":
        result = update_nse_bucket(current_user, id, bucket)

    return result


@bucket_router.get("/profit", response_description="Get bucket profit by id")
def get_buckets_profit(
    stock_index: str, id: str, current_user: User = Depends(get_current_user)
):
    """
    get bucket's profit
    """
    result = None
    if stock_index == "nasdaq":
        result = get_nasdaq_bucket_profit(current_user, id)
    if stock_index == "nse":
        result = get_nse_bucket_profit(current_user, id)
    return result
