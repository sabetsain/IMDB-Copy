import os

from flask import Flask, redirect, url_for, render_template, session, request, flash
from flaskr import create_app
from .user import User

app = create_app()
app.secret_key = 'BAD_SECRET_KEY'

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User(username=username, password=password)

        if user.is_authenticated():
            session['username'] = username
            
            return redirect(url_for('home_page', username=username))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/user/<username>')
def home_page(username):
    if 'username' not in session or session['username'] != username:
        return redirect(url_for('login'))
    
    return f'Hello, {username}!'
