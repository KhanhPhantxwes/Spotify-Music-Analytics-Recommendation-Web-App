from flask import Blueprint, render_template, redirect, url_for

from website.Recommendation.get_lyric import get_song_info, song_lyric

from .model import Artist, Playlist, User, Song,Playlist_Song
from . import db
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

views = Blueprint('views',__name__)

@views.route('/')
def home():
        return render_template("login.html")

@views.route('/playlist/<playlistid>')
def Playlist_item_display(playlistid):
        
        playlist_item = (
                db.session.query( Song.song_name, Artist.artist_name)
                .join(Playlist_Song, Song.song_id == Playlist_Song.c.song_id)
                .join(Artist, Song.artist_id == Artist.artist_id)
                .filter(Playlist_Song.c.playlist_id == playlistid)
                .all()
        )
        

        #get_song_info()
        print(song_lyric(playlist_item))

        return render_template("playlist_item.html", playlist = playlist_item)