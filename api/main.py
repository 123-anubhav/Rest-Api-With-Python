from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from configuration.database import Base, engine, get_db
from models.User import User
from schemas.user import UserCreate, UserResponse


# Create tables
Base.metadata.create_all(bind=engine)


app = FastAPI()


# CREATE
@app.post("/users", response_model=UserResponse)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    new_user = User(
        name=user.name,
        email=user.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# READ ALL
@app.get("/users", response_model=list[UserResponse])
def get_users(
    db: Session = Depends(get_db)
):

    users = db.query(User).all()

    return users


# READ ONE
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# UPDATE
@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserCreate,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.name = user_data.name
    user.email = user_data.email

    db.commit()
    db.refresh(user)

    return user


# DELETE
@app.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

    return {
        "message": "User deleted successfully"
    }