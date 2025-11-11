from website.model import Artist, Artist_Song, Song
from .. import db
import lyricsgenius

from collections import defaultdict


from sqlalchemy.orm import joinedload

def get_song_info():
    songs = Song.query.options(joinedload(Song.artist)).all()  # eager load M2M
    for s in songs:
        names = ", ".join(a.artist_name for a in s.artist) or "(no artist)"
        print(f"{s.song_name} → {names}")

    
def song_lyric():
    access_token = "YaMnWwPTM5olA0OrlNIu4tzhwehCDWHlJdguSp1ml1HKL44H9guBSJeNd0wLrL17"
    # Initialize Genius client
    genius = lyricsgenius.Genius(access_token)

    # Search for the song
    #song = genius.search_song("Blinding Lights", "The Weeknd")
    #GET THE LIST IN ARTIST_SONG TABLE
    song_list = db.session.query(Artist_Song).all()

    # Print the lyrics
    #print(song.lyrics)
    for song in song_list:
        print(song.artist_id + " " + song.song_id)