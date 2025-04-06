from app import app, db
from models import User, Album, Song, Review, Playlist, PlaylistSong
from werkzeug.security import generate_password_hash
from datetime import datetime, date
import lastfm
import time
from lastfm import get_top_album, get_album_info
import requests
import re

def clean_text(text):
    """이모지와 특수 문자를 제거하고 기본 ASCII 문자만 남깁니다."""
    # ASCII 문자, 숫자, 기본 문장 부호만 허용
    return re.sub(r'[^\x00-\x7F]+', '', text)

def create_album_from_data(album_data):
    """Last.fm API에서 받은 앨범 데이터로 Album 객체 생성"""
    # 앨범 상세 정보 가져오기
    album_info = lastfm.get_album_info(
        mbid=album_data.get('mbid'),
        album_title=album_data.get('name'),
        artist_name=album_data.get('artist', {}).get('name')
    )
    
    if not album_info:
        return None
        
    album = Album(
        title=album_info['title'],
        artist=album_info['artist'],
        release_date=datetime.now().date(),  # Last.fm에서 발매일을 가져올 수 없음
        genre=", ".join(album_info.get('tags', [])[:2]) if album_info.get('tags') else 'Unknown',
        cover_image=album_info.get('cover_image'),
        youtube_url=None  # Last.fm에서는 유튜브 URL을 제공하지 않음
    )
    db.session.add(album)
    db.session.flush()  # ID 생성
    
    # 곡 추가
    for track_data in album_info.get('tracks', []):
        song = Song(
            title=track_data['title'],
            duration=track_data.get('duration', '0:00'),
            track_number=track_data.get('rank', 1),
            youtube_url=None,  # Last.fm에서는 유튜브 URL을 제공하지 않음
            lastfm_url=track_data.get('url'),
            album_id=album.id
        )
        db.session.add(song)
    
    return album

