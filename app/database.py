from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
from urllib.parse import quote

## SQLALCHEMY_DATABASE_URL --> "postgresql://<user-name>:<password>@<ip-address>/<host-name>/<database-name>"
SQLALCHEMY_DATABASE_URL = f"{settings.db}://{settings.db_user}:%s@{settings.db_host}:{settings.db_port}/{settings.db_name}" % quote(settings.db_password)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

## Dependency
def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()