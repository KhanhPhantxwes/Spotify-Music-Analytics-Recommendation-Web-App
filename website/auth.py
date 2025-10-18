from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from flask import Blueprint,render_template, request,flash,redirect, session, url_for
from .model import User
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
import os
from flask_login import current_user, login_user

auth = Blueprint('auth',__name__)

Client_id = 'ecbedf2ee9224930b498f45f0e39301a'
Client_secret = 'bdc98e6f899b423c9f96bec0cbb2860c'
Redirect_url = 'http://127.0.0.1:5000/callback'
Scope = 'user-library-read playlist-modify-public playlist-read-private' #different access scopes

cache_handler = FlaskSessionCacheHandler(session)

############################
#                          #
# AUTHORIZATION  MANAGER   #
#                          #
############################
sp_oauth = SpotifyOAuth(
    client_id = Client_id,
    client_secret = Client_secret,
    redirect_uri = Redirect_url,
    scope = Scope,
    cache_handler = cache_handler,
    show_dialog=True

)
sp = Spotify(auth_manager = sp_oauth)


@auth.route("/spotify-login")
def home_spotify():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        #LOGIN with Spotify page
        auth_url = sp_oauth.get_authorize_url() 
        return redirect(auth_url)
    return redirect(url_for('auth.spotify_getplaylist'))  #if users already logged in

@auth.route("/callback")
def callback():
    sp_oauth.get_access_token(code = request.args.get("code"))
    return redirect(url_for('auth.spotify_getplaylist'))

@auth.route('/spotify-playlist')
def spotify_getplaylist():
    #VALIDATE the token which is currently in the token has not expired
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url() 
        return redirect(auth_url)
    
    #PLAYLIST
    playlists = sp.current_user_playlists() #Get current user playlists without required getting his profile Parameters
    playlists_info = [(pl['name'], pl['external_urls']['spotify'],pl['id']) for pl in playlists['items']]  
    playlists_html = '<br>'.join([f'{name}: {url} : {id}' for name,url,id in playlists_info])

    #Items inside "September" playlist      
    id = '4GEHf0KSpeKjsmQOMiUj0I'
    Items = sp.playlist_items(id, limit =10)
    item_info = [(pl['added_at'], pl['added_by']['external_urls']['spotify'], pl['track']['album']['name'],pl['track']['album']['artists']) for pl in Items['items']]
    item_html = '<br>'.join([f'Time added : {added_at} -- User id : {url} -- Album name : {album} -- Artist : {artist} <br>' 
    for added_at, url, album, artist in item_info])
    
    #Artist top tracks by country
    artist_id = '4wZ6awunqaaVLl5j0WpDFu'
    artist_top_track = sp.artist_top_tracks(artist_id, country="US")
    track_info = [(pl['name']) for pl in artist_top_track['tracks']]
    track_html = '<br>'.join([f'{name}' for name in track_info])

    result_html = playlists_html +  item_html + track_html

    return result_html

@auth.route('/login', methods =[ 'GET','POST'])
def login():
    data = request.form
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('log in successfully!', category='success')
                login_user(user)
                current_user.last_login = datetime.now(ZoneInfo("America/Chicago"))
                db.session.commit()
                return redirect(url_for('views.home'))
            else:
                flash('Try again', category='error')
        else:
            flash('Email does not exist', category='error')
            
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return "<p>Log out</p>"

@auth.route('/signup',methods =[ 'GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        firstname = request.form.get('firstname')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('user exists',category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters', category='error')
        elif len(firstname) < 2:
            flash('first name must be greater than 1 characters', category='error')
        elif password1!=password2:
            flash('Passwords dont match', category='error')
        elif len(password1) < 7:
            flash('password is too short', category='error')
        else:
            new_user = User(email=email, first_name = firstname,password = generate_password_hash(password1,method = 'pbkdf2:sha256'), create_at = datetime.now(ZoneInfo("America/Chicago") ))
            db.session.add(new_user)
            db.session.commit()
            flash('account created', category='success')
            #CHECK IF account was created and save in database
            print(f"✅ Created new user -> ID: {new_user.id}, Email: {new_user.email}, Name: {new_user.first_name}")

            return redirect(url_for('views.home'))
        
    return render_template("signup.html")
