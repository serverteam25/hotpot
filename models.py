from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# 플레이리스트와 곡 간의 관계를 위한 연결 테이블
class PlaylistSong(db.Model):
    __tablename__ = 'playlist_song'
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'), primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), primary_key=True)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    playlist = db.relationship("Playlist", back_populates="songs")
    song = db.relationship("Song", back_populates="playlists")


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    preferred_genres = db.Column(db.String(255))  # 선호 장르 (쉼표로 구분된 문자열)

    reviews = db.relationship('Review', backref='author', lazy='dynamic')
    playlists = db.relationship('Playlist', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    release_date = db.Column(db.Date)
    genre = db.Column(db.String(255))
    cover_image = db.Column(db.String(500))
    youtube_url = db.Column(db.String(500))  # 유튜브 URL
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    reviews = db.relationship('Review', backref='album', lazy='dynamic')
    songs = db.relationship('Song', backref='album', lazy='dynamic')

    def __repr__(self):
        return f'<Album {self.title} by {self.artist}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'artist': self.artist,
            'release_date': self.release_date.strftime('%Y-%m-%d') if self.release_date else None,
            'genre': self.genre,
            'cover_image': self.cover_image,
            'youtube_url': self.youtube_url,
            'avg_rating': self.average_rating(),
            'song_count': self.songs.count()
        }

    def average_rating(self):
        reviews = self.reviews.all()
        if not reviews:
            return 0
        return sum(review.rating for review in reviews) / len(reviews)

    @property
    def youtube_embed_url(self):
        if not self.youtube_url:
            return None
        if 'youtube.com/watch?v=' in self.youtube_url:
            video_id = self.youtube_url.split('v=')[1].split('&')[0]
            return f"https://www.youtube.com/embed/{video_id}"
        elif 'youtube.com/playlist?list=' in self.youtube_url:
            list_id = self.youtube_url.split('list=')[1].split('&')[0]
            return f"https://www.youtube.com/embed/videoseries?list={list_id}"
        elif 'youtu.be/' in self.youtube_url:
            video_id = self.youtube_url.split('youtu.be/')[1].split('?')[0]
            return f"https://www.youtube.com/embed/{video_id}"
        return self.youtube_url

    @property
    def first_song_youtube_embed_url(self):
        first_song = self.songs.first()
        if first_song and first_song.youtube_url:
            return first_song.youtube_embed_url
        return None


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.String(10))  # 예: "3:45"
    track_number = db.Column(db.Integer)
    youtube_url = db.Column(db.String(500))  # 유튜브 URL
    lastfm_url = db.Column(db.String(500))   # Last.fm URL
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=False)

    playlists = db.relationship('PlaylistSong', back_populates='song')

    def __repr__(self):
        return f'<Song {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'duration': self.duration,
            'track_number': self.track_number,
            'youtube_url': self.youtube_url,
            'lastfm_url': self.lastfm_url,
            'album_id': self.album_id,
            'album_title': self.album.title,
            'artist': self.album.artist
        }

    @property
    def youtube_embed_url(self):
        if not self.youtube_url:
            return None
        if 'youtube.com/watch?v=' in self.youtube_url:
            video_id = self.youtube_url.split('v=')[1].split('&')[0]
        elif 'youtu.be/' in self.youtube_url:
            video_id = self.youtube_url.split('youtu.be/')[1].split('?')[0]
        else:
            return self.youtube_url
        return f"https://www.youtube.com/embed/{video_id}"


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    cover_image = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_public = db.Column(db.Boolean, default=True)

    songs = db.relationship('PlaylistSong', back_populates='playlist')

    def __repr__(self):
        return f'<Playlist {self.name} by User {self.user_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'cover_image': self.cover_image,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'user_id': self.user_id,
            'username': self.user.username,
            'is_public': self.is_public,
            'song_count': len(self.songs)
        }


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=False)
    is_public = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Review {self.id} by User {self.user_id} for Album {self.album_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'user_id': self.user_id,
            'username': self.author.username,
            'album_id': self.album_id,
            'is_public': self.is_public
        }
