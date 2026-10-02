from sqlalchemy.orm import Session

from models.User import User
from schemas.user import UserCreate
from repositories.user_repository import UserRepository


class UserService:

    def __init__(self):

        self.user_repository = UserRepository()


    def create_user(
        self,
        db: Session,
        request: UserCreate
    ):

        existing_user = self.user_repository.find_by_email(
            db,
            request.email
        )

        if existing_user:
            raise ValueError("Email already exists")

        user = User(
            name=request.name,
            email=request.email
        )

        return self.user_repository.save(
            db,
            user
        )


    def get_users(self, db: Session):

        return self.user_repository.find_all(db)


    def get_user(
        self,
        db: Session,
        user_id: int
    ):

        return self.user_repository.find_by_id(
            db,
            user_id
        )


    def update_user(
        self,
        db: Session,
        user_id: int,
        request: UserCreate
    ):

        user = self.user_repository.find_by_id(
            db,
            user_id
        )

        if user is None:
            return None

        user.name = request.name
        user.email = request.email

        return self.user_repository.save(
            db,
            user
        )


    def delete_user(
        self,
        db: Session,
        user_id: int
    ):

        user = self.user_repository.find_by_id(
            db,
            user_id
        )

        if user is None:
            return False

        self.user_repository.delete(
            db,
            user
        )

        return True
