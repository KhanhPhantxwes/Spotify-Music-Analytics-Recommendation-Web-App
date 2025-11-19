from sqlalchemy import select
from website.model import Artist, Artist_Song, Song, Song_point
from .. import db
import numpy as np
import json
import lyricsgenius
from sentence_transformers import SentenceTransformer

#1 Get the lyric transformation model
EMB_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"#"sentence-transformers/all-MiniLM-L6-v2"
_model = None    # global cache for the model

def get_model():
    """Load the SentenceTransformer model once and reuse it."""
    global _model
    if _model is None:
        _model = SentenceTransformer(EMB_MODEL_NAME)
    return _model

def clean_lyrics(text: str) -> str:
    if not text: return ""
    t = text.replace("\r"," ").replace("\n","\n")  # keep line breaks
    t = t.replace("[Chorus]", "").replace("[Verse]", "").replace("[Bridge]", "")
    return " ".join(t.split())  # collapse whitespace

#2 Convert lyric text into a normalized vector
def Embed_lyric(lyric: str) -> np.ndarray:
    model = get_model()
    # model.encode returns a 2D array when you pass a list -> [0] gives you the first vector
    vec = model.encode([lyric], normalize_embeddings=True)[0]
    return vec


## Query the table and return the lyric vector
def ensure_song_embedding(song_id: str) -> np.ndarray | None:
    """
    Return the embedding for this song_id.
    - If it exists in Song_point, load and return it.
    - If not, compute from lyrics, store, and return.
    - If no lyrics, return None.
    """
    # 1) check if already in embedding table
    row = db.session.execute(
        select(Song_point).where(Song_point.song_id == song_id)
    ).scalar_one_or_none()

    if row:
        # row.vec_json is a JSON string: "[0.12, -0.03, ...]"
        return np.array(json.loads(row.vec_json), dtype=np.float32)
    # 2) no embedding yet → fetch song & lyrics
    song = db.session.execute(
        select(Song).where(Song.song_id == song_id)
    ).scalar_one_or_none()

    if not song or not song.lyric:
        # no song or no lyrics -> can't embed
        return None

    # 3) clean text and compute embedding
    cleaned = clean_lyrics(song.lyric)   # you define this
    vec = Embed_lyric(cleaned)
    # 4) store in Song_point for future reuse
    db.session.merge(
        Song_point(
            song_id=song_id,
            vec_json=json.dumps(vec.tolist()),
            dim=int(vec.shape[0])
        )
    )
    db.session.commit()

    # 5) return vector to caller
    return vec