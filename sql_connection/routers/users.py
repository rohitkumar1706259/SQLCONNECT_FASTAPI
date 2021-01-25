from typing import List
from pydantic import ValidationError

from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, Security, status
from sql_connection import crud, models, schemas
from sql_connection.database import SessionLocal, engine
from fastapi import APIRouter
#
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm,SecurityScopes
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token",scopes={"me": "Read information about the current user.", "items": "Read items."})
#
router=APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#
'''
async def get_current_user(db: Session = Depends(get_db),security_scopes: SecurityScopes,token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, crud.SECRET_KEY, algorithms=[crud.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = email
    except JWTError:
        raise credentials_exception
    user = crud.get_user(db,email=token_data)
    if user is None:
        raise credentials_exception
    return user
'''
async def get_current_user(
    security_scopes: SecurityScopes,db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):

    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, crud.SECRET_KEY, algorithms=[crud.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        #token_data = TokenData(scopes=token_scopes,email=email)
        token_data=schemas.TokenData(scopes=token_scopes, email=email)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = crud.get_user(db, email=email)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user



@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(db: Session = Depends(get_db),form_data: OAuth2PasswordRequestForm = Depends()):
    user =crud.authenticate_user(db,form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token =crud.create_access_token(
        data={"sub": user.email, "scopes": form_data.scopes}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_active_user(
    current_user: schemas.User= Security(get_current_user, scopes=["me"])
):
    #if current_user.is_active==True:
        #raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@router.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    return current_user




@router.post("/users/me", response_model=schemas.User,tags=["Users"])
async def create_user(user: schemas.UserCreate,current:schemas.User=Depends(get_current_active_user), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)





@router.get("/users/me", response_model=List[schemas.User],tags=["Users"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),current:schemas.User=Depends(get_current_active_user)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.delete("/users/{user_id}", response_model=List[schemas.User],tags=["Users"])
def delete_User(user_id:int ,db: Session = Depends(get_db),current:schemas.User=Depends(get_current_active_user)):
    items = crud.get_delete_users(db=db,user_id=user_id)



@router.get("/users/{user_id}", response_model=schemas.User,tags=["Users"])
def read_user(user_id: int, db: Session = Depends(get_db),current:schemas.User=Depends(get_current_active_user)):
    db_user = crud.get_user_name(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.patch("/users/{user_id}", response_model=schemas.User,tags=["Users"])
def update_email(
    user_id:int,user: schemas.UserCreate, db: Session = Depends(get_db),current:schemas.User=Depends(get_current_active_user)
):
    return crud.user_update(db=db,user=user,user_id=user_id)













