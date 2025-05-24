import os

from flask import redirect, url_for, render_template, session, request, flash, Blueprint
from .user import User

bp = Blueprint('auth', __name__)

@bp.route('/')
def index():
    return redirect(url_for('auth.login'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User(username=username, password=password)

        if user.is_authenticated():
            session['username'] = username
            
            return redirect(url_for('auth.home_page', username=username))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@bp.route('/user/<username>')
def home_page(username):
    if 'username' not in session or session['username'] != username:
        return redirect(url_for('login'))
    
    return render_template('user.html')
