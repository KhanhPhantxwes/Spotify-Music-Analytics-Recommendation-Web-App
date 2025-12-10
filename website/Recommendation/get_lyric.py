import os
from website.model import Artist, Artist_Song, Song
from .. import db
import lyricsgenius

from collections import defaultdict


from sqlalchemy.orm import joinedload

def get_songid():
    song_list = (db.session.query(Song.song_id)
                .all())
    return [row[0] for row in song_list]



def get_song_info(): #get list of song with name and artist name
    songs = Song.query.options(joinedload(Song.artist)).all()  # eager load M2M
    song_info = []
    for s in songs:
        names = ", ".join(a.artist_name for a in s.artist) or "(no artist)"
        song_info.append((s.song_name, names))
    return song_info
    
def song_lyric(song_list):
    access_token = os.getenv("GENIUS_API_KEY")
    # Initialize Genius client
    genius = lyricsgenius.Genius(access_token)

    results = []

    for song_id,song_name, artist_name in song_list:
        song_obj = (Song.query.filter_by(song_name=song_name).first())
        if song_obj is None:
            print(f"⚠️ Song '{song_name}' not found in DB, skipping.")
            results.append((song_name, artist_name, None))
            continue

        # 2. Skip songs that already have lyrics (unless overwrite=True)
        if song_obj.lyric:
            print(f"ℹ️ Lyrics already exist for '{song_name}', skipping.")
            results.append((song_name, artist_name, song_obj.lyric))
            continue
        # 3. Fetch from Genius
        try:
            genius_song = genius.search_song(song_name, artist_name)
            if genius_song and genius_song.lyrics:
                print(f"✅ Found lyrics for {song_name} by {artist_name}")

                # 4. UPDATE DB COLUMN
                song_obj.lyric = genius_song.lyrics
                results.append((song_name, artist_name, genius_song.lyrics))
            else:
                print(f"⚠️ No lyrics found for {song_name} by {artist_name}")
                results.append((song_name, artist_name, None))

        except Exception as e:
            print(f"❌ Error fetching lyrics for {song_name} by {artist_name}: {e}")
            results.append((song_name, artist_name, None))

    # 5. COMMIT ALL CHANGES ONCE
    try:
        db.session.commit()
        print("💾 All lyrics saved to database.")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error committing lyrics to DB: {e}")

    return results    








    
    


    