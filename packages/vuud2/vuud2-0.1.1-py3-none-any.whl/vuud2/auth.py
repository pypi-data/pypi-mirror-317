# from fastapi import Depends, HTTPException
# from sqlalchemy.orm import Session
# from . import crud
# from .db import get_db

# def authenticate_user(db: Session, email: str, password: str):
#     user = crud.get_user_by_email(db, email)
#     if not user or user.password != password:
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     return user

# def verify_role(
#     user_email: str,
#     required_role: str,
#     db: Session = Depends(get_db)  
# ):
#     user = crud.get_user_by_email(db, user_email)
#     if not user or user.role != required_role:
#         raise HTTPException(status_code=403, detail="Not enough permissions")
#     return user  
