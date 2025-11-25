from datetime import datetime
import json
from sqlalchemy import select 
from website.Recommendation.get_lyrics_vector import Embed_lyric, clean_lyrics
from website.model import Artist, Artist_Song, BillboardEntry2, Song, User
from .. import db
import lyricsgenius
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import billboard

#GET TOP 100 POPULAR SONGS IN BILLBOARD CHART
def Get_top100(access_token: str, user: User):
    sp = Spotify(auth=access_token)

    #get current_user id
    current_user = user.spotify_id
    # Billboard Hot 100 (most common)
    chart = billboard.ChartData('hot-100')

    print("Date:", chart.date)
    print("Number of entries:", len(chart))

    chart_date_obj = datetime.strptime(chart.date, "%Y-%m-%d").date()

    access_token = "YaMnWwPTM5olA0OrlNIu4tzhwehCDWHlJdguSp1ml1HKL44H9guBSJeNd0wLrL17"
    # Initialize Genius client
    genius = lyricsgenius.Genius(access_token,
        timeout=8,         # seconds per request
        retries=2,         # small number of retries
        sleep_time=0.3,    # pause between requests to be nice
        )

    for entry in chart:
        # 1) check if this song for this chart+date is already stored
        existing = db.session.execute(
            select(BillboardEntry2.id).where(
                BillboardEntry2.chart_name == "hot-100",
                BillboardEntry2.chart_date == chart_date_obj,
                BillboardEntry2.song_title == entry.title,
                BillboardEntry2.artist_name == entry.artist,
            )
        ).scalar_one_or_none()

        if existing:
            # already have this song for this chart/date → skip
            continue

        try:
            song_obj = genius.search_song(entry.title, entry.artist)
        except Exception as e:
            print(f"Failed to fetch lyrics for {entry.title} – {entry.artist}: {e}")
            song_obj = None
        lyric_text = song_obj.lyrics if song_obj else None
        # 3) clean text and compute embedding
        cleaned = clean_lyrics(lyric_text)   # you define this
        vec = Embed_lyric(cleaned)

        db.session.add(BillboardEntry2(
            chart_name = "hot-100",
            chart_date = chart_date_obj,
            rank = entry.rank,
            song_title = entry.title,
            artist_name = entry.artist,
            lyric =  lyric_text,
            vec_json = json.dumps(vec.tolist())


        ))

    db.session.commit()

        
