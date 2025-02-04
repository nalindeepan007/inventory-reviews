
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from urllib.parse import urlparse
from sqlalchemy.ext.declarative import declarative_base



tmpPostgres = urlparse(os.getenv("DATABASE_URL"))




syncEngine = create_engine(f"postgresql://{tmpPostgres.username}:{tmpPostgres.password}@{tmpPostgres.hostname}{tmpPostgres.path}", echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=syncEngine)
Base = declarative_base()


