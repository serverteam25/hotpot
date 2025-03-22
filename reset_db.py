from app import app, db
import os

# 애플리케이션 컨텍스트 내에서 실행
with app.app_context():
    # 외래 키 제약 조건 비활성화 (MySQL)
    from sqlalchemy import text
    db.session.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.session.commit()
    
    # 테이블 모두 삭제 후 다시 생성
    db.drop_all()
    db.create_all()
    
    # 외래 키 제약 조건 다시 활성화
    db.session.execute(text("SET FOREIGN_KEY_CHECKS=1"))
    db.session.commit()
    
    print("데이터베이스가 초기화되었습니다.") 