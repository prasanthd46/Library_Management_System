from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from typing import List
from models import User

import crud,schemas,security
from database import get_db

router = APIRouter(
    prefix="/api/vi/authors",
    tags=["Authors"]
)


@router.post("/",response_model=schemas.Author)
def create_new_author(author:schemas.AuthorCreate,db:Session = Depends(get_db),current_user: User = Depends(security.get_current_user)):
    author = crud.create_author(db,author=author)
    return author

@router.get("/",response_model=List[schemas.Author])
def read_authors(db:Session= Depends(get_db),skip:int=0,limit:int=100,adb:Session=Depends(get_db),current_user: User = Depends(security.get_current_user)):
    authors = crud.get_authors(db=db,skip=skip,limit=limit)
    return authors

@router.get("/{author_id}",response_model=schemas.Author)
def read_author(author_id:int,db:Session=Depends(get_db),current_user: User = Depends(security.get_current_user)):
    db_author=crud.get_author(db=db,author_id=author_id)
    if(db_author is None):
        raise HTTPException(status_code=404,detail="Author not found")
    
    return db_author