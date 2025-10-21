from .model import Playlist, User
from . import db
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

def Get_currentuser_playlist(access_token: str, user: User):
    sp = Spotify(auth=access_token)
    playlists = sp.current_user_playlists()
    my_pl = []
    for playlist in playlists['items']:
        my_pl.append(playlist['name'])
    return my_pl


