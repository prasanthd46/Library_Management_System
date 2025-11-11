from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from typing import List, Optional

from security import get_current_user
import crud, models, schemas
from database import get_db



router = APIRouter(
    tags=["Borrow"]
)

@router.post('/api/v1/borrow',response_model=schemas.BorrowRecord)
def borrow_book(borrow_request:schemas.BorrowCreate,db:Session= Depends(get_db),current_user:schemas.User = Depends(get_current_user)):
    record = crud.borrow_book(db=db,book_id = borrow_request.book_id,user_id=current_user.id)
    if record == "Not_found":
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail="Book is not found"
        )
    
    if record == "Not_available":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Book is not available"
        )
        
    return record

@router.post("/api/v1/return/{record_id}", response_model=schemas.BorrowRecord)
def return_borrow_book(  record_id: int,db: Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    record = crud.return_book(db=db, record_id=record_id)
    
    if record == "Not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Borrow record not found"
        )
        
    if record == "Book_Returned":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="This book has already been returned"
        )
        
    return record


@router.get("/api/v1/borrow/history", response_model=List[schemas.BorrowRecord])
def get_my_borrow_history( db: Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):

    history = crud.get_borrow_history(db=db, user_id=current_user.id)
    
    return history