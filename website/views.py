

from flask import Blueprint, render_template, redirect, url_for, request

from website.Graph.Circle import Circle_graph
from website.Recommendation.get_lyric import get_song_info, song_lyric
from website.Recommendation.get_recommendation import Get_recommendation

from .model import Artist, Playlist, User, Song,Playlist_Song
from . import db
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

import io
import base64
import matplotlib
matplotlib.use("Agg")  # important on servers / no GUI

views = Blueprint('views',__name__)

@views.route('/')
def home():
        return render_template("login.html")

@views.route('/playlist/<playlistid>')
def Playlist_item_display(playlistid):
        
        playlist_item = (
                db.session.query( Song.song_id,Song.song_name, Artist.artist_name)
                .join(Playlist_Song, Song.song_id == Playlist_Song.c.song_id)
                .join(Artist, Song.artist_id == Artist.artist_id)
                .filter(Playlist_Song.c.playlist_id == playlistid)
                .all()
        )
        
        #To display song lyric onclick from html
        song_id = request.args.get("song_id", type = str)
        selected_song = None
        if song_id:
                selected_song = Song.query.get(song_id) #Return a Song instance

        #Fetch lyric of songs into database (if new song is added)
        song_lyric(playlist_item)

        #List of recommendations
        recommended_list = Get_recommendation(playlistid,30,10000)

        #Graph
        mood_chart = Circle_graph(playlistid)



        return render_template("playlist_item.html", playlist = playlist_item, recs= recommended_list, chart =mood_chart,
                                selected_song_lyric = selected_song, playlistid = playlistid )