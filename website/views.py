from flask import Blueprint, render_template, redirect, url_for
from .model import Playlist, User, Song,Playlist_Song
from . import db
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

views = Blueprint('views',__name__)

@views.route('/')
def home():
        return render_template("login.html")

@views.route('/playlist/<playlistid>')
def Playlist_item_display(playlistid):
        #playlist_item = db.session.execute(db.select(Playlist_Song.c.song_id)
                        #.where(Playlist_Song.c.playlist_id == playlistid)).scalars().all()
        playlist_item = db.session.query(Song.song_id, Song.song_name).join(
                Playlist_Song, Song.song_id == Playlist_Song.c.song_id
        ).filter(Playlist_Song.c.playlist_id == playlistid).all()


        return render_template("playlist_item.html", playlist = playlist_item)