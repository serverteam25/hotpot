# Hotpot Music 🔥

음악 앨범 관리 및 명곡 월드컵 웹 애플리케이션

## 시작하기

### 1. 필수 요구사항

- Python 3.9 이상 (https://www.python.org/downloads/)
- MySQL 8.0 이상 (https://dev.mysql.com/downloads/mysql/)
- Last.fm API 키 (https://www.last.fm/api/account/create 에서 발급)

### 2. 환경 설정

1. 저장소 클론
```bash
git clone https://github.com/yourusername/hotpot.git
cd hotpot
```

2. 가상환경 생성 및 활성화
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

4. 환경 변수 설정 -> 내가 .env.example 만들어놨으니까 
이거 .env 으로만 바꾸고, 사용하셈
`.env` 파일을 프로젝트 루트 디렉토리에 생성하고 다음 
내용을 입력:
```
# Database Configuration
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_NAME=hotpot

# Last.fm API Configuration
LASTFM_API_KEY=your_lastfm_api_key

# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
# 아래 SECRET_KEY는 반드시 변경하여 사용하세요
SECRET_KEY=please_change_this_to_your_random_secret_key
```

### 3. 데이터베이스 설정

1. MySQL 서버 실행 확인
```bash
# Windows의 경우
net start mysql

# macOS의 경우
brew services start mysql

# Linux의 경우
sudo service mysql start
```

2. MySQL에서 데이터베이스 생성:
```bash
# MySQL에 접속
mysql -u root -p
```

```sql
-- MySQL 프롬프트에서 실행
CREATE DATABASE hotpot CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

3. 데이터베이스 테이블 생성 및 초기 데이터 설정:
```bash
# 데이터베이스 테이블 생성
python app.py

# 초기 데이터 생성 (샘플 앨범 및 곡 추가) 노래 자동으로 추가하려면 이거 편집하면 됨. 수동 추가도 웹 상에서 가능하게 함. 
python seed_db.py
```

### 4. 애플리케이션 실행

1. 웹 서버 실행
```bash
python app.py
```

2. 웹 브라우저에서 접속
```
http://localhost:5002
```

3. 회원가입 후 로그인
   - 우측 상단의 "회원가입" 클릭
   - 사용자 정보 입력 후 가입
   - 로그인하여 서비스 이용 시작

## 주요 기능

1. **앨범 관리**
   - Last.fm API를 통한 앨범 정보 자동 가져오기
   - 앨범 상세 정보 및 수록곡 관리

2. **명곡 월드컵**
   - 힙합/K-POP 장르별 토너먼트
   - 16강/32강 선택 가능

3. **플레이리스트**
   - 개인 플레이리스트 생성 및 관리
   - 좋아하는 곡 저장

## 데이터베이스 백업 및 복원

### 백업하기
```bash
mysqldump -u root -p hotpot > backup.sql
```

### 복원하기
```bash
mysql -u root -p hotpot < backup.sql
```

## 문제 해결

### 데이터베이스 연결 오류
- MySQL 서버가 실행 중인지 확인
- `.env` 파일의 데이터베이스 설정이 올바른지 확인
- MySQL 비밀번호가 정확한지 확인

### Last.fm API 오류
- API 키가 올바르게 설정되었는지 확인
- `.env` 파일에 API 키가 정확히 입력되었는지 확인
- API 호출 한도(일일 제한)를 초과하지 않았는지 확인

### 초기 데이터 생성 오류
- `seed_db.py` 실행 시 오류가 발생하면 Last.fm API 키가 올바른지 확인
- 데이터베이스 연결 설정이 올바른지 확인
- 이미 데이터가 존재하는 경우 중복 추가되지 않음

### 포트 충돌
기본 포트(5002)가 사용 중인 경우:
1. `app.py` 파일에서 포트 번호 변경
```python
app.run(debug=True, port=5003)  # 또는 다른 포트 번호
```

