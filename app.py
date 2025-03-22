from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Album, Review, Song, Playlist, PlaylistSong
from config import Config
from datetime import datetime
from sqlalchemy import or_
import re
import requests
import json
from pytube import YouTube, Playlist as PytubePlaylist
import urllib.parse

app = Flask(__name__)
app.config.from_object(Config)

# 데이터베이스 초기화
db.init_app(app)

# 로그인 관리자 초기화
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 데이터베이스 생성
@app.before_first_request
def create_tables():
    db.create_all()

# 홈 페이지
@app.route('/')
def index():
    albums = Album.query.order_by(Album.created_at.desc()).all()
    return render_template('index.html', albums=albums)

# 회원가입
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.')
            return redirect(url_for('register'))
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.')
            return redirect(url_for('register'))
        
        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# 로그인
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not check_password_hash(user.password_hash, password):
            flash('Invalid username or password.')
            return redirect(url_for('login'))
        
        login_user(user)
        return redirect(url_for('index'))
    
    return render_template('login.html')

# 로그아웃
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# 앨범 목록 (JSON API)
@app.route('/api/albums')
def api_albums():
    albums = Album.query.all()
    return jsonify([album.to_dict() for album in albums])

# 앨범 상세 페이지
@app.route('/album/<int:album_id>')
def album_detail(album_id):
    album = Album.query.get_or_404(album_id)
    songs = Song.query.filter_by(album_id=album_id).order_by(Song.track_number).all()
    
    # 로그인한 사용자의 플레이리스트 가져오기
    playlists = []
    if current_user.is_authenticated:
        playlists = Playlist.query.filter_by(user_id=current_user.id).all()
    
    # 앨범 리뷰 가져오기
    reviews = Review.query.filter_by(album_id=album_id).order_by(Review.created_at.desc()).all()
    
    # 현재 사용자가 이미 리뷰를 작성했는지 확인
    user_has_review = False
    if current_user.is_authenticated:
        user_has_review = Review.query.filter_by(
            album_id=album_id, 
            user_id=current_user.id
        ).first() is not None
    
    return render_template(
        'album_detail.html', 
        album=album, 
        songs=songs,
        playlists=playlists,
        reviews=reviews,
        user_has_review=user_has_review
    )

# 장르 목록 (앨범 추가/수정 페이지에서 사용)
GENRES = [
    "팝", "록", "힙합", "R&B", "일렉트로닉", "클래식", "재즈", "컨트리", 
    "포크", "블루스", "레게", "월드", "라틴", "메탈", "펑크", "소울", 
    "인디", "K-Pop", "J-Pop", "트로트", "OST", "그 외"
]

# 새 앨범 추가
@app.route('/add_album', methods=['GET', 'POST'])
@login_required
def add_album():
    if request.method == 'POST':
        title = request.form.get('title')
        artist = request.form.get('artist')
        release_date_str = request.form.get('release_date')
        youtube_url = request.form.get('youtube_url')
        cover_image = request.form.get('cover_image')
        
        # 장르 처리 (체크박스 및 커스텀 장르)
        genre_values = request.form.getlist('genre')
        custom_genre = request.form.get('custom_genre')
        
        if custom_genre:
            genre_values.append(custom_genre)
        
        # 장르 배열을 쉼표로 구분된 문자열로 변환
        genre = ", ".join(genre_values) if genre_values else None
        
        if not title or not artist:
            flash('제목과 아티스트는 필수 입력 항목입니다.', 'danger')
            return redirect(url_for('add_album'))
        
        release_date = None
        if release_date_str:
            try:
                release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('날짜 형식이 올바르지 않습니다. YYYY-MM-DD 형식으로 입력해주세요.', 'danger')
                return redirect(url_for('add_album'))
        
        new_album = Album(
            title=title,
            artist=artist,
            release_date=release_date,
            genre=genre,
            cover_image=cover_image,
            youtube_url=youtube_url
        )
        
        db.session.add(new_album)
        db.session.commit()
        
        flash('앨범이 성공적으로 추가되었습니다!', 'success')
        
        # 유튜브 링크가 있다면 자동으로 곡 추가
        if youtube_url and 'youtube.com' in youtube_url:
            try:
                # 유튜브 플레이리스트에서 곡 정보 가져오기
                songs_info = fetch_songs_from_youtube(youtube_url)
                
                # 각 곡 정보로 노래 생성
                for song_info in songs_info:
                    song = Song(
                        title=song_info.get('title', ''),
                        track_number=song_info.get('track_number'),
                        duration=song_info.get('duration'),
                        youtube_url=song_info.get('youtube_url'),
                        album_id=new_album.id
                    )
                    db.session.add(song)
                
                db.session.commit()
                flash(f'{len(songs_info)}개의 노래가 앨범에 자동으로 추가되었습니다!', 'success')
            except Exception as e:
                flash(f'노래를 자동으로 추가하는 중 오류가 발생했습니다: {str(e)}', 'warning')
        
        return redirect(url_for('album_detail', album_id=new_album.id))
    
    return render_template('add_album.html', genres=GENRES)

