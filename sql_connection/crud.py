from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()
#new code
# #return db.query(models.User).filter(models.User.id == user_id).first()
def get_delete_items(db: Session, item_id:id):
    to=db.query(models.Item).filter(models.Item.id==item_id).first()
    db.delete(to)
    db.commit()
#use user_id
def update_user_item(db: Session, item: schemas.ItemCreate,user_id:int,item_id:id):
    to=db.query(models.Item).filter(models.Item.id==item_id).first()
    to.title=item.title
    db.commit()
    db.refresh(to)
    return to

def recreate_user_item(db: Session, item: schemas.ItemCreate, user_id: int, item_id: id):
    to = db.query(models.Item).filter(models.Item.id == item_id).first()
    to.title = item.title
    to.description=item.description
    db.commit()
    db.refresh(to)
    return to

    #update_data=item.dict(exclude_unset=True)
    #updated_item=stored_item_model.copy(update=update_data)
    #db.commit()
    #db.refresh(updated_item)
    #return updated_item





def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def get_one_items(db: Session, id:id):
    return db.query(models.Item).filter(models.Item.id == id).all()



def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item



