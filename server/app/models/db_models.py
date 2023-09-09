import datetime
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UsersTable(Base):
    # model for table Users
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False)


class BucketStockMongo(BaseModel):
    stock_code: Optional[str]
    stock_name: Optional[str]
    stock_buying_date: Optional[datetime.datetime]
    initial_stock_allocated_count: Optional[float]
    initial_stock_allocated_price: Optional[float]
    initial_investment_in_stock: Optional[float]


class BucketMongo(BaseModel):
    """
    BucketMongo class represents each bucket in the mongo collection.
    """

    bucket_name: str
    bucket_stocks: List[BucketStockMongo]
    bucket_period: int
    created_by: Optional[int]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    soft_deleted_at: Optional[datetime.datetime]
    investment_amount: Optional[float]
