# from fastapi import APIRouter, Depends, HTTPException
# from . import schemas, auth, crud, models
# from .db import get_db
# from sqlalchemy.orm import Session


# router = APIRouter()

# @router.post("/login/")
# def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     authenticated_user = auth.authenticate_user(db, user.email, user.password)
#     return {"message": f"Welcome, {authenticated_user.email}", "role": authenticated_user.role}


# @router.get("/users/{user_id}", response_model=schemas.User)
# def get_user(user_email: str, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, user_email)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# @router.get("/readers/{reader_id}", response_model=schemas.Reader)
# def get_reader(reader_id: int, db: Session = Depends(get_db)):
#     db_reader = crud.get_reader_by_id(db, reader_id)
#     if db_reader is None:
#         raise HTTPException(status_code=404, detail="Reader not found")
#     return db_reader


# @router.post("/books/", response_model=schemas.Book)
# def create_book(book: schemas.BookCreate, db: Session = Depends(get_db), user: schemas.User = Depends(auth.verify_role)):
#     if user.role != 'manager':
#         raise HTTPException(status_code=403, detail="Not enough permissions")
#     return crud.create_book(db, book)


# @router.get("/books/", response_model=list[schemas.Book])
# def get_books(db: Session = Depends(get_db)):
#     return db.query(models.Book).all()


# @router.get("/books/{book_id}/instances", response_model=list[schemas.BookInstance])
# def get_book_instances(book_id: int, db: Session = Depends(get_db)):
#     return crud.get_book_instances(db, book_id)


# @router.post("/books/{instance_id}/borrow")
# def borrow_book(instance_id: int, db: Session = Depends(get_db), user: schemas.User = Depends(auth.verify_role)):
#     if user.role != 'reader':
#         raise HTTPException(status_code=403, detail="Not enough permissions")
#     return crud.borrow_book(db, instance_id)

# @router.post("/books/search/{title}")
# def search_book(title: str, db: Session = Depends(get_db)):
#     return crud.search_book(db, title)

# @router.post("/create-user/")
# def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
#     return crud.create_user(db, user)