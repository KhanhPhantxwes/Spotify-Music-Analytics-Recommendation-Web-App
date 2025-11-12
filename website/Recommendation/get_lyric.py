from website.model import Artist, Artist_Song, Song
from .. import db
import lyricsgenius

from collections import defaultdict


from sqlalchemy.orm import joinedload

def get_song_info(): #get list of song with name and artist name
    songs = Song.query.options(joinedload(Song.artist)).all()  # eager load M2M
    song_info = []
    for s in songs:
        names = ", ".join(a.artist_name for a in s.artist) or "(no artist)"
        song_info.append((s.song_name, names))
    return song_info
    
def song_lyric(song_list):
    access_token = "YaMnWwPTM5olA0OrlNIu4tzhwehCDWHlJdguSp1ml1HKL44H9guBSJeNd0wLrL17"
    # Initialize Genius client
    genius = lyricsgenius.Genius(access_token)

    results = []

    for song_name, artist_name in song_list:
        try:
            song = genius.search_song(song_name, artist_name)
            if song and song.lyrics:
                print(f"✅ Found lyrics for {song_name} by {artist_name}")
                results.append((song_name, artist_name, song.lyrics))
            else:
                print(f"⚠️ No lyrics found for {song_name} by {artist_name}")
                results.append((song_name, artist_name, None))
        except Exception as e:
            print(f"❌ Error fetching lyrics for {song_name} by {artist_name}: {e}")
            results.append((song_name, artist_name, None))
    return results




    
    


    