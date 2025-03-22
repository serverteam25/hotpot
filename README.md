# Hotpot - 음악 앨범 및 플레이리스트 관리 웹 애플리케이션

Hotpot은 사용자가 음악 앨범을 관리하고, 노래를 플레이리스트에 추가하여 자신만의 음악 컬렉션을 만들 수 있는 웹 애플리케이션입니다. YouTube 링크를 통해 음악을 재생하고 앨범에 대한 리뷰를 작성할 수 있는 기능도 제공합니다.-> 이 커맨트 참고. + 이미지 커버 추가할 땐 copy image address 를 해야함. // 트랙은 아직 하나씩 추가를 해야함. 

## 주요 기능

- 사용자 인증(회원가입, 로그인, 로그아웃)
- 앨범 추가, 수정, 삭제 기능
- 노래 추가, 수정, 삭제 기능
- 플레이리스트 생성 및 관리 기능
- YouTube 링크를 통한 음악 재생 기능
- 앨범 리뷰 작성 및 별점 평가 기능
- 앨범 및 노래 검색 기능
- API 엔드포인트를 통한 JSON 데이터 제공
=> 교수님이 말씀하신 조건 만족 
## 설치 방법

### 사전 요구사항

- Python 3.9 이상
- Conda (또는 다른 가상환경 관리자)

### 설치 단계

1. 저장소 클론하기:
   ```bash
   git clone https://github.com/yourusername/hotpot.git
   cd hotpot
   ```

2. Conda를 사용하여 가상환경 생성 및 활성화:
   ```bash
   conda create -n hotpot python=3.9
   conda activate hotpot
   ```

3. 필요한 패키지 설치:
   ```bash
   pip install -r requirements.txt
   ```

4. 데이터베이스 초기화:
   ```bash
   python reset_db.py
   ```

5. (선택 사항) 테스트 데이터 추가: -> 이건 일단 안 해도 됨 
   ```bash
   # 아래 명령은 예시일 뿐, 실제 테스트 데이터 추가 스크립트가 있다면 해당 명령을 실행
   # python seed_db.py
   ```

## 실행 방법

1. 가상환경이 활성화되어 있는지 확인:
   ```bash
   conda activate hotpot
   ```

2. 애플리케이션 실행:
   ```bash
   python app.py
   ```

3. 웹 브라우저에서 다음 주소로 접속:
   ```
   http://127.0.0.1:5002
   ```

## 알려진 이슈 및 해결 방법

### 패키지 버전 충돌 문제

`url_quote` 관련 오류 메시지가 나타나는 경우, 패키지 버전 충돌 문제일 가능성 높음. 다음과 같이 해결. 

1. 정확한 버전의 Flask와 Werkzeug 설치:
   ```bash
   pip install Flask==2.0.1 Werkzeug==2.0.1
   ```

2. 가상환경을 새로 생성하여 clean install 시도:
   ```bash
   conda deactivate
   conda env remove -n hotpot
   conda create -n hotpot python=3.9
   conda activate hotpot
   pip install -r requirements.txt
   ```

### 포트 충돌 문제

포트가 이미 사용 중이라는 메시지가 나오는 경우:

1. 실행 중인 Flask 애플리케이션이 있는지 확인:
   ```bash
   # macOS/Linux
   lsof -i :5002
   
   # Windows
   netstat -ano | findstr :5002
   ```

2. 실행 중인 프로세스를 종료하거나, app.py 파일에서 다른 포트를 사용하도록 수정:
   ```python
   # app.py 파일의 마지막 줄을 수정
   app.run(debug=True, port=5003)  # 다른 포트 번호 사용
   ```

## 데이터베이스 관리

이 프로젝트는 SQLite 데이터베이스를 사용합니다. 데이터베이스 파일은 Git에 포함되지 않으므로, 처음 clone 후에는 반드시 초기화해야 합니다.
-> 그래서 내가 올린 앨범들은 안 뜰거야. 어차피 테스트 레포라 ㅇㅇ 
1. 데이터베이스 초기화:
   ```bash
   python reset_db.py
   ```

2. 데이터베이스 백업 (선택 사항):
   ```bash
   # SQLite 데이터베이스 백업 예시
   sqlite3 hotpot.db .dump > backup.sql
   ```

## 기여 방법 
주의: 절대 전체를 push 하려 하지 말고, 본인이 편집한 건 
commit message에 편집한 파일 명 기재 필수!!! 
관리 힘들어짐. 그냥 톡으로 먼저 말하고 하자!! 
1. 저장소 포크하기
2. 기능 브랜치 생성하기 (`git checkout -b feature/amazing-feature`)
3. 변경 사항 커밋하기 (`git commit -m 'Add some amazing feature'`)
4. 브랜치에 푸시하기 (`git push origin feature/amazing-feature`)
5. Pull Request 열기

