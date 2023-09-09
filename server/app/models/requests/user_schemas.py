from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str or None = None


class User(BaseModel):
    username: str
    email: str
    password: str


class UserInDB(User):
    hashed_password: str


class BucketSchema(BaseModel):
    bucket_name: str
    bucket_stocks: list[str]
    bucket_period: int
    investment_amount: Optional[float]


if __name__ == "__main__":
    pass
