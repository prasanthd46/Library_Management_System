from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import crud, schemas, security
from database import get_db


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)

@router.post('/register',response_model=schemas.User)
def register_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detial="Email already registered"
        )
    return crud.create_user(db=db, user=user)

@router.post("/login",response_model=schemas.Token)
def login_user(login_data: OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db)):
    
    user = crud.get_user_by_email(db,email=login_data.username)
    
    if not user or not security.verify_password(login_data.password,user.password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        ) 
        
    token_data = {"sub":user.email}
    access_token = security.create_access_token(data=token_data)
    return {"access_token": access_token, "token_type": "bearer"}