from datetime import datetime,date
from pydantic import BaseModel, EmailStr,Field
from typing import Optional





class AuthorBase(BaseModel):
    name:str
    bio:Optional[str]=None

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id:int
    class Config:
        from_attributes = True


class BookBase(BaseModel):
    title:str

class BookCreate(BookBase):
    author_id:int
    publication_date: Optional[date] = None

class BookUpdate(BaseModel):
    title:Optional[str]=None
    publication_date: Optional[date] = None
    author_id:Optional[int]=None
    is_available:Optional[bool]=None

class Book(BookBase):
    id:int
    author_id:int
    is_available:bool
    author:Author
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email:EmailStr

class UserCreate(UserBase):
    password:str=Field(...,max_length=72)
    is_admin:Optional[bool]=False
    
class User(UserBase):
    id:int
    is_admin:bool
    class Config:
        from_attributes = True       


class Token(BaseModel):
    access_token:str
    token_type:str


class BorrowCreate(BaseModel):
    book_id: int


class BorrowRecord(BaseModel):
    id: int
    date_borrowed: datetime
    date_returned: Optional[datetime] = None
    user: User 
    book: Book
    class Config:
        from_attributes = True
