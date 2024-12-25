# from pydantic import BaseModel
# from typing import Optional

# class UserBase(BaseModel):
#     email: str
#     role: str 

# class UserCreate(UserBase):
#     password: str 

# class User(UserBase):
#     id: int

#     class Config:
#         orm_mode = True

# class CreateUser(UserBase):
#     password: str


# class ReaderBase(BaseModel):
#     reader_number: str
#     passport_number: str
#     full_name: str
#     address: str
#     workplace: str
#     age: int

# class ReaderCreate(ReaderBase):
#     pass

# class Reader(ReaderBase):
#     id: int
#     user_id: int 

#     class Config:
#         orm_mode = True

# class BookBase(BaseModel):
#     title: str
#     author: Optional[str] = None
#     publisher: str
#     year: int
#     pages: int
#     code: str
    

# class BookCreate(BookBase):
#     pass

# class Book(BookBase):
#     id: int

#     class Config:
#         orm_mode = True

# class BookInstanceBase(BaseModel):
#     inventory_number: str
#     book_id: int
#     is_borrowed: bool = False

# class BookInstance(BookInstanceBase):
#     id: int

#     class Config:
#         orm_mode = True
