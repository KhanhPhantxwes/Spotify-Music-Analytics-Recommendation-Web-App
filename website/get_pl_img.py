from .model import Playlist, User
from . import db
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth


from website.model import Playlist, User


def Get_playlist_img(access_token: str, user: User):
    img_list = (db.session.query(Playlist.playlist_img).filter_by(owner_id = user.spotify_id).all())
    image_urls = [r[0] for r in img_list if r[0] is not None]
    return image_urls