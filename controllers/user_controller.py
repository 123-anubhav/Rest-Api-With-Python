from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from configuration.database import get_db
from schemas.user import UserCreate, UserResponse
from services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

user_service = UserService()


@router.post(
    "",
    response_model=UserResponse
)
def create_user(
        request: UserCreate,
        db: Session = Depends(get_db)
):
    try:

        response = user_service.create_user(
            db,
            request
        )
        print("user successfully created... ",response.id)
        print("\nuser data ", response)
        return response

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get(
    "",
    response_model=list[UserResponse]
)
def get_users(
        db: Session = Depends(get_db)
):
    return user_service.get_users(db)


@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_user(
        user_id: int,
        db: Session = Depends(get_db)
):
    user = user_service.get_user(
        db,
        user_id
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.put(
    "/{user_id}",
    response_model=UserResponse
)
def update_user(
        user_id: int,
        request: UserCreate,
        db: Session = Depends(get_db)
):
    user = user_service.update_user(
        db,
        user_id,
        request
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.delete("/{user_id}")
def delete_user(
        user_id: int,
        db: Session = Depends(get_db)
):
    deleted = user_service.delete_user(
        db,
        user_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "User deleted successfully"
    }
