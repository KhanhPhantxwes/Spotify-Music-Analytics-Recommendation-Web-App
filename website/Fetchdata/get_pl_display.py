from ..model import Playlist, User
from .. import db
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from website.model import Artist, Artist_Song, Song, Song_point,BillboardEntry2,Playlist_Song


def Get_playlist_display(access_token: str, user: User):
    playlist= (db.session.query(Playlist.playlist_img, Playlist.playlist_name, Playlist.playlist_id).filter_by(owner_id = user.spotify_id).all())
    #image_urls = [r[0] for r in img_list if r[0] is not None]
    return playlist

def Get_song_lyric(songid : str):
    song_lyric = db.session.query(Song.lyric).filter(Song.song_id == songid).scalar()

    return song_lyric
