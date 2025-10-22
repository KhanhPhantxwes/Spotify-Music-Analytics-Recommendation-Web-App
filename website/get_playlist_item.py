from .model import Playlist, User, Song
from . import db
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

def Get_pl_item(access_token: str, user: User):
    sp = Spotify(auth=access_token)
    #id = '4GEHf0KSpeKjsmQOMiUj0I' need to query playlist table to retrieve id of each playlist

    #get current_user id
    current_user = user.spotify_id

    #get list of playlist that has has owner_id = current_user
    playlists = Playlist.query.filter_by(owner_id=user.spotify_id).all()

    my_song = []

    for pl in playlists:
        pl_id = pl.playlist_id
        songs = sp.playlist_items(pl_id,limit =20)
        for song in songs['items']:
            track = song['track']
            when_added = song['added_at']
            owner = song['added_by']['id']
            if track is None:
                    continue  # skip unavailable tracks
            song_id = track['id']
            song_obj = Song.query.get(song_id)
            if song_obj is None:
                artist_id = track['artists'][0]['id'] 
                song_name = track['name']
                popularity= track['popularity']
                mood = ''
                lyric = ''
                new_song = Song(added_at = when_added,owner_id = owner, song_id=song_id,artist_id=artist_id,song_name=song_name,song_popularity = popularity,mood=mood,lyric=lyric)
                db.session.add(new_song)

    db.session.commit()

