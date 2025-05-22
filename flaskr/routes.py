from flask import Blueprint, render_template, session
from .db import get_db

bp = Blueprint('movies', __name__)

@bp.route('/user_profile')
def user_profile():
	db = get_db()
	return render_template('user_profile.html')