from flask import Blueprint,render_template, request,flash,redirect, url_for
from .model import User
from werkzeug.security import generate_password_hash,check_password_hash
from . import db

auth = Blueprint('auth',__name__)

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
            new_user = User(email=email, first_name = firstname,password = generate_password_hash(password1,method = 'pbkdf2:sha256') )
            db.session.add(new_user)
            db.session.commit()
            flash('account created', category='success')
            #CHECK IF account was created and save in database
            print(f"✅ Created new user -> ID: {new_user.id}, Email: {new_user.email}, Name: {new_user.first_name}")

            return redirect(url_for('views.home'))
        
       


  
    return render_template("signup.html")
