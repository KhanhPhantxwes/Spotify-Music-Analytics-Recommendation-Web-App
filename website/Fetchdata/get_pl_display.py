from ..model import Playlist, User
from .. import db
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth





def Get_playlist_display(access_token: str, user: User):
    playlist= (db.session.query(Playlist.playlist_img, Playlist.playlist_name, Playlist.playlist_id).filter_by(owner_id = user.spotify_id).all())
    #image_urls = [r[0] for r in img_list if r[0] is not None]
    return playlist