from fastapi import Depends, HTTPException, status, APIRouter, responses
from fastapi.security import OAuth2PasswordRequestForm
from app.models.requests.user_schemas import User, Token
from app.models.db_models import UsersTable
from app.services.users import UserOps
from app.utils.jwt import get_password_hash, create_access_token, get_current_user

user_router = APIRouter()


@user_router.get("/me")
async def token_validator(current_user: User = Depends(get_current_user)):
    """
    helps check token is valid or not.
    """
    return responses.JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"email": current_user.email, "username": current_user.username},
    )


@user_router.post("/signup")
async def register_user(user: User):
    """
    signup new user.
    """
    email = user.email
    username = user.username
    password = user.password

    user_ops = UserOps()

    if user_ops.get_email_from_db(email) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="email already registered"
        )

    if user_ops.get_username_from_db(username) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="username already registered"
        )

    hashed_password = get_password_hash(password)

    user_ops.create_user_in_db(
        UsersTable(username=username, password=hashed_password, email=email)
    )

    return {"message": "user created successfully"}


@user_router.post("/signin", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    signin user.
    """
    user_ops = UserOps()
    user = user_ops.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


if __name__ == "__main__":
    pass
