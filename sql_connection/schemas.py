from typing import List, Optional
from pydantic import BaseModel

#inherit from pydantic model so we can map them with paramters
class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None

'''
And create an ItemCreate and UserCreate that inherit from them (so they will have the same attributes), plus any additional data (attributes) needed for creation.
'''
class ItemCreate(ItemBase):
    pass

#for reading
class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

#inherit from pydantic model so we can map them with paramters
class UserBase(BaseModel):
    email: str

#But for security, the password won't be in other Pydantic models, for example, it won't be sent from the API when reading a user.

class UserCreate(UserBase):
    password: str

#for reading
class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True