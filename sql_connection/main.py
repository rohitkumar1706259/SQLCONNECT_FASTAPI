from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
from .routers import users,items
#creating all db
models.Base.metadata.create_all(bind=engine)

#calling api
app = FastAPI()

app.include_router(users.router)
app.include_router(items.router)
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user



'''










'''
@app.patch("/users/{email}", response_model=schemas.User)
def update_password(email: str, db: Session = Depends(get_db)):
    db_user = crud.update_user_password(db=db,email=email,user=user)
    #if db_user is None:
        #raise HTTPException(status_code=404, detail="User not found")
    return db_user

'''
'''
@app.delete("/item/{item_id}", response_model=List[schemas.Item])
def delete_item(item_id:int ,db: Session = Depends(get_db)):
    items = crud.get_delete_items(db=db,item_id=item_id)

@app.patch("/users/{user_id}/items/{item_id}", response_model=schemas.Item)
def update_item_for_user(
    user_id:int,item_id: int,item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.update_user_item(db=db, item=item,user_id=user_id,item_id=item_id)



@app.put("/users/{user_id}/items/{item_id}", response_model=schemas.Item)
def recreate_item_for_user(
    user_id:int,item_id: int,item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.recreate_user_item(db=db, item=item,user_id=user_id,item_id=item_id)


#@app.put("/todos/{id}",responses=List[schemas.Item])
#def update_todo(id:int,todo:schemas.Itemupdate)




# end
@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.get("/item/{id}", response_model=List[schemas.Item])
def read_item(id:int ,db: Session = Depends(get_db)):
    items = crud.get_one_items(db=db,id=id)
    if items==[]:
        raise HTTPException(status_code=404, detail="404 -Item not found")
    return items
'''