from sqlalchemy import select
from website.model import Artist, Artist_Song, Playlist_Song, Song, Song_point
from .. import db
import numpy as np
import json

#to understand the playlist overall mood, we compute the average of all song vectors
#Playlist vibe = (vector_A + vector_B + vector_C + ... ) / N

def Get_playlist_vibe(playlist_id : str) -> np.ndarray | None:
    #1 get song_ id items in this playlist

    items = db.session.execute(
        select(Playlist_Song.c.song_id).where(Playlist_Song.c.playlist_id == playlist_id)
    ).scalars().all()

    if not items:
        return None

    #2 Iterate through list of item to retrive song vectors
    
    song_vector =   db.session.execute(
                    select(Song_point.vec_json).where(Song_point.song_id.in_(items))
                    ).all() #this will return a list of tuples, each one contains the song vector in json string
    #3 Unpack the json 
    vecs = [np.array(json.loads(vj), dtype=np.float32) for (vj,) in song_vector if vj]

    if not vecs:
        return None
    
    #4 Compute the avg vector
    avg = np.mean(np.stack(vecs, axis=0), axis=0) #compute the avg of each column

# 5) Normalize the centroid (optional but recommended for cosine similarity)
    norm = np.linalg.norm(avg)
    return avg / norm if norm > 0 else avg

    




