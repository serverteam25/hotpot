import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))  # <- 이거 중요
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hotpot-music-review-app-secret-key'
    SQLALCHEMY_DATABASE_URI = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
