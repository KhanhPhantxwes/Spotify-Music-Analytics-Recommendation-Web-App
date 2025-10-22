from .model import Playlist, User
from . import db
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

def Get_currentuser_playlist(access_token: str, user: User):
    sp = Spotify(auth=access_token)
    playlists = sp.current_user_playlists()

    def upsert_page(page):
        for p in page.get("items", []):
            pid  = p["id"]
            name = p.get("name")
            img  = None
            if p.get("images"):  # check before accessing index 0
                img = p["images"][0].get("url")

            # Upsert logic: if exists, update; else add new
            existing = Playlist.query.get(pid)
            if existing:
                existing.playlist_name = name
                existing.playlist_img  = img
                existing.owner_id      = user.spotify_id
            else:
                new_pl = Playlist(
                    playlist_id=pid,
                    playlist_name=name,
                    playlist_img=img,
                    owner_id=user.spotify_id
                )
                db.session.add(new_pl)
    
    upsert_page(playlists)
    # Handle first page
    upsert_page(playlists)

    # Paginate through the rest
    while playlists.get("next"):
        playlists = sp.next(playlists)
        upsert_page(playlists)

    # Commit once after all playlists are added/updated
    db.session.commit()

    print(f"✅ Synced playlists for {user.spotify_id}")




