from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = (
    "postgresql+psycopg2://postgres:Mahadev3%40@127.0.0.1:5432/supplymind"
)

engine = create_engine( # This creates the connection mechanism to PostgreSQL.
    DATABASE_URL, 
    echo=True # prints SQL statements in the terminal
)

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

Base = declarative_base() # Every Entity/Model will inherit from Base. Similar to @Entity in Java

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

""" 
Similar to 
    try {
        return connection;
    } finally {
        connection.close();
    }
"""