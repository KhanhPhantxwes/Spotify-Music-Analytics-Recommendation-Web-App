from .model import Artist, Playlist, User, Song
from . import db
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

def Get_pl_item(access_token: str, user: User):
    sp = Spotify(auth=access_token)


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
                song_obj = new_song
            
            for a in track.get("artists", []):
                ar_id = a.get("id")
                if not ar_id:
                    continue
                artist_obj = Artist.query.get(ar_id)
                if artist_obj is None:
                    artist_obj = Artist(artist_id=ar_id, artist_name=a.get("name"))
                    db.session.add(artist_obj)
                if artist_obj not in song_obj.artist:
                    song_obj.artist.append(artist_obj)


            #append to the playlist_song table
            if song_obj not in pl.song:
                pl.song.append(song_obj)
    
    db.session.commit()

