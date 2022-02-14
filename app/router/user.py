from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schimas, utils

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schimas.UserResponse)
def user_create(user: schimas.User, db: Session = Depends(get_db)):
    if not user.password:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="you should inter your password")
    else:
        hashed_password = utils.hashing_password(user.password)
        user.password = hashed_password
        new_user = models.Users(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schimas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id of {id} dose not exist")

    return user

