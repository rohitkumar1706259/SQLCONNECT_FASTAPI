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
#
ACCESS_TOKEN_EXPIRE_MINUTES = 30
#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#
app.include_router(users.router)
app.include_router(items.router)
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()










