from pydantic import BaseModel, Field


class BookSchema(BaseModel):
    title: str
    author: str
    publication_year: int = Field(gt=0, description="Year of publish of the book")

class BookSchemaResponse(BookSchema):
    id : int

class BookUpdateSchema(BookSchemaResponse):
    pass

class ReviewSchema(BaseModel):
    book_id: int
    review_text: str
    rating: int = Field(gt=0, lt=11, description="Rating of book on scale of 1 to 10")

class ReviewSchemaResponse(ReviewSchema):
    id : int

class ReviewUpdateSchema(ReviewSchemaResponse):
    pass