# 앨범 수정
@app.route('/edit_album/<int:album_id>', methods=['GET', 'POST'])
@login_required
def edit_album(album_id):
    album = Album.query.get_or_404(album_id)
    
    if request.method == 'POST':
        album.title = request.form.get('title')
        album.artist = request.form.get('artist')
        release_date_str = request.form.get('release_date')
        album.youtube_url = request.form.get('youtube_url')
        album.cover_image = request.form.get('cover_image')
        
        # 장르 처리 (체크박스 및 커스텀 장르)
        genre_values = request.form.getlist('genre')
        custom_genre = request.form.get('custom_genre')
        
        if custom_genre:
            genre_values.append(custom_genre)
        
        # 장르 배열을 쉼표로 구분된 문자열로 변환
        album.genre = ", ".join(genre_values) if genre_values else None
        
        if not album.title or not album.artist:
            flash('제목과 아티스트는 필수 입력 항목입니다.', 'danger')
            return redirect(url_for('edit_album', album_id=album_id))
        
        if release_date_str:
            try:
                album.release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('날짜 형식이 올바르지 않습니다. YYYY-MM-DD 형식으로 입력해주세요.', 'danger')
                return redirect(url_for('edit_album', album_id=album_id))
        else:
            album.release_date = None
        
        db.session.commit()
        flash('앨범이 성공적으로 수정되었습니다!', 'success')
        return redirect(url_for('album_detail', album_id=album_id))
    
    # 현재 장르를 리스트로 분리
    album_genres = album.genre.split(', ') if album.genre else []
    
    return render_template('edit_album.html', album=album, genres=GENRES, album_genres=album_genres)

# 앨범 삭제
@app.route('/delete_album/<int:album_id>')
@login_required
def delete_album(album_id):
    album = Album.query.get_or_404(album_id)
    
    # 앨범에 속한 노래 목록 가져오기
    songs = Song.query.filter_by(album_id=album_id).all()
    
    # 노래와 연결된 모든 플레이리스트 연결 삭제
    for song in songs:
        PlaylistSong.query.filter_by(song_id=song.id).delete()
    
    # 노래 삭제
    Song.query.filter_by(album_id=album_id).delete()
    
    # 앨범 리뷰 삭제
    Review.query.filter_by(album_id=album_id).delete()
    
    # 앨범 삭제
    db.session.delete(album)
    db.session.commit()
    
    flash('앨범이 성공적으로 삭제되었습니다!')
    return redirect(url_for('index'))

# 노래 추가
@app.route('/add_song/<int:album_id>', methods=['GET', 'POST'])
def add_song(album_id):
    album = Album.query.get_or_404(album_id)
    
    if request.method == 'POST':
        title = request.form.get('title')
        track_number = request.form.get('track_number')
        duration = request.form.get('duration')
        youtube_url = request.form.get('youtube_url')
        
        # 필수 입력값 검증
        if not title:
            flash('노래 제목을 입력해주세요.', 'danger')
            return redirect(url_for('add_song', album_id=album_id))
        
        # 트랙 번호 숫자 변환
        track_num = None
        if track_number:
            try:
                track_num = int(track_number)
            except ValueError:
                flash('트랙 번호는 숫자여야 합니다.', 'danger')
                return redirect(url_for('add_song', album_id=album_id))
        
        # 새 노래 객체 생성
        new_song = Song(
            title=title,
            track_number=track_num,
            duration=duration if duration else None,
            youtube_url=youtube_url if youtube_url else None,
            album_id=album_id
        )
        
        # 데이터베이스에 추가
        db.session.add(new_song)
        db.session.commit()
        
        flash('노래가 추가되었습니다!', 'success')
        return redirect(url_for('album_detail', album_id=album_id))
    
    return render_template('add_song.html', album=album)

