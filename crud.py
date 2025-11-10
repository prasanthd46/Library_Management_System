
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import DateTime
from sqlalchemy.orm import Session

import models,schemas,security


def create_author(db:Session,author:schemas.AuthorCreate):
    
    author_data =author.model_dump()
    
    author_record = models.Author(**author_data)
    db.add(author_record)
    db.commit()
    db.refresh(author_record)
    
    return author_record

def get_author(db:Session,author_id:int):
    
    author_data = db.query(models.Author).filter(models.Author.id == author_id).first()
    return author_data
    
def get_authors(db:Session,skip:int=0,limit:int=100):
    
    authors_data = db.query(models.Author).offset(skip).limit(limit).all()
    return authors_data

def get_user(db:Session,user_id:int):
    
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db:Session,email:str):
    
    return db.query(models.User).filter(models.User.email == email.lower()).first()

def create_user(db:Session,user:schemas.UserCreate):
    plain_password = user.password
    hashed_password = security.get_password_hash(plain_password)
    
    user_record = models.User(
        email=user.email.lower(),
        password=hashed_password,
        is_admin=user.is_admin
    )
    db.add(user_record)
    db.commit()
    db.refresh(user_record)
    
    return user_record


def create_book(db:Session,book:schemas.BookCreate):
    db_author = get_author(db,author_id=book.author_id)
    if not db_author:
        return None
    
    
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    
    return db_book

def get_book(db:Session,book_id:int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_books(db:Session,skip:int = 0,limit:int=100,search:Optional[str]=None,is_available:Optional[bool]=None):
    books = db.query(models.Book)
    
    if is_available is not None:
        books = books.filter(models.Book.is_available == is_available)
    
    if search:
        books = books.filter(models.Book.title.ilike(f"%{search}%"))
        
    return books.offset(skip).limit(limit).all()

def update_book(db:Session,book_id:int,book_update:schemas.BookUpdate):
    
    db_book = get_book(db=db, book_id=book_id)
    
    if db_book is None:
        return None

    update_data = book_update.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_book, key, value)
        
    
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    
    return db_book

def remove_book(db:Session,book_id:schemas.BookBase):
    
    db_book = get_book(db=db,book_id=book_id)
    
    if db_book is None:
        return None
    
    db.delete(db_book)
    db.commit()
    return db_book

def borrow_book(db:Session,book_id:int,user_id:int):
    db_book = get_book(db,book_id)
    
    if db_book is None:
        return "Not_found"
    
    if not db_book.is_available:
        return "Not_available"
    
    
    db_borrow_record = models.Borrow(
        book_id=book_id,
        user_id=user_id
    )
    
    db_book.is_available = False
    
    db.add(db_borrow_record)
    db.add(db_book)
    
    db.commit()
    db.refresh(db_borrow_record)
    
    return db_borrow_record

def return_book(db:Session,record_id:int):
    db_borrow_record = db.query(models.Borrow).filter(models.Borrow.id == record_id).first()
    
    if db_borrow_record is None:
        return "Not_found"
    
    if db_borrow_record.date_returned is not None:
        return "Book_Returned"
    
    db_borrow_record.date_returned=datetime.now(timezone.utc)
    
    db_borrow_record.book.is_available = True
    
    db.add(db_borrow_record.book)
    db.add(db_borrow_record)
    
    db.commit()
    db.refresh(db_borrow_record)
    
    return db_borrow_record

def get_borrow_history(db:Session,user_id):
    
    db_borrow_records = db.query(models.Borrow).filter(models.Borrow.user_id == user_id).order_by(models.Borrow.date_borrowed.desc()).all()
    
    if db_borrow_records is None:
        return "Not_Found"
    
    return db_borrow_records

