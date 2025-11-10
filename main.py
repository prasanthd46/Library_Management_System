from fastapi import FastAPI

from routers import borrow
import models

from database import engine
from routers import authors,auth,book,borrow
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(auth.router)
app.include_router(authors.router)
app.include_router(book.router)
app.include_router(borrow.router)

@app.get('/')
def read_root():
    return {"message":"Welcome to Library Management System API"}
