from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from models import db
from models.user_model import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            flash('Login Successful', category='success')
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Check email and password', category='error')

    return render_template("login.html")


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        return render_template("sign_up.html")

    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if user:
        flash('Email already registered', category='error')
        return render_template("sign_up.html")
    new_user = User(username=username, email=email,
                    password=generate_password_hash(password, method='pbkdf2:sha256', salt_length=8))
    flash("User created successfully", category="success")
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
    return redirect(url_for('main.dashboard'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))