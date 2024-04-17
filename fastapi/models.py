import sqlalchemy as sa
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Book(Base):
    __tablename__ = "Books"

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.Text, nullable=False)
    author = sa.Column(sa.Text, nullable=False)
    publication_year = sa.Column(sa.Integer, nullable=False)
    reviews = relationship("Review")


class Review(Base):
    __tablename__ = "Reviews"

    id = sa.Column(sa.Integer, primary_key=True)
    review_text = sa.Column(sa.Text, nullable=False)
    rating = sa.Column(sa.Integer, nullable=False)
    book_id = sa.Column(sa.Integer, sa.ForeignKey("Books.id", ondelete="CASCADE"))
    book = relationship("Book", back_populates="reviews")
