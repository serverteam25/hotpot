from app import app, db
from models import Album, Song
from datetime import date

def add_album(title, artist, release_date, genre, cover_image, youtube_url, songs):
    with app.app_context():
        # 앨범 생성
        new_album = Album(
            title=title,
            artist=artist,
            release_date=release_date,
            genre=genre,
            cover_image=cover_image,
            youtube_url=youtube_url
        )
        db.session.add(new_album)
        db.session.flush()  # ID 생성

        # 곡 추가
        for track_number, song_data in enumerate(songs, 1):
            song = Song(
                title=song_data['title'],
                duration=song_data['duration'],
                track_number=track_number,
                youtube_url=song_data.get('youtube_url'),
                lastfm_url=song_data.get('lastfm_url'),
                album_id=new_album.id
            )
            db.session.add(song)

        db.session.commit()
        print(f"앨범 '{title}'이(가) 성공적으로 추가되었습니다.")

if __name__ == "__main__":
    # 예시: 앨범 추가
    new_album_data = {
        'title': '앨범 제목',
        'artist': '아티스트',
        'release_date': date(2024, 1, 1),
        'genre': '장르',
        'cover_image': '커버 이미지 URL',
        'youtube_url': '유튜브 URL',
        'songs': [
            {
                'title': '곡 1',
                'duration': '3:45',
                'youtube_url': '유튜브 URL 1',
                'lastfm_url': 'Last.fm URL 1'
            },
            {
                'title': '곡 2',
                'duration': '4:20',
                'youtube_url': '유튜브 URL 2',
                'lastfm_url': 'Last.fm URL 2'
            }
        ]
    }

    add_album(**new_album_data) 