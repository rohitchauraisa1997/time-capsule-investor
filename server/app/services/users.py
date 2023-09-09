from sqlalchemy.orm import sessionmaker, aliased
from app.database.mysql import USERS_ENGINE
from app.models.db_models import UsersTable
from passlib.context import CryptContext


class UserOps:
    def __init__(self):
        pass

    @classmethod
    def create_user_in_db(cls, user: UsersTable):
        """
        create new user
        """
        session_maker_instance = sessionmaker(bind=USERS_ENGINE)
        session = session_maker_instance()

        try:
            session.add(user)
            session.commit()
        except Exception as error:
            session.rollback()
            raise error
        finally:
            # close session after use
            session.close()

    @classmethod
    def get_username_from_db(cls, username: str):
        """
        return user if user exists for the given username.
        """
        session_maker_instance = sessionmaker(bind=USERS_ENGINE)
        session = session_maker_instance()

        try:
            user_alias = aliased(UsersTable)

            # Fetch the user from the database based on the username
            user_data = (
                session.query(
                    user_alias.id,
                    user_alias.username,
                    user_alias.password,
                    user_alias.email,
                )
                .filter(user_alias.username == username)
                .first()
            )

            if user_data:
                user = UsersTable(
                    id=user_data[0],
                    username=user_data[1],
                    password=user_data[2],
                    email=user_data[3],
                )
                return user
            
            return None
        finally:
            session.close()

    @classmethod
    def get_email_from_db(cls, email: str):
        """
        return user if user exists for the given email.
        """
        session_maker_instance = sessionmaker(bind=USERS_ENGINE)
        session = session_maker_instance()

        try:
            user_alias = aliased(UsersTable)

            user_data = (
                session.query(
                    user_alias.id,
                    user_alias.username,
                    user_alias.password,
                    user_alias.email,
                )
                .filter(user_alias.email == email)
                .first()
            )

            if user_data:
                user = UsersTable(
                    id=user_data[0],
                    username=user_data[1],
                    password=user_data[2],
                    email=user_data[3],
                )
                return user

            return None
        finally:
            session.close()

    def verify_password(self, plain_password, hashed_password):
        """
        check input password with password stored in database.
        """

        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        pwd_comparison_result = pwd_context.verify(plain_password, hashed_password)
        return pwd_comparison_result

    def authenticate_user(self, username, password):
        """
        authennticate user function
        """
        user = self.get_username_from_db(username)
        if not user:
            return False
        if not self.verify_password(password, user.password):
            return False

        return user


if __name__ == "__main__":
    pass
