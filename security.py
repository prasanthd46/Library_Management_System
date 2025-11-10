from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError,jwt
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from typing import Optional
import os

import crud
from database import get_db

from dotenv import load_dotenv

load_dotenv()

ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
SECRET_KEY = os.getenv("SECRET_KEY")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password:str,hashed_password:str):
    
    return password_context.verify(plain_password,hashed_password)

def get_password_hash(password:str):
    return password_context.hash(password)




def create_access_token(data:dict):
    
    data_encode = data.copy()
    
    expire_time = datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_encode.update({"exp":expire_time})
    encoded_jwt=jwt.encode(data_encode,SECRET_KEY,algorithm=ALGORITHM)
    
    return encoded_jwt


def get_current_user(token:str= Depends(oauth2_scheme),db:Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )
    
    try:
        payload = jwt.decode(token,SECRET_KEY,ALGORITHM)
        email:str = payload.get("sub")
        if email is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    
    user = crud.get_user_by_email(db,email=email)
    
    if user is None:
        raise credentials_exception
    
    return user

