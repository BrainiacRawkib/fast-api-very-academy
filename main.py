import os

from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db
from dotenv import load_dotenv
from models import Book, Author
from schemas import Book as BookSchema, Author as AuthorSchema


load_dotenv('.env')

app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DB_URL'])


@app.get('/')
async def root():
    return {'msg': 'FastAPI & Docker bolts like crazy'}


@app.post('/add-book/', response_model=BookSchema)
def add_book(book: BookSchema):
    db_book = Book(title=book.title, rating=book.rating, author_id=book.author_id)
    db.session.add(db_book)
    db.session.commit()
    return db_book


@app.post('/add-author/', response_model=AuthorSchema)
def add_author(author: AuthorSchema):
    db_author = Author(name=author.name, age=author.age)
    db.session.add(db_author)
    db.session.commit()
    return db_author
