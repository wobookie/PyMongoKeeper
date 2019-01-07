from flask_login import login_user
from flask import Blueprint, request, redirect, render_template, url_for, session, jsonify
from app.models import user
from app.db import mongo

bp = Blueprint('login', __name__)

def do_login(username, password):
    return mongo.init_mongo_connection(username, password)

# Route for handling the login page logic
@bp.route('/')
def home():
    return render_template('auth/login.html')

# Route for handling the login page logic
@bp.route('/login')
def login():
    return render_template('auth/login.html')

@bp.route('/validateLogin', methods=['POST'])
def validateLogin():
    error = None
    redirect = '/'

    if do_login(request.form['username'], request.form['password']):
        login_user(user.User(request.form['username']))
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        session['logged_in'] = True
        status = True
        redirect = ('/dashboard')
    else:
        session['logged_in'] = False
        status = False

    return jsonify({'result': status, 'redirect': redirect})

