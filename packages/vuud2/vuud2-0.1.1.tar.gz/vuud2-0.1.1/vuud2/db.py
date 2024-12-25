# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# Base = declarative_base()

# DB = 'postgresql://postgres:postgres@dbpg/postgres'

# engine = create_engine(DB)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# def get_db(): 
#    db = SessionLocal()
#    try:
#        yield db
#    finally:
#        db.close() 