# 노래 수정
@app.route('/edit_song/<int:song_id>', methods=['GET', 'POST'])
def edit_song(song_id):
    song = Song.query.get_or_404(song_id)
    
    if request.method == 'POST':
        title = request.form.get('title')
        track_number = request.form.get('track_number')
        duration = request.form.get('duration')
        youtube_url = request.form.get('youtube_url')
        
        # 필수 입력값 검증
        if not title:
            flash('노래 제목을 입력해주세요.', 'danger')
            return redirect(url_for('edit_song', song_id=song_id))
        
        # 데이터 업데이트
        song.title = title
        song.duration = duration if duration else None
        song.track_number = int(track_number) if track_number else None
        song.youtube_url = youtube_url if youtube_url else None
        
        db.session.commit()
        
        flash('노래가 수정되었습니다!', 'success')
        return redirect(url_for('album_detail', album_id=song.album_id))
    
    return render_template('edit_song.html', song=song)

# 노래 삭제
@app.route('/delete_song/<int:song_id>')
@login_required
def delete_song(song_id):
    song = Song.query.get_or_404(song_id)
    album_id = song.album_id
    
    # 노래와 연결된 모든 플레이리스트 연결 삭제
    PlaylistSong.query.filter_by(song_id=song_id).delete()
    
    db.session.delete(song)
    db.session.commit()
    
    flash('노래가 성공적으로 삭제되었습니다!')
    return redirect(url_for('album_detail', album_id=album_id))

# 플레이리스트 목록
@app.route('/playlists')
@login_required
def playlists():
    user_playlists = Playlist.query.filter_by(user_id=current_user.id).all()
    return render_template('playlists.html', playlists=user_playlists)

# 플레이리스트 상세
@app.route('/playlist/<int:playlist_id>')
@login_required
def playlist_detail(playlist_id):
    playlist = Playlist.query.get_or_404(playlist_id)
    
    # 비공개 플레이리스트는 소유자만 볼 수 있음
    if not playlist.is_public and playlist.user_id != current_user.id:
        abort(403)
    
    return render_template('playlist_detail.html', playlist=playlist)

# 플레이리스트 생성
@app.route('/create_playlist', methods=['GET', 'POST'])
@login_required
def create_playlist():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        cover_image = request.form.get('cover_image')
        is_public = 'is_public' in request.form
        
        if not name:
            flash('플레이리스트 이름은 필수 입력 항목입니다.')
            return redirect(url_for('create_playlist'))
        
        new_playlist = Playlist(
            name=name,
            description=description,
            cover_image=cover_image,
            user_id=current_user.id,
            is_public=is_public
        )
        
        db.session.add(new_playlist)
        db.session.commit()
        
        flash('플레이리스트가 성공적으로 생성되었습니다!')
        return redirect(url_for('playlist_detail', playlist_id=new_playlist.id))
    
    return render_template('create_playlist.html')

# 플레이리스트 수정
@app.route('/edit_playlist/<int:playlist_id>', methods=['GET', 'POST'])
@login_required
def edit_playlist(playlist_id):
    playlist = Playlist.query.get_or_404(playlist_id)
    
    # 플레이리스트 소유자만 수정 가능
    if playlist.user_id != current_user.id:
        abort(403)
    
    if request.method == 'POST':
        playlist.name = request.form.get('name')
        playlist.description = request.form.get('description')
        playlist.cover_image = request.form.get('cover_image')
        playlist.is_public = 'is_public' in request.form
        
        if not playlist.name:
            flash('플레이리스트 이름은 필수 입력 항목입니다.')
            return redirect(url_for('edit_playlist', playlist_id=playlist_id))
        
        db.session.commit()
        flash('플레이리스트가 성공적으로 수정되었습니다!')
        return redirect(url_for('playlist_detail', playlist_id=playlist_id))
    
    return render_template('edit_playlist.html', playlist=playlist)

