from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sql_connection import crud, models, schemas
from sql_connection.database import SessionLocal, engine
from fastapi import APIRouter


router=APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users/", response_model=schemas.User,tags=["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.get("/users/", response_model=List[schemas.User],tags=["Users"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.delete("/users/{user_id}", response_model=List[schemas.User],tags=["Users"])
def delete_User(user_id:int ,db: Session = Depends(get_db)):
    items = crud.get_delete_users(db=db,user_id=user_id)




@router.get("/users/{user_id}", response_model=schemas.User,tags=["Users"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.patch("/users/{user_id}", response_model=schemas.User,tags=["Users"])
def update_email(
    user_id:int,user: schemas.UserCreate, db: Session = Depends(get_db)
):
    return crud.user_update(db=db,user=user,user_id=user_id)













