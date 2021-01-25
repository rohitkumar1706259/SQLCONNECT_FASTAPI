from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sql_connection import crud, models, schemas
from sql_connection.database import SessionLocal, engine
from fastapi import APIRouter
from sql_connection.routers import users

router=APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.delete("/item/{item_id}", response_model=List[schemas.Item],tags=["items"])
def delete_item(item_id:int ,db: Session = Depends(get_db)):
    items = crud.get_delete_items(db=db,item_id=item_id)

@router.patch("/users/{user_id}/items/{item_id}", response_model=schemas.Item,tags=["items"])
def update_item_for_user(
    user_id:int,item_id: int,item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.update_user_item(db=db, item=item,user_id=user_id,item_id=item_id)



@router.put("/users/{user_id}/items/{item_id}", response_model=schemas.Item,tags=["items"])
def recreate_item_for_user(
    user_id:int,item_id: int,item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.recreate_user_item(db=db, item=item,user_id=user_id,item_id=item_id)


@router.post("/users/{user_id}/items/", response_model=schemas.Item,tags=["items"])
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db),current:schemas.User=Depends(users.get_current_active_user)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)

'''
@router.get("/items/", response_model=List[schemas.Item],tags=["items"])
def read_items(db: Session = Depends(get_db),skip: int = 0, limit: int = 100):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

'''
@router.get("/item/{id}", response_model=List[schemas.Item],tags=["items"])
def read_item(id:int ,db: Session = Depends(get_db)):
    items = crud.get_one_items(db=db,id=id)
    if items==[]:
        raise HTTPException(status_code=404, detail="404 -Item not found")
    return items
