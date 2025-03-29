import os
import requests

LASTFM_API_KEY = os.environ.get("LASTFM_API_KEY")
BASE_URL = "http://ws.audioscrobbler.com/2.0/"
HEADERS = {"User-Agent": "hotpot-app"}

#last.fm 내 top 5 artists 가져오기기
def get_top_artists(limit=5):
    params = {
        "method": "chart.gettopartists",
        "api_key": LASTFM_API_KEY,
        "format": "json",
        "limit": limit
    }
    res = requests.get(BASE_URL, params=params, headers=HEADERS)
    data = res.json()
    return data.get("artists", {}).get("artist", [])

#artist의 top ablum 1개 가져오기
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
        return albums[0]  # 가장 인기 있는 앨범 하나 리턴
    return None

#위의 함수 2개를 가지고 추천 앨범 5개 가져오기기
def get_chart_recommended_albums(limit=5):
    #차트 기반 추천 앨범 5개를 가져와 리스트로 반환
    top_artists = get_top_artists(limit=limit)
    result = []

    for artist in top_artists:
        album = get_top_album(artist["name"])
        if not album:
            continue

        title = album.get("name")
        artist_name = album.get("artist", {}).get("name") or artist["name"]
        image = album.get("image", [])[-1].get("#text") if album.get("image") else None
        playcount = album.get("playcount")

        result.append({
            "title": title,
            "artist": artist_name,
            "cover_image": image,
            "playcount": playcount
        })

    return result
    