import os
import requests
from datetime import datetime
from models import db, Album, Song  # Flask 앱에서 models import 필요

LASTFM_API_KEY = os.environ.get("LASTFM_API_KEY")
BASE_URL = "http://ws.audioscrobbler.com/2.0/"
HEADERS = {"User-Agent": "hotpot-app"}

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
        return albums[0]
    return None

def get_album_info(mbid=None, album_title=None, artist_name=None):
    params = {
        "method": "album.getinfo",
        "api_key": LASTFM_API_KEY,
        "format": "json",
    }

    if mbid:
        params["mbid"] = mbid
    elif album_title and artist_name:
        params["album"] = album_title
        params["artist"] = artist_name
    else:
        return None
    res = requests.get(BASE_URL, params=params, headers=HEADERS)
    data = res.json()
    album_info = data.get("album", {})

    if not album_info:
        return None

    tracks = []
    for track in album_info.get("tracks", {}).get("track", []):
        raw_duration = track.get("duration")
        try:
            duration = int(raw_duration) if raw_duration is not None else 0
        except ValueError:
            duration = 0

        minutes = duration // 60
        seconds = duration % 60
        formatted_duration = f"{minutes}:{seconds:02d}"
        tracks.append({
            "title": track.get("name"),
            "duration": formatted_duration,
            "url": track.get("url"),
            "rank": track.get("@attr", {}).get("rank")
        })
    return {
        "title": album_info.get("name"),
        "artist": album_info.get("artist"),
        "cover_image": album_info.get("image", [])[-1].get("#text") if album_info.get("image") else None,
        "tracks": tracks,
        "tags": [tag.get("name") for tag in album_info.get("tags", {}).get("tag", [])]
    }

def get_chart_recommended_albums(limit=10):
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
            print(">> 저장할 youtube_url:", track.get("url"))

            song = Song(
                title=track["title"],
                duration=track["duration"],
                track_number=track.get("rank") or idx,
                album_id=new_album.id,
                youtube_url=track["url"] 
            )
            db.session.add(song)

        saved_albums.append(new_album)
    print(f"총 저장된 추천 앨범 수: {len(saved_albums)}")

    db.session.commit()
    return saved_albums