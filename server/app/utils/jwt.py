from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from app.models.requests.user_schemas import TokenData
from app.services.users import UserOps

SECRET_KEY = "a7a5e3112275fbe0066706e1b246a25474ccd0a72ef97c6fa88744ce2fdf2ee4"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 200
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="signin")


async def get_current_user(token: str = Depends(oauth_2_scheme)):
    cred_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate creds",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise cred_exception

        token_data = TokenData(username=username)

    except JWTError:
        raise cred_exception

    user_ops = UserOps
    user = user_ops.get_username_from_db(username=token_data.username)
    if user is None:
        raise cred_exception

    return user


def get_password_hash(password):
    return PWD_CONTEXT.hash(password)


def create_access_token(data):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = data.copy()
    if access_token_expires:
        expire = datetime.utcnow() + access_token_expires
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode["exp"] = expire

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


if __name__ == "__main__":
    pass
