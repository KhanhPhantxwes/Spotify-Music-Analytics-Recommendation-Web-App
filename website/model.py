from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime, timezone

class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id =db.Column(db.Integer, db.ForeignKey('user.id'))


User_Song = db.Table(
    "user_song",
    db.Column('user_id',db.Integer, db.ForeignKey('user.id'),primary_key=True),
    db.Column('song_id',db.Integer, db.ForeignKey('song.song_id'),primary_key=True)
)

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key =True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    create_at = db.Column(db.DateTime(timezone=True), default=func.now())
    last_login = db.Column(db.DateTime(timezone=True))
    spotify_id = db.Column(db.String(150))
    notes = db.relationship('Note') #define one-to-many relationship between User and Note

    #many-to-many
    song = db.relationship('Song', secondary = User_Song, back_populates = 'user')

class Song(db.Model):
    __tablename__ = "song"
    song_id = db.Column(db.Integer, primary_key =True)
    artist_id =  db.Column(db.String(150))
    song_name = db.Column(db.String(150))
    mood = db.Column(db.String(150))
    lyric = db.Column(db.String(2000))

    #many-to-many 
    user = db.relationship('User', secondary = User_Song , back_populates = 'song')


    