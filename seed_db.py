from app import app, db
from models import User, Album, Song, Review, Playlist, PlaylistSong
from werkzeug.security import generate_password_hash
from datetime import datetime, date
import lastfm

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
    with app.app_context():
        # 테스트 유저가 이미 존재하는지 확인
        test_user = User.query.filter_by(username="testuser").first()
        if not test_user:
            # 테스트 유저 생성
            test_user = User(
                username="testuser",
                email="test@example.com",
                password_hash=generate_password_hash("password123")
            )
            db.session.add(test_user)
            db.session.flush()
        
        # Last.fm API를 통해 앨범 데이터 가져오기
        print("Last.fm에서 앨범 데이터를 가져오는 중...")
        
        # 힙합 아티스트 목록
        hiphop_artists = [
            "Kendrick Lamar", "J. Cole", "Drake", "Travis Scott", "Kanye West",
            "Jay-Z", "Nas", "Eminem", "Tyler, The Creator", "Childish Gambino",
            "A$AP Rocky", "Mac Miller", "Post Malone", "Lil Baby", "21 Savage",
            "Future", "Migos", "Lil Uzi Vert", "Playboi Carti", "Young Thug",
            "Metro Boomin", "Tyler, The Creator"
        ]
        
        # R&B 아티스트 목록
        rnb_artists = [
            "Frank Ocean", "The Weeknd", "SZA", "Daniel Caesar", "H.E.R.",
            "Alicia Keys", "John Legend", "Usher", "Chris Brown", "Beyoncé",
            "Rihanna", "Bruno Mars", "Anderson .Paak", "D'Angelo", "Erykah Badu",
            "Lauryn Hill", "Jhené Aiko", "Summer Walker", "Kehlani", "Teyana Taylor"
        ]
        
        # K-pop 여자 그룹 목록
        kpop_girl_groups = [
            "BLACKPINK", "TWICE", "Red Velvet", "NewJeans", "LE SSERAFIM",
            "IVE", "aespa", "ITZY", "STAYC", "NMIXX",
            "Girls' Generation", "2NE1", "MAMAMOO", "GFRIEND", "Apink",
            "EXID", "Dreamcatcher", "LOONA", "WJSN", "fromis_9"
        ]
        
        all_albums = []
        
        # 힙합 앨범 가져오기
        for artist in hiphop_artists:
            print(f"{artist}의 앨범을 가져오는 중...")
            album_data = lastfm.get_top_album(artist)
            if album_data:
                album = create_album_from_data(album_data)
                if album:
                    all_albums.append(album)
        
        # R&B 앨범 가져오기
        for artist in rnb_artists:
            print(f"{artist}의 앨범을 가져오는 중...")
            album_data = lastfm.get_top_album(artist)
            if album_data:
                album = create_album_from_data(album_data)
                if album:
                    all_albums.append(album)
        
        # K-pop 앨범 가져오기
        for group in kpop_girl_groups:
            print(f"{group}의 앨범을 가져오는 중...")
            album_data = lastfm.get_top_album(group)
            if album_data:
                album = create_album_from_data(album_data)
                if album:
                    all_albums.append(album)
        
        print(f"총 {len(all_albums)}개의 앨범이 추가되었습니다.")
        
        # 테스트 리뷰 추가
        for album in all_albums:
            review = Review(
                rating=4,
                comment="테스트 리뷰입니다.",
                user_id=test_user.id,
                album_id=album.id
            )
            db.session.add(review)
        
        # 힙합/R&B 플레이리스트 생성
        hiphop_rnb_playlist = Playlist(
            name="힙합/R&B 플레이리스트",
            description="인기 힙합과 R&B 곡들을 모았습니다.",
            user_id=test_user.id
        )
        db.session.add(hiphop_rnb_playlist)
        db.session.flush()
        
        # K-pop 플레이리스트 생성
        kpop_playlist = Playlist(
            name="K-pop 플레이리스트",
            description="인기 K-pop 곡들을 모았습니다.",
            user_id=test_user.id
        )
        db.session.add(kpop_playlist)
        db.session.flush()
        
        # 플레이리스트에 노래 추가
        for album in all_albums:
            for song in album.songs:
                playlist_song = PlaylistSong(
                    playlist_id=hiphop_rnb_playlist.id if album.genre in ["Hip-Hop", "R&B"] else kpop_playlist.id,
                    song_id=song.id
                )
                db.session.add(playlist_song)
        
        db.session.commit()
        print("시드 데이터가 성공적으로 추가되었습니다.")

if __name__ == "__main__":
    seed_database() 