from flask import Blueprint, flash, redirect, render_template, url_for, request
from flask_login import login_required, logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User

users_bp = Blueprint('users', __name__)

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password)
        user = User.query.filter_by(username=username).first()
        if user is None:
            user = User(username=username, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Usuari registrat correctament', 'success')
            return redirect(url_for('users.login'))
        else:
            flash('Un usuari amb el mateix nom ja existeix', 'warning')
    return render_template('auth/register.html')


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        remember = request.form.get('remember') == 'on'
        if user and check_password_hash(user.password, password):
            login_user(user, remember=remember)
            flash('Sessió iniciada correctament', 'success')
            if not user.has_answered:
                return redirect(url_for('questions.initial_questions'))
            else:
                return redirect(url_for('home'))
        else:
            flash('Usuari o contrassenya incorrectes', 'warning')
    return render_template('auth/login.html')


@users_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))