from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./service.db"
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://service:s7mitPN55ZwCwWJj@127.0.0.1:3306/service?charset=utf8mb4"
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:password@hostname/dbname?charset=uft8"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False},
    # pool_size=20, max_overflow=100
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

Base.metadata.create_all(engine)

Session = sessionmaker(engine)()