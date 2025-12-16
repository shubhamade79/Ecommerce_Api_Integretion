from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Define Base
Base = declarative_base()
# 3. Database URL
DATABASE_URL = "postgresql://postgres:root@localhost:5432/ecom"
# 4. Create engine
engine = create_engine(DATABASE_URL)
# 5. Create a session
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)





