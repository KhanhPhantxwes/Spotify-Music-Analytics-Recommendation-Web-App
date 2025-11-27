from sqlalchemy import select
from website.Recommendation.get_playlist_vector import Get_playlist_vibe
from website.model import Artist, Artist_Song, Song, Song_point,BillboardEntry2
from .. import db
import numpy as np
import json
import lyricsgenius
from sentence_transformers import SentenceTransformer


def _json_to_vec(vj: str) -> np.ndarray:
    """Convert stored JSON string to numpy vector."""
    return np.array(json.loads(vj), dtype=np.float32)

def _cosine(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity; works even if vectors aren't normalized."""
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


#Given my playlist vibe vector, rank the song which is the most similar to the playlist vibe vector from billboard top 100
def Get_recommendation(playlistid: str,top_k: int = 30, candidate_limit: int = 10000):
    #Playlist vibe load
    current_playlist_vive = Get_playlist_vibe(playlistid)
    if current_playlist_vive is None:
        return []

    #Load top 100 song from Billboard entry 2 table
    candidate_list = db.session.execute(
        select(
            BillboardEntry2.rank,
            BillboardEntry2.song_title,
            BillboardEntry2.artist_name,
            BillboardEntry2.vec_json,
            BillboardEntry2.chart_date
        ).order_by(BillboardEntry2.rank.asc())
    ).all()
    #Turn vec_json into numpy vector
    scored = []
    for rank, title, artist, vec_json, chart_date in candidate_list:

        if not vec_json:
            # no embedding stored
            continue

        v = _json_to_vec(vec_json)

    #Compute similar between playlist vibe and each song
        sim = _cosine(current_playlist_vive, v)
        scored.append({
            "rank": rank,
            "song_title": title,
            "artist_name": artist,
            "similarity": sim,
            "chart_date": chart_date.isoformat() if chart_date else None
        })

    #Sort and rank similarity
        scored.sort(key=lambda x: x["similarity"], reverse=True)


    #Return top K
    return scored[:top_k]
    
