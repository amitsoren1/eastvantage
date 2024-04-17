# Python - Assignment - FastAPI

### Python 3.11.4

## Steps to run the server
```
git clone https://github.com/amitsoren1/eastvantage.git
cd eastvantage/fastapi
pip install -r requirements.txt
uvicorn main:app
```

## How to use this app
- visit http://127.0.0.1:8000/docs to access all APIs

## http://127.0.0.1:8000/book
- make `POST` request to a add a new book in this format
    ```
    {
        "title": "book title",
        "author": "book author name",
        "publication_year": 1000
    }
    ```
- make `GET` request to get all books
- To filter books by `author` and `publication_year` add in query like following examples:
    -   to filter by `author` http://127.0.0.1:8000/book?author=author name
    -   to filter by `publication_year` http://127.0.0.1:8000/book?publication_year=1000
    -   to filter by `author` and `publication_year` http://127.0.0.1:8000/book?author=author name&publication_year=1000

## http://127.0.0.1:8000/review
- make `POST` request to a add a new review in this format
    ```
    {
        "book_id": 1,
        "review_text": "good book",
        "rating": 1
    }
    ```
- make `GET` request to get all reviews


## Steps to run tests
```
git clone https://github.com/amitsoren1/eastvantage.git
cd eastvantage/fastapi
pip install -r requirements.txt
pip install pytest httpx
```

- **for windows**
    ```
    set PYTHONPATH=.
    ```

- **for linux**
    ```
    export PYTHONPATH=.
    ```

```
pytest .
```