# models

# from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
# from sqlalchemy.orm import relationship
# from .db import Base

# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True)
#     password = Column(String)  
#     role = Column(String)  # 'reader' или 'manager' 

#     reader = relationship("Reader", back_populates="user", uselist=False)

# class Reader(Base):
#     __tablename__ = "readers"
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     reader_number = Column(String, unique=True)
#     passport_number = Column(String, unique=True)
#     full_name = Column(String)
#     address = Column(String)
#     workplace = Column(String)
#     age = Column(Integer)

#     user = relationship("User", back_populates="reader")

# class Book(Base):
#     __tablename__ = "books"
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     author = Column(String)
#     publisher = Column(String)
#     year = Column(Integer)
#     pages = Column(Integer)
#     code = Column(String, unique=True)

# class BookInstance(Base):
#     __tablename__ = "book_instances"
#     id = Column(Integer, primary_key=True, index=True)
#     book_id = Column(Integer, ForeignKey("books.id"))
#     inventory_number = Column(String, unique=True)
#     is_borrowed = Column(Boolean, default=False)

#     book = relationship("Book", back_populates="instances")

# Book.instances = relationship("BookInstance", back_populates="book")


