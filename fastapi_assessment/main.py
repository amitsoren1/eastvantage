from contextlib import asynccontextmanager
from typing import List
from fastapi import BackgroundTasks, Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from crud import add_book, add_review, list_books, list_reviews, send_confirmation_email
from database import get_db, engine
from models import Base
from schemas import BookSchema, BookSchemaResponse, ReviewSchema, ReviewSchemaResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(summary="Assessment", lifespan=lifespan)


@app.get("/book", response_model=List[BookSchemaResponse], status_code=200)
async def get_books(author: str = None, publish_year: int = None, db: AsyncSession = Depends(get_db)):
    return await list_books(db, author, publish_year)


@app.post("/book", response_model=BookSchemaResponse, status_code=201)
async def create_book(book_schema: BookSchema, db: AsyncSession = Depends(get_db)):
    return await add_book(db, book_schema)

@app.get("/review", response_model=List[ReviewSchemaResponse], status_code=200)
async def get_reviews(db: AsyncSession = Depends(get_db)):
    return await list_reviews(db)

@app.post("/review", response_model=ReviewSchemaResponse, status_code=201)
async def submit_review(review_schema: ReviewSchema, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    review = await add_review(db, review_schema)
    background_tasks.add_task(send_confirmation_email, "user@email.com", message="Your review has been submitted")
    return review
