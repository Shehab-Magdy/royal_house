import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from sqlalchemy.orm import session
from royal import app, db, crypt
from royal.forms import LoginForm, RegistrationForm
from royal.models import User
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    return render_template("site/dashboard.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = crypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data,password=hashed_password,email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account is created successfully for {form.username.data}! You may login now.','success')
        return redirect(url_for('login'))
    return render_template("auth/sign_up.html", title="Create User", form = form)


@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and crypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Please check your email and password.', 'danger')
    return render_template("auth/login.html", title="Login", form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
