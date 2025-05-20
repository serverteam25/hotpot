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
    """
    Last.fm API를 통해 앨범 상세 정보를 가져옵니다.
    """
    try:
        # API 파라미터 설정
        params = {
            'method': 'album.getInfo',
            'api_key': LASTFM_API_KEY,
            'format': 'json'
        }
        
        if mbid:
            params['mbid'] = mbid
        elif album_title and artist_name:
            params['album'] = album_title
            params['artist'] = artist_name
        else:
            return None
            
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if 'album' not in data:
            print(f"No album data found for {album_title}")
            return None
            
        album_data = data['album']
        
        # 태그 정보 처리
        tags = []
        if 'tags' in album_data:
            tags_data = album_data['tags']
            if isinstance(tags_data, dict) and 'tag' in tags_data:
                tag_list = tags_data['tag']
                if isinstance(tag_list, list):
                    tags = [tag['name'][:50] for tag in tag_list if isinstance(tag, dict) and 'name' in tag]  # 각 태그를 50자로 제한
                elif isinstance(tag_list, dict) and 'name' in tag_list:
                    tags = [tag_list['name'][:50]]  # 태그를 50자로 제한
        
        # 최대 3개의 태그만 사용하고, 전체 길이가 250자를 넘지 않도록 함
        tags = tags[:3]
        combined_tags = ", ".join(tags)
        if len(combined_tags) > 250:
            # 태그들을 250자 이내로 줄임
            tags = []
            current_length = 0
            for tag in tags[:3]:
                if current_length + len(tag) + 2 <= 250:  # 2는 ", " 구분자의 길이
                    tags.append(tag)
                    current_length += len(tag) + 2
                else:
                    break
        
        # 트랙 정보 처리
        tracks = []
        if 'tracks' in album_data and album_data['tracks']:
            tracks_data = album_data['tracks']
            if isinstance(tracks_data, dict) and 'track' in tracks_data:
                track_list = tracks_data['track']
                if isinstance(track_list, list):
                    for i, track in enumerate(track_list, 1):
                        if isinstance(track, dict):
                            # 트랙 제목 길이 제한 및 필터링
                            track_title = track.get('name', f'Track {i}')
                            if len(track_title) > 250:  # 여유있게 250자로 제한
                                track_title = track_title[:250] + '...'
                            
                            track_info = {
                                'title': track_title,
                                'duration': track.get('duration', '0:00'),
                                'rank': i,
                                'url': track.get('url', '')
                            }
                            tracks.append(track_info)
                elif isinstance(track_list, dict):
                    track_title = track_list.get('name', 'Track 1')
                    if len(track_title) > 250:
                        track_title = track_title[:250] + '...'
                        
                    tracks.append({
                        'title': track_title,
                        'duration': track_list.get('duration', '0:00'),
                        'rank': 1,
                        'url': track_list.get('url', '')
                    })
        
        # 커버 이미지 처리
        cover_image = None
        if 'image' in album_data:
            images = album_data['image']
            if isinstance(images, list) and images:
                for image in images:
                    if isinstance(image, dict) and image.get('size') == 'extralarge' and '#text' in image:
                        cover_image = image['#text']
                        break
        
        return {
            'title': album_data.get('name', album_title),
            'artist': album_data.get('artist', artist_name),
            'tags': tags,
            'tracks': tracks,
            'cover_image': cover_image
        }
        
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
            print(">> 저장할 url:", track["url"])
            song = Song(
                title=track["title"],
                duration=track["duration"],
                track_number=idx,
                album_id=new_album.id,
                lastfm_url=track["url"]
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

def get_all_albums(artist_name):
    """
    아티스트의 정규 앨범만 가져옵니다.
    싱글, EP, 리믹스, 라이브, 컴필레이션 등은 제외됩니다.
    """
    try:
        params = {
            'method': 'artist.getTopAlbums',
            'artist': artist_name,
            'api_key': LASTFM_API_KEY,
            'format': 'json',
            'limit': 50
        }
        
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if 'topalbums' not in data or 'album' not in data['topalbums']:
            print(f"No albums found for {artist_name}")
            return []
        
        albums = data['topalbums']['album']
        
        # 제외할 키워드 목록 (대소문자 구분 없이 적용)
        exclude_keywords = [
            # 싱글, EP 관련
            'single', 'ep', 'maxi', 'promo', 'promotional',
            
            # 리믹스, 리메이크 관련
            'remix', 'remixed', 'mix', 'mashup', 'remaster', 'remastered',
            'remake', 'cover', 'acoustic', 'unplugged',
            
            # 라이브, 데모 관련
            'live', 'demo', 'concert', 'session', 'bootleg', 'recording',
            
            # 컴필레이션, 베스트 관련
            'compilation', 'complete', 'collection', 'best of', 'greatest',
            'hits', 'anthology', 'selected', 'selection', 'essential',
            
            # 특별판, 확장판 관련
            'deluxe', 'special', 'edition', 'expanded', 'extended',
            'bonus', 'exclusive', 'limited', 'collector', 'anniversary',
            
            # 버전 관련
            'version', 'ver.', ' ver', ' v1', ' v2', ' v3', ' v4',
            'japanese', 'chinese', 'korean', 'international',
            'winter', 'summer', 'spring', 'autumn',
            'day', 'night', 'morning', 'evening',
            
            # 기타
            'instrumental', 'inst.', 'karaoke', 'soundtrack', 'ost',
            'mixtape', 'tape', 'demo', 'clean', 'explicit',
            'repackage', 'repacked', 'digital', 'physical',
            'feat.', 'ft.', '&', '+',
            
            # 괄호로 묶인 버전 표시
            '(cd', '(lp', '(digital', '(vinyl', '(box',
            '(deluxe', '(special', '(expanded', '(remastered',
            '(anniversary', '(japanese', '(korean', '(chinese',
            '(original', '(bonus', '(exclusive'
        ]
        
        # 앨범 정보 정리
        album_list = []
        seen_albums = set()  # 중복 앨범 체크를 위한 세트
        
        for album in albums:
            album_name = album['name']
            
            # 이미 추가된 앨범인지 확인 (더 엄격한 정규화)
            normalized_name = album_name.lower()
            normalized_name = ''.join(c for c in normalized_name if c.isalnum() or c.isspace())
            normalized_name = ' '.join(normalized_name.split())
            
            if normalized_name in seen_albums:
                continue
                
            # 앨범 이름이 너무 길면 건너뛰기 (보통 리믹스나 특별판인 경우가 많음)
            if len(album_name) > 40:  # 40자로 제한
                continue
            
            # 괄호 안의 내용 체크
            if '(' in album_name and ')' in album_name:
                bracket_content = album_name[album_name.find('(')+1:album_name.find(')')]
                if any(keyword.lower() in bracket_content.lower() for keyword in exclude_keywords):
                    continue
            
            # 제외할 키워드가 포함된 앨범 건너뛰기 (더 엄격한 검사)
            should_exclude = False
            album_name_lower = album_name.lower()
            
            # 전체 문자열에서 키워드 검사
            for keyword in exclude_keywords:
                if keyword.lower() in album_name_lower:
                    should_exclude = True
                    break
                    
            # 각 단어 단위로 키워드 검사
            if not should_exclude:
                words = album_name_lower.split()
                for word in words:
                    if word in [k.lower() for k in exclude_keywords]:
                        should_exclude = True
                        break
            
            if should_exclude:
                continue
                
            album_info = {
                'title': album_name,
                'artist': album['artist']['name'],
                'mbid': album.get('mbid', ''),
                'cover_image': album['image'][-1]['#text'] if album['image'] else None
            }
            
            album_list.append(album_info)
            seen_albums.add(normalized_name)
        
        print(f"Found {len(album_list)} valid albums for {artist_name}")
        return album_list
        
    except Exception as e:
        print(f"Error fetching albums for {artist_name}: {str(e)}")
        return []