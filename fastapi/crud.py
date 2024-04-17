import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException, status

from models import Book, Review
from schemas import BookSchema, BookUpdateSchema, ReviewSchema, ReviewUpdateSchema


async def list_books(session: AsyncSession, author: str, publish_year: int):
    if author and publish_year:
        result = await session.execute(select(Book).where(Book.author == author and Book.publication_year == publish_year))
    elif author:
        result = await session.execute(select(Book).where(Book.author == author))
    elif publish_year:
        result = await session.execute(select(Book).where(Book.publication_year == publish_year))
    else:
        result = await session.execute(select(Book))
    #     result = await session.execute(select(Book).options(selectinload(Book.reviews)))
    # for x in result.scalars().all():
    #     print(x.reviews)
    return result.scalars().all()

async def get_book(session: AsyncSession, book_id: int):
    try:
        return (await session.execute(select(Book).where(Book.id == book_id))).scalars().one()
    except NoResultFound:
        raise Exception("Book with id {book_id} not found")

async def update_book(session: AsyncSession, book_id: int, book_schema: BookUpdateSchema):
    try:
        book = (await session.execute(select(Book).where(Book.id == book_id))).scalars().one()
    except NoResultFound:
        raise Exception("Book with id {book_id} not found")
    book.author = book_schema.author
    book.title = book_schema.title
    book.publication_year = book_schema.publication_year

    await session.commit()
    await session.refresh(book)

    return book

async def delete_book(session: AsyncSession, book_id: int):
    try:
        book = (await session.execute(select(Book).where(Book.id == book_id))).scalars().one()
    except NoResultFound:
        return True

    await session.delete(book)

    return True

async def add_book(session: AsyncSession, book_schema: BookSchema):
    new_book = Book(**book_schema.model_dump())
    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)
    return new_book

async def list_reviews(session: AsyncSession):
    result = await session.execute(select(Review))
    return result.scalars().all()

async def add_review(session: AsyncSession, review_schema: ReviewSchema):
    if not (await session.execute(select(Book).where(Book.id == review_schema.book_id))).scalars().first():
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Book with id {review_schema.book_id} not found")
    new_review = Review(**review_schema.model_dump())
    session.add(new_review)
    await session.commit()
    await session.refresh(new_review)
    return new_review

async def get_review(session: AsyncSession, review_id: int):
    try:
        return (await session.execute(select(Review).where(Review.id == review_id))).scalars().one()
    except NoResultFound:
        raise Exception("review with id {review_id} not found")

async def update_review(session: AsyncSession, review_id: int, review_schema: ReviewUpdateSchema):
    try:
        review = (await session.execute(select(Review).where(Review.id == review_id))).scalars().one()
    except NoResultFound:
        raise Exception("review with id {review_id} not found")
    review.book_id = review_schema.book_id
    review.review_text = review_schema.review_text
    review.rating = review_schema.rating

    await session.commit()
    await session.refresh(review)

    return review

async def delete_review(session: AsyncSession, review_id: int):
    try:
        review = (await session.execute(select(Review).where(Review.id == review_id))).scalars().one()
    except NoResultFound:
        return True

    await session.delete(review)

    return True

async def send_confirmation_email(email, message="Your review has been submitted"):
    await asyncio.sleep(5)
