from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base


databaseUrl = "postgresql://postgres:postgres@localhost:5432/trainbooking"

engine = create_engine(databaseUrl)
sessionLocal = sessionmaker(bind=engine,autocommit = False)

def get_db():
    db = sessionLocal()
    try :
        yield db
    finally:
        db.close()

Base = declarative_base()