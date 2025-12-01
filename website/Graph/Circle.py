from sqlalchemy import select
from website.model import Artist, Artist_Song, Song, Song_point,BillboardEntry2,Playlist_Song
from .. import db
import matplotlib.pyplot as plt
from collections import Counter
import io
import base64

def Circle_graph(playlist_id : str):
    stmt = (
    select(Song.mood)
    .join(Playlist_Song, Song.song_id == Playlist_Song.c.song_id)
    .where(Playlist_Song.c.playlist_id == playlist_id)
)
    mood_label = db.session.execute(stmt).scalars().all()

    count = Counter(mood_label)

    # Unique labels
    unique_labels = list(count.keys())

    # Sizes for the pie chart
    sizes = list(count.values())
    # Plot
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.pie(
    sizes,
    labels=unique_labels,
    autopct='%1.1f%%',
    startangle=90
    )
    ax.set_title("Distribution of mood label")
    ax.axis('equal')
    #Save to buffer → base64
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode("ascii")

    # 5. Clean up
    plt.close(fig)
    return img_base64
