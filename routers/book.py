from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional


import crud, models, schemas
from database import get_db
from security import get_current_user



router = APIRouter(
    prefix="/api/v1/books",  
    tags=["Books"]            
)


@router.post("/",response_model=schemas.BookCreate)
def create_newbook(book:schemas.BookCreate,db:Session=Depends(get_db),current_user:models.User = Depends(get_current_user)):
    db_book = crud.create_book(db,book)
    if db_book is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found for book"
        ) 
    
    return db_book

@router.get("/",response_model=List[schemas.Book])
def read_books(db:Session=Depends(get_db),skip:int =0,limit:int=100,search:Optional[str]=None,is_available:Optional[bool]=None,current_user:schemas.User = Depends(get_current_user)):
    
    books = crud.get_books(db=db,skip=skip,limit=limit,search=search,is_available=is_available)
    
    return books

@router.get("/{book_id}",response_model= schemas.Book)
def read_book(book_id:int,db:Session=Depends(get_db),current_user: models.User = Depends(get_current_user)):
    book = crud.get_book(db=db,book_id=book_id)
    if book is None:
        raise HTTPException(
            status_code = 404,
            detail="Book is not found"
        )
    
    return book

@router.patch('/{book_id}',response_model=schemas.Book)
def update_book(book_id:int,book_update:schemas.BookUpdate,db:Session=Depends(get_db),current_user:schemas.User = Depends(get_current_user)):
    if book_update.author_id is not None:
        db_author = crud.get_author(db, author_id=book_update.author_id)
        if db_author is None:
            raise HTTPException(
                status_code=404, 
                detail="Author not found for the book"
            )
    db_book = crud.update_book(
        db=db, 
        book_id=book_id, 
        book_update=book_update
    )

    if db_book is None:
        raise HTTPException(
            status_code=404, 
            detail="Book is not found"
        )
        
    return db_book


@router.delete('/{book_id}',response_model=schemas.BookBase)
def delete_book(book_id:int,db:Session=Depends(get_db),current_user:schemas.User= Depends(get_current_user)):
    db_book = crud.remove_book(db=db,book_id=book_id)
    if db_book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found "
        )
    return db_book

