import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hotpot-music-review-app-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://root:password@localhost/hotpot_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False 