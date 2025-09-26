import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

# Lấy DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("❌ DATABASE_URL is missing. Please set it in .env")

# Debug: in host để chắc chắn trỏ đúng Neon
parsed = urlparse(DATABASE_URL)
print("DB HOST =", parsed.hostname)   # phải in ra *.neon.tech

# Tạo engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # tránh connection chết khi Neon scale-to-zero
    pool_size=5,
    max_overflow=10,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# JWT Config
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))