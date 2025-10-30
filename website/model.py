from . import db
from flask_login import UserMixin
from sqlalchemy.sql import funcp
from datetime import datetime, timezone

class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id =db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="notes")


Playlist_Song = db.Table(
    "playlist_song",
    db.Column('playlist_id',db.String(150), db.ForeignKey('playlist.playlist_id'),primary_key=True),
    db.Column('song_id',db.String(150), db.ForeignKey('song.song_id'),primary_key=True),
)

class Playlist(db.Model):
    __tablename__ = "playlist"
    playlist_id = db.Column(db.String(150), unique=True,primary_key = True)
    playlist_name = db.Column(db.String(150))
    playlist_img  = db.Column(db.String(512))  # URLs can exceed 150 chars

    # FK to a UNIQUE, indexed column (user.spotify_id)
    owner_id      = db.Column(
        db.String(150),
        db.ForeignKey("user.spotify_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    owner = db.relationship(
        "User",
        back_populates="playlists",
        primaryjoin="Playlist.owner_id==User.spotify_id",
        foreign_keys=[owner_id]
    )
    #many-to-many
    song = db.relationship('Song', secondary = Playlist_Song, back_populates = 'playlist')



class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key =True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    create_at = db.Column(db.DateTime(timezone=True), default=func.now())
    last_login = db.Column(db.DateTime(timezone=True))
    spotify_id = db.Column(db.String(150),unique=True, index=True, nullable=True)
    notes       = db.relationship("Note", back_populates="user", cascade="all, delete-orphan") #define one-to-many relationship between User and Note
    playlists = db.relationship('Playlist', back_populates="owner", cascade="all, delete-orphan")

    #many-to-many
    #song = db.relationship('Song', secondary = User_Song, back_populates = 'user')


#Artist_Song = db.Table(
    #"artist_song",
    #db.Column('artist_id',db.String(150), db.ForeignKey('artist.artist_id'),primary_key=True),
    #db.Column('song_id',db.String(150), db.ForeignKey('song.song_id'),primary_key=True),
#)
class Song(db.Model):
    __tablename__ = "song"
    added_at = db.Column(db.String(150))
    owner_id = db.Column(db.String(150))
    song_id = db.Column(db.String(150), unique=True, index=True, nullable=False,primary_key =True) #spotify track ID is string
    artist_id =  db.Column(db.String(150))
    song_name = db.Column(db.String(150))
    song_popularity = db.Column(db.Integer)
    mood = db.Column(db.String(150))
    lyric = db.Column(db.String(2000))

    #many-to-many 
    playlist = db.relationship('Playlist', secondary = Playlist_Song, back_populates = 'song')
    #artist = db.relationship('artist', secondary = Artist_Song, back_populates = 'song')
    #user = db.relationship('User', secondary = User_Song , back_populates = 'song')

class Artist(db.Model):
    __tablename__ = "artist"
    artist_id = db.Column(db.String(150), primary_key = True)
    artist_name = db.Column(db.String(150))
    Genre = db.Column(db.String(150))
    artist_img = db.Column(db.String(150))
    artist_populatiry = db.Column(db.Integer)
    many_to_many
    song = db.relationship('Song', secondary = Artist_Song, back_populates = 'artist')