def seed_database():
    """데이터베이스를 초기화하고 초기 데이터를 추가합니다."""
    
    print("Dropping all tables...")
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Tables recreated successfully")

        # 테스트 유저 생성
        test_user = User(
            username="testuser",
            email="test@example.com",
            password_hash=generate_password_hash("password123", method='sha256')
        )
        db.session.add(test_user)
        db.session.commit()
        print("Test user created")

        # 모든 정규 앨범을 가져올 메인 아티스트
        main_artists = [
            'Kanye West', 'Tyler, The Creator', 'Playboi Carti', 
            'JPEGMAFIA', 'Cordae', 'Drake', 'Kendrick Lamar',
            'J. Cole', 'Travis Scott', 'Frank Ocean', 'The Weeknd',
            'Aminé', 'IDK', 'SZA', 'Daniel Caesar'
        ]
        
        # Top 5 앨범만 가져올 아티스트
        kpop_artists = [
            # 5세대 그룹
            'BABYMONSTER', 'ILLIT', 
           'KISS OF LIFE',  
            'NewJeans', 'LE SSERAFIM', 'IVE', 'NMIXX', 
            'tripleS',
            
            # 4세대 그룹
            'BLACKPINK', 'TWICE', 'Red Velvet', 'aespa', 'ITZY', 
            'STAYC', '(G)I-DLE', 'fromis_9',
            
            
            # 3세대 그룹
            'OH MY GIRL',  'GFRIEND', 'LOONA'
   
            
        
        ]

        # 정규 앨범 필터링을 위한 키워드
        exclude_keywords = [
            'single', 'ep', 'remix', 'live', 'demo', 'instrumental',
            'compilation', 'complete', 'collection', 'best of', 'greatest hits',
            'deluxe', 'special', 'edition', 'remaster', 'remastered',
            'mixtape', 'mix tape', 'soundtrack', 'ost', 'cover',
            'acoustic', 'unplugged', 'session', 'bootleg',
            'clean', 'explicit', 'clean version', 'explicit version',
            'karaoke', 'instrumental version', 'inst.',
            'japanese', 'chinese', 'korean', 'international',
            'repackage', 'repacked', 'bonus', 'exclusive',
            'feat.', 'ft.', '&',
            '(cd', '(lp', '(digital', '(vinyl',
            'version', 'ver.', ' ver'
        ]

        print("\nProcessing main artists (up to 10 albums)...")
        # 메인 아티스트들의 앨범 가져오기 (최대 10개)
        for artist_name in main_artists:
            print(f"\nProcessing {artist_name}...")
            
            params = {
                'method': 'artist.getTopAlbums',
                'artist': artist_name,
                'api_key': lastfm.LASTFM_API_KEY,
                'format': 'json',
                'limit': 50  # 필터링을 위해 여유있게 가져오기
            }
            
            try:
                response = requests.get(lastfm.BASE_URL, params=params)
                response.raise_for_status()
                data = response.json()
                
                if 'topalbums' not in data or 'album' not in data['topalbums']:
                    print(f"No albums found for {artist_name}")
                    continue
                
                albums = data['topalbums']['album']
                added_count = 0
                
                for album_data in albums:
                    if added_count >= 10:  # 10개 앨범만 추가
                        break
                        
                    title = album_data.get("name")
                    
                    # 제외할 키워드가 포함된 앨범 건너뛰기
                    should_exclude = False
                    title_lower = title.lower()
                    
                    for keyword in exclude_keywords:
                        if keyword.lower() in title_lower:
                            should_exclude = True
                            break
                    
                    if should_exclude:
                        continue
                        
                    artist_name = album_data.get("artist", {}).get("name") or artist_name
                    mbid = album_data.get("mbid")

                    # 이미 존재하는 앨범인지 확인
                    existing = Album.query.filter_by(title=title, artist=artist_name).first()
                    if existing:
                        print(f"Album {title} by {artist_name} already exists")
                        continue

                    # 앨범 상세 정보 가져오기
                    album_info = get_album_info(mbid=mbid, album_title=title, artist_name=artist_name)
                    if not album_info:
                        print(f"Could not fetch album info for {title}")
                        continue
                    
                    # 트랙이 3개 미만인 앨범 건너뛰기
                    if len(album_info.get("tracks", [])) < 3:
                        print(f"Skipping {title} - less than 3 tracks")
                        continue
                    
                    # 새 앨범 생성
                    new_album = Album(
                        title=album_info["title"],
                        artist=album_info["artist"],
                        genre=", ".join(album_info.get("tags", [])[:2]),
                        cover_image=album_info.get("cover_image")
                    )
                    db.session.add(new_album)
                    db.session.flush()

                    # 트랙 추가
                    for track in album_info.get("tracks", []):
                        song = Song(
                            title=clean_text(track["title"]),  # 제목 정제
                            duration=track["duration"],
                            track_number=track.get("rank", 1),
                            album_id=new_album.id
                        )
                        db.session.add(song)

                    # 테스트 리뷰 추가
                    test_review = Review(
                        rating=5,
                        comment=f"Great album by {artist_name}!",
                        user_id=test_user.id,
                        album_id=new_album.id
                    )
                    db.session.add(test_review)
                    
                    db.session.commit()
                    added_count += 1
                    print(f"Added album {added_count}/10: {title} by {artist_name}")
                
                time.sleep(1)  # API 호출 간격 조절
                
            except Exception as e:
                print(f"Error processing {artist_name}: {str(e)}")
                continue

        print("\nProcessing K-pop artists (top 5 albums)...")
        # K-pop 아티스트들의 top 5 앨범 가져오기
        for artist_name in kpop_artists:
            print(f"\nProcessing {artist_name}...")
            
            params = {
                'method': 'artist.getTopAlbums',
                'artist': artist_name,
                'api_key': lastfm.LASTFM_API_KEY,
                'format': 'json',
                'limit': 10
            }
            
            try:
                response = requests.get(lastfm.BASE_URL, params=params)
                response.raise_for_status()
                data = response.json()
                
                if 'topalbums' not in data or 'album' not in data['topalbums']:
                    print(f"No albums found for {artist_name}")
                    continue
                
                albums = data['topalbums']['album']
                added_count = 0
                
                for album_data in albums:
                    if added_count >= 5:  # 5개 앨범만 추가
                        break
                        
                    title = album_data.get("name")
                    artist_name = album_data.get("artist", {}).get("name") or artist_name
                    mbid = album_data.get("mbid")

                    # 이미 존재하는 앨범인지 확인
                    existing = Album.query.filter_by(title=title, artist=artist_name).first()
                    if existing:
                        print(f"Album {title} by {artist_name} already exists")
                        continue

                    # 앨범 상세 정보 가져오기
                    album_info = get_album_info(mbid=mbid, album_title=title, artist_name=artist_name)
                    if not album_info:
                        print(f"Could not fetch album info for {title}")
                        continue
                    
                    # 트랙이 3개 미만인 앨범 건너뛰기
                    if len(album_info.get("tracks", [])) < 3:
                        print(f"Skipping {title} - less than 3 tracks")
                        continue
                    
                    # 새 앨범 생성
                    new_album = Album(
                        title=album_info["title"],
                        artist=album_info["artist"],
                        genre=", ".join(album_info.get("tags", [])[:2]),
                        cover_image=album_info.get("cover_image")
                    )
                    db.session.add(new_album)
                    db.session.flush()

                    # 트랙 추가
                    for track in album_info.get("tracks", []):
                        song = Song(
                            title=clean_text(track["title"]),  # 제목 정제
                            duration=track["duration"],
                            track_number=track.get("rank", 1),
                            album_id=new_album.id
                        )
                        db.session.add(song)

                    # 테스트 리뷰 추가
                    test_review = Review(
                        rating=5,
                        comment=f"Great album by {artist_name}!",
                        user_id=test_user.id,
                        album_id=new_album.id
                    )
                    db.session.add(test_review)
                    
                    db.session.commit()
                    added_count += 1
                    print(f"Added album {added_count}/5: {title} by {artist_name}")
                
                time.sleep(1)  # API 호출 간격 조절
                
            except Exception as e:
                print(f"Error processing {artist_name}: {str(e)}")
                continue

        # 플레이리스트 생성
        hip_hop_playlist = Playlist(
            name="힙합/R&B 플레이리스트",
            user_id=test_user.id
        )
        kpop_playlist = Playlist(
            name="K-pop 플레이리스트",
            user_id=test_user.id
        )
        
        db.session.add(hip_hop_playlist)
        db.session.add(kpop_playlist)
        db.session.commit()
        
        print("\nDatabase seeding completed successfully!")

if __name__ == "__main__":
    seed_database() 