# 플레이리스트 삭제
@app.route('/delete_playlist/<int:playlist_id>')
@login_required
def delete_playlist(playlist_id):
    playlist = Playlist.query.get_or_404(playlist_id)
    
    # 플레이리스트 소유자만 삭제 가능
    if playlist.user_id != current_user.id:
        abort(403)
    
    # 플레이리스트와 노래 연결 삭제
    PlaylistSong.query.filter_by(playlist_id=playlist_id).delete()
    
    db.session.delete(playlist)
    db.session.commit()
    
    flash('플레이리스트가 성공적으로 삭제되었습니다!')
    return redirect(url_for('playlists'))

# 플레이리스트에 노래 추가
@app.route('/add_to_playlist/<int:playlist_id>/<int:song_id>')
@login_required
def add_to_playlist(playlist_id, song_id):
    playlist = Playlist.query.get_or_404(playlist_id)
    song = Song.query.get_or_404(song_id)
    
    # 플레이리스트 소유자만 노래 추가 가능
    if playlist.user_id != current_user.id:
        abort(403)
    
    # 이미 추가된 노래인지 확인
    existing = PlaylistSong.query.filter_by(playlist_id=playlist_id, song_id=song_id).first()
    if existing:
        flash('이 노래는 이미 플레이리스트에 있습니다.')
        return redirect(url_for('playlist_detail', playlist_id=playlist_id))
    
    playlist_song = PlaylistSong(playlist_id=playlist_id, song_id=song_id)
    db.session.add(playlist_song)
    db.session.commit()
    
    redirect_to = request.args.get('redirect_to')
    if redirect_to == 'search_songs':
        query = request.args.get('query', '')
        return redirect(url_for('search_songs', playlist_id=playlist_id, query=query))
    
    flash('노래가 플레이리스트에 추가되었습니다!')
    return redirect(url_for('playlist_detail', playlist_id=playlist_id))

# 플레이리스트에서 노래 제거
@app.route('/remove_from_playlist/<int:playlist_id>/<int:song_id>')
@login_required
def remove_from_playlist(playlist_id, song_id):
    playlist = Playlist.query.get_or_404(playlist_id)
    
    # 플레이리스트 소유자만 노래 제거 가능
    if playlist.user_id != current_user.id:
        abort(403)
    
    playlist_song = PlaylistSong.query.filter_by(playlist_id=playlist_id, song_id=song_id).first_or_404()
    
    db.session.delete(playlist_song)
    db.session.commit()
    
    flash('노래가 플레이리스트에서 제거되었습니다!')
    return redirect(url_for('playlist_detail', playlist_id=playlist_id))

# 노래 검색 및 플레이리스트에 추가
@app.route('/search_songs/<int:playlist_id>')
@login_required
def search_songs(playlist_id):
    playlist = Playlist.query.get_or_404(playlist_id)
    
    # 플레이리스트 소유자만 노래 추가 가능
    if playlist.user_id != current_user.id:
        abort(403)
    
    query = request.args.get('query', '')
    songs = []
    
    if query:
        # 노래 제목, 아티스트 또는 앨범 제목으로 검색
        songs = Song.query.join(Album).filter(
            or_(
                Song.title.ilike(f'%{query}%'),
                Album.artist.ilike(f'%{query}%'),
                Album.title.ilike(f'%{query}%')
            )
        ).all()
    
    # 플레이리스트에 이미 추가된 노래들의 ID 목록
    playlist_song_ids = [ps.song_id for ps in PlaylistSong.query.filter_by(playlist_id=playlist_id).all()]
    
    return render_template(
        'search_songs.html',
        playlist=playlist,
        query=query,
        songs=songs,
        playlist_song_ids=playlist_song_ids
    )

# 플레이리스트에 노래 추가 (API)
@app.route('/add_song_to_playlist/<int:playlist_id>/<int:song_id>', methods=['POST'])
@login_required
def add_song_to_playlist(playlist_id, song_id):
    playlist = Playlist.query.get_or_404(playlist_id)
    song = Song.query.get_or_404(song_id)
    
    # 플레이리스트 소유자만 노래 추가 가능
    if playlist.user_id != current_user.id:
        return jsonify({
            'success': False,
            'message': '이 플레이리스트를 수정할 권한이 없습니다.'
        })
    
    # 이미 추가된 노래인지 확인
    existing = PlaylistSong.query.filter_by(playlist_id=playlist_id, song_id=song_id).first()
    if existing:
        return jsonify({
            'success': False,
            'message': '이 노래는 이미 플레이리스트에 있습니다.'
        })
    
    playlist_song = PlaylistSong(playlist_id=playlist_id, song_id=song_id)
    db.session.add(playlist_song)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '노래가 플레이리스트에 추가되었습니다!'
    })

