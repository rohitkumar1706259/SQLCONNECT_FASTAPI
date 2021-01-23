from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from . import models, schemas
# new edit
from jose import JWTError, jwt
from passlib.context import CryptContext

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import Optional

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def authenticate_user(fake_db, email: str, password: str):
    user = get_user(fake_db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt














##########################################################################################
def get_user_name(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()
#new code
# #return db.query(models.User).filter(models.User.id == user_id).first()
def get_delete_items(db: Session, item_id:id):
    to=db.query(models.Item).filter(models.Item.id==item_id).first()
    db.delete(to)
    db.commit()

def get_delete_users(db: Session, user_id:id):
    to=db.query(models.User).filter(models.User.id==user_id).first()
    db.delete(to)
    db.commit()




#use user_id
def update_user_item(db: Session, item: schemas.ItemCreate,user_id:int,item_id:id):
    to=db.query(models.Item).filter(models.Item.id==item_id).first()
    to.title=item.title
    db.commit()
    db.refresh(to)
    return to

def user_update(db: Session, user: schemas.UserCreate,user_id:int):
    to=db.query(models.User).filter(models.User.id==user_id).first()
    to.email=user.email
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


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    #fake_hashed_password = user.password + "notreallyhashed"
    #db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db_user = models.User(email=user.email, hashed_password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session,skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def get_one_items(db: Session, id:id):
    return db.query(models.Item).filter(models.Item.id == id).all()



def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item



