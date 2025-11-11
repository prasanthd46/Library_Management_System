from datetime import datetime, timezone
from sqlalchemy import Column, Date, Integer, String, Boolean, ForeignKey,DateTime
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    
    borrow_records=relationship("Borrow",back_populates="user")

class Author(Base):
    __tablename__ = "authors"
    
    id = Column(Integer, primary_key=True,index=True)
    name= Column(String, index=True, nullable= False)
    bio = Column(String, nullable=True)
    
    books = relationship("Book",back_populates="author",cascade="delete,delete-orphan")

class Book(Base):
    __tablename__ = "books"
    
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String,index=True,nullable=False)
    publication_date = Column(Date, nullable=True)
    is_available=Column(Boolean,default=True)
    
    author_id=Column(Integer,ForeignKey("authors.id"),nullable=False)
    author= relationship("Author",back_populates="books")

    borrow_records=relationship("Borrow",back_populates="book")

class Borrow(Base):
    __tablename__= "borrow_record"
    
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("users.id",ondelete="Cascade"),nullable=False)
    book_id = Column(Integer,ForeignKey("books.id",ondelete="Cascade"),nullable=False)
    
    date_borrowed=Column(DateTime(timezone=True),nullable=False,default=lambda: datetime.now(timezone.utc))
    date_returned=Column(DateTime(timezone=True),nullable=True)

    book = relationship("Book", back_populates="borrow_records")
    user = relationship("User", back_populates="borrow_records")