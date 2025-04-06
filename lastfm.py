import os
import requests
from datetime import datetime
from models import db, Album, Song  # Flask 앱에서 models import 필요
from dotenv import load_dotenv

load_dotenv()

LASTFM_API_KEY = os.getenv('LASTFM_API_KEY')
BASE_URL = 'http://ws.audioscrobbler.com/2.0/'
HEADERS = {
    'User-Agent': 'Hotpot Music App/1.0'
}

def get_top_artists(limit=5, page=1):
    params = {
        "method": "chart.gettopartists",
        "api_key": LASTFM_API_KEY,
        "format": "json",
        "limit": limit,
        "page": page
    }
    res = requests.get(BASE_URL, params=params, headers=HEADERS)
    data = res.json()
    return data.get("artists", {}).get("artist", [])

def get_top_album(artist_name):
    params = {
        "method": "artist.gettopalbums",
        "artist": artist_name,
        "api_key": LASTFM_API_KEY,
        "format": "json",
        "limit": 1
    }
    res = requests.get(BASE_URL, params=params, headers=HEADERS)
    data = res.json()
    albums = data.get("topalbums", {}).get("album", [])
    if albums:
        album = albums[0]
        return {
            "name": album.get("name"),
            "artist": {"name": album.get("artist", {}).get("name", artist_name)},
            "mbid": album.get("mbid"),
            "image": album.get("image", [])
        }
    return None

def get_album_info(mbid=None, album_title=None, artist_name=None):
    """앨범 상세 정보 가져오기"""
    params = {
        'method': 'album.getInfo',
        'api_key': LASTFM_API_KEY,
        'format': 'json'
    }
    
    if mbid:
        params['mbid'] = mbid
    else:
        params['album'] = album_title
        params['artist'] = artist_name
    
    try:
        response = requests.get(BASE_URL, params=params, headers=HEADERS)
        data = response.json()
        
        if 'error' in data:
            print(f"Last.fm API Error: {data['error']}")
            return None
        
        album_data = data.get('album', {})
        
        # 앨범 기본 정보
        album_info = {
            'title': album_data.get('name', ''),
            'artist': album_data.get('artist', ''),
            'cover_image': album_data.get('image', [{}])[-1].get('#text', ''),
            'tags': [],
            'tracks': []
        }
        
        # 태그 정보 처리
        tags_data = album_data.get('tags', {}).get('tag', [])
        if isinstance(tags_data, dict):
            tags_data = [tags_data]
        elif isinstance(tags_data, str):
            tags_data = [{'name': tags_data}]
            
        for tag in tags_data:
            if isinstance(tag, dict) and 'name' in tag:
                album_info['tags'].append(tag['name'])
        
        # 수록곡 정보 처리
        tracks_data = album_data.get('tracks', {}).get('track', [])
        if isinstance(tracks_data, dict):
            tracks_data = [tracks_data]
            
        for track in tracks_data:
            if isinstance(track, dict):
                duration = track.get('duration', '0')
                try:
                    duration_sec = int(duration)
                    minutes = duration_sec // 60
                    seconds = duration_sec % 60
                    duration_str = f"{minutes}:{seconds:02d}"
                except (ValueError, TypeError):
                    duration_str = "0:00"
                    
                track_info = {
                    'title': track.get('name', ''),
                    'duration': duration_str
                }
                album_info['tracks'].append(track_info)
        
        return album_info
        
    except Exception as e:
        print(f"Error fetching album info: {str(e)}")
        return None

def get_chart_recommended_albums(limit=8):
    top_artists = get_top_artists(limit=limit)
    saved_albums = []

    for artist in top_artists:
        album_data = get_top_album(artist["name"])
        if not album_data:
            continue

        title = album_data.get("name")
        artist_name = album_data.get("artist", {}).get("name") or artist["name"]
        mbid = album_data.get("mbid")

        # 이미 같은 제목과 아티스트의 앨범이 있는지 확인
        existing = Album.query.filter_by(title=title, artist=artist_name).first()
        if existing:
            saved_albums.append(existing)
            continue

        album_info = get_album_info(mbid=mbid, album_title=title, artist_name=artist_name)
        if not album_info:
            continue
        
        new_album = Album(
            title=album_info["title"],
            artist=album_info["artist"],
            release_date=datetime.now().date(),
            genre=", ".join(album_info.get("tags", [])[:2]),
            cover_image=album_info.get("cover_image")
        )
        db.session.add(new_album)
        db.session.flush()  # ID 확보용

        for idx, track in enumerate(album_info.get("tracks", []), start=1):
            song = Song(
                title=track["title"],
                duration=track["duration"],
                track_number=idx,
                album_id=new_album.id
            )
            db.session.add(song)

        saved_albums.append(new_album)

    db.session.commit()
    return saved_albums

def get_chart_recommended_albums_old(limit=8):
    top_artists = get_top_artists(limit=limit)
    saved_albums = []

    for artist in top_artists:
        album_data = get_top_album(artist["name"])
        if not album_data:
            continue
        

        title = album_data.get("name")
        artist_name = album_data.get("artist", {}).get("name") or artist["name"]
        mbid = album_data.get("mbid")

        print("album 처음: ", album_data)

        # 이미 같은 제목과 아티스트의 앨범이 있는지 확인
        existing = Album.query.filter_by(title=title, artist=artist_name).first()
        if existing:
            saved_albums.append(existing)
            continue

        album_info = get_album_info(mbid=mbid, album_title=title, artist_name=artist_name)

        print(album_info)
        if not album_info:
            continue
        
        new_album = Album(
            title=album_info["title"],
            artist=album_info["artist"],
            release_date=datetime.now().date(),
            genre=", ".join(album_info.get("tags", [])[:2]),
            cover_image=album_info.get("cover_image")
        )
        db.session.add(new_album)
        db.session.flush()  # ID 확보용

        for idx, track in enumerate(album_info.get("tracks", []), start=1):
            song = Song(
                title=track["title"],
                duration=track["duration"],
                track_number=track.get("rank") or idx,
                album_id=new_album.id,
                lastfm_url=track["url"] 
            )
            db.session.add(song)

        saved_albums.append(new_album)
    print(f"총 저장된 추천 앨범 수: {len(saved_albums)}")

    db.session.commit()
    return saved_albums