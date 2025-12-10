from ..model import Playlist, User, Artist, Song
from .. import db
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

#True with playlist created by user -- > need another funtion to retrieve artist by mapping song_id

def Get_artists(access_token: str, user:User):
    sp = Spotify(auth=access_token)
    artist_tuple = (db.session.query(Song.artist_id).filter_by(owner_id = user.spotify_id).all())
    # Flatten the list of 1-tuples into plain strings
    artist_list = [r[0] for r in artist_tuple]

    for ar_id in artist_list:
        artist = sp.artist(ar_id)
        #check if artist id already exists
        check_artist = Artist.query.filter_by(artist_id = ar_id).first()

        if check_artist is None:# <-- create only if not exists
            artist_info = Artist(
            artist_id = artist['id'],
            artist_name = artist['name'],
            Genre = ", ".join(artist.get("genres", []))[:150],
            artist_img = artist['images'][0]['url'] if artist["images"] else None,
            artist_populatiry=artist['popularity']
            )
            db.session.add(artist_info)
        else:
            #print(f"Error retrieving artist info")
            # optional: update existing
            check_artist.artist_name = artist["name"]
            check_artist.genre = ", ".join(artist.get("genres", []))[:150]
            check_artist.artist_img = (artist["images"][0]["url"] if artist.get("images") else None)
            check_artist.artist_popularity = artist.get("popularity")

    db.session.commit()

