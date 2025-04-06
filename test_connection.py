from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text  # 이거 추가!
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

try:
    with app.app_context():
        # DB 연결 테스트용 쿼리
        db.session.execute(text('SELECT 1'))  # ← 여기 수정
        print("✅ 데이터베이스 연결 성공!")
except Exception as e:
    print("❌ 데이터베이스 연결 실패:")
    print(e)