# 유튜브 링크에서 앨범 정보 가져오기
@app.route('/fetch_album_info', methods=['POST'])
@login_required
def fetch_album_info():
    data = request.json
    youtube_url = data.get('youtube_url')
    
    if not youtube_url:
        return jsonify({
            'success': False,
            'message': '유튜브 URL이 제공되지 않았습니다.'
        })
    
    try:
        # 유튜브 URL에서 앨범 정보 가져오기
        album_info = fetch_album_from_youtube(youtube_url)
        
        return jsonify({
            'success': True,
            'album': album_info
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'앨범 정보를 가져오는 중 오류가 발생했습니다: {str(e)}'
        })

# 유튜브에서 앨범 정보 가져오기
def fetch_album_from_youtube(youtube_url):
    try:
        # 플레이리스트 URL인지 확인
        if 'list=' in youtube_url:
            # 유튜브 플레이리스트 정보 가져오기
            playlist = PytubePlaylist(youtube_url)
            
            # 플레이리스트 제목에서 앨범 제목과 아티스트 추출
            title = playlist.title
            
            # 일반적으로 유튜브 플레이리스트 제목 형식: "앨범명 - 아티스트"
            # 또는 "아티스트 - 앨범명" 형식이 많음
            artist = ""
            album_title = title
            
            if ' - ' in title:
                parts = title.split(' - ', 1)
                if len(parts) == 2:
                    # 어떤 부분이 아티스트인지 추정 (보통 짧은 쪽이 아티스트)
                    if len(parts[0]) < len(parts[1]):
                        artist = parts[0].strip()
                        album_title = parts[1].strip()
                    else:
                        artist = parts[1].strip()
                        album_title = parts[0].strip()
            
            # 썸네일 이미지 추출
            try:
                # 플레이리스트의 첫 번째 영상 썸네일 가져오기
                first_video_url = playlist.video_urls[0] if playlist.video_urls else None
                thumbnail_url = None
                
                if first_video_url:
                    yt = YouTube(first_video_url)
                    thumbnail_url = yt.thumbnail_url
            except:
                thumbnail_url = None
            
            return {
                'title': album_title,
                'artist': artist,
                'release_date': datetime.now().strftime('%Y-%m-%d'),  # 정확한 발매일은 알 수 없음
                'genre': '알 수 없음',  # 장르 정보는 유튜브에서 직접 제공하지 않음
                'cover_image': thumbnail_url,
                'youtube_url': youtube_url,
            }
        else:
            # 단일 비디오인 경우
            yt = YouTube(youtube_url)
            video_title = yt.title
            
            # 비디오 제목에서 앨범 제목과 아티스트 추출 시도
            artist = ""
            album_title = video_title
            
            if ' - ' in video_title:
                parts = video_title.split(' - ', 1)
                if len(parts) == 2:
                    artist = parts[0].strip()
                    album_title = parts[1].strip()
            
            return {
                'title': album_title,
                'artist': artist if artist else yt.author,
                'release_date': datetime.now().strftime('%Y-%m-%d'),
                'genre': '알 수 없음',
                'cover_image': yt.thumbnail_url,
                'youtube_url': youtube_url,
            }
            
    except Exception as e:
        # 오류 발생 시 기본 정보 반환
        return {
            'title': '유튜브에서 가져온 앨범',
            'artist': '알 수 없음',
            'release_date': datetime.now().strftime('%Y-%m-%d'),
            'genre': '알 수 없음',
            'cover_image': None,
            'youtube_url': youtube_url,
            'error': str(e)
        }

