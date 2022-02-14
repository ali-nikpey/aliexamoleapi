from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'


engin = create_engine(SQLALCHEMY_DATABASE_URL)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engin)

Base = declarative_base()


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

#
# try:
#     con = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='980241066', cursor_factory=RealDictCursor)
#     cursor = con.cursor()
#     print("Database successfully connected!")
# except Exception as error:
#     print("connecting to Database failed!!")
#     print("error: ", error)