# 유튜브에서 노래 정보 가져오기
def fetch_songs_from_youtube(youtube_url):
    try:
        songs = []
        
        # 플레이리스트 URL인지 확인
        if 'list=' in youtube_url:
            # 유튜브 플레이리스트 정보 가져오기
            playlist = PytubePlaylist(youtube_url)
            
            # 플레이리스트 내 모든 비디오 정보 추출
            for index, video_url in enumerate(playlist.video_urls):
                try:
                    yt = YouTube(video_url)
                    
                    # 비디오 제목에서 불필요한 부분 제거 시도
                    title = yt.title
                    # "[Official MV]", "(Audio)" 등의 패턴 제거
                    title = re.sub(r'\[.*?\]|\(.*?\)|Official|Audio|Video|MV', '', title).strip()
                    
                    # 재생 시간을 분:초 형식으로 변환
                    duration_seconds = yt.length
                    minutes = duration_seconds // 60
                    seconds = duration_seconds % 60
                    duration = f"{minutes}:{seconds:02d}"
                    
                    songs.append({
                        'title': title,
                        'track_number': index + 1,
                        'duration': duration,
                        'youtube_url': video_url
                    })
                except Exception as e:
                    print(f"비디오 정보 추출 중 오류: {str(e)}")
                    continue
        else:
            # 단일 비디오인 경우
            yt = YouTube(youtube_url)
            
            # 비디오 제목에서 불필요한 부분 제거 시도
            title = yt.title
            title = re.sub(r'\[.*?\]|\(.*?\)|Official|Audio|Video|MV', '', title).strip()
            
            # 재생 시간을 분:초 형식으로 변환
            duration_seconds = yt.length
            minutes = duration_seconds // 60
            seconds = duration_seconds % 60
            duration = f"{minutes}:{seconds:02d}"
            
            songs.append({
                'title': title,
                'track_number': 1,
                'duration': duration,
                'youtube_url': youtube_url
            })
        
        return songs
    except Exception as e:
        print(f"노래 정보 가져오기 오류: {str(e)}")
        # 오류 발생 시 빈 리스트 반환
        return []

@app.route('/add_review/<int:album_id>', methods=['POST'])
@login_required
def add_review(album_id):
    album = Album.query.get_or_404(album_id)
    
    # 기존 리뷰 확인
    existing_review = Review.query.filter_by(
        album_id=album_id,
        user_id=current_user.id
    ).first()
    
    if existing_review:
        flash('이미 이 앨범에 리뷰를 작성했습니다. 기존 리뷰를 수정해주세요.', 'warning')
        return redirect(url_for('album_detail', album_id=album_id))
    
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    
    # 유효성 검사
    if not rating or not rating.isdigit() or int(rating) < 0 or int(rating) > 3:
        flash('별점을 0부터 3까지 선택해주세요.', 'danger')
        return redirect(url_for('album_detail', album_id=album_id))
    
    # 리뷰 생성
    new_review = Review(
        rating=int(rating),
        comment=comment,
        user_id=current_user.id,
        album_id=album_id
    )
    
    db.session.add(new_review)
    db.session.commit()
    
    flash('리뷰가 등록되었습니다!', 'success')
    return redirect(url_for('album_detail', album_id=album_id))

@app.route('/edit_review/<int:review_id>', methods=['POST'])
@login_required
def edit_review(review_id):
    review = Review.query.get_or_404(review_id)
    
    # 리뷰 소유자 확인
    if review.user_id != current_user.id:
        flash('본인의 리뷰만 수정할 수 있습니다.', 'danger')
        return redirect(url_for('album_detail', album_id=review.album_id))
    
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    
    # 유효성 검사
    if not rating or not rating.isdigit() or int(rating) < 0 or int(rating) > 3:
        flash('별점을 0부터 3까지 선택해주세요.', 'danger')
        return redirect(url_for('album_detail', album_id=review.album_id))
    
    # 리뷰 업데이트
    review.rating = int(rating)
    review.comment = comment
    review.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    flash('리뷰가 수정되었습니다!', 'success')
    return redirect(url_for('album_detail', album_id=review.album_id))

@app.route('/delete_review/<int:review_id>')
@login_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    
    # 리뷰 소유자 또는 관리자 확인
    if review.user_id != current_user.id:
        flash('본인의 리뷰만 삭제할 수 있습니다.', 'danger')
        return redirect(url_for('album_detail', album_id=review.album_id))
    
    album_id = review.album_id
    db.session.delete(review)
    db.session.commit()
    
    flash('리뷰가 삭제되었습니다.', 'success')
    return redirect(url_for('album_detail', album_id=album_id))

if __name__ == '__main__':
    app.run(debug=True, port=5002) 