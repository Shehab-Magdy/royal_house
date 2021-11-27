import os
import secrets
from datetime import date
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from sqlalchemy.orm import session
from royal import app, db, crypt
from royal.forms import LoginForm, RegistrationForm, OfferForm
from royal.models import User, offer, items
from flask_login import login_user, current_user, logout_user, login_required


@app.template_filter('datetimeformat')
def datetimeformat(value, format='%Y-%m-%d'):
    return value.strftime(format)

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

def save_image(form_picture):
    hex_name = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    image_name = hex_name + f_ext
    file_path = os.path.join(app.root_path, 'static/items_images', image_name)
    
    output_size = (230,190)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(file_path)
    
    return image_name

@app.route("/item", methods=['GET','POST'])
@login_required
def create_offer_item():
    if request.method == 'GET':
        form = OfferForm()
        if request.args.get('q'):
            q = request.args.get('q')
            item1 = items.query.filter_by(code = q).first()
            form.code.data = item1.code
            form.item_name.data = item1.item_name
            form.item_price.data = item1.item_price
        return render_template("site/items.html", title="Make Offer", form = form)
    elif request.method == 'POST':
        form = OfferForm()
        if form.validate_on_submit():
            new_offer = offer(code = form.code.data, item_name = form.item_name.data, item_price = form.item_price.data, item_sale_price = form.item_sale_price.data, date_from = form.date_from.data, date_to = form.date_to.data, description = form.description.data)
            if form.item_image.data:
                picture_file = save_image(form.item_image.data)
                new_offer.item_image = picture_file
            db.session.add(new_offer)
            db.session.commit()
            flash('Data saved successfully!', 'success')
            return redirect(url_for('create_offer_item'))
        else:
            flash("Data didn't saved successfully!", 'danger')
            return render_template("site/items.html", title="Make Offer", form = form)


@app.route("/magazine", methods=['GET'])
def magazine():
    if request.args:
        start = request.args.get('d_from') #'2021-11-31'
        end = request.args.get('d_to') #'2021-12-31'
        items_offer = offer.query.filter(offer.date_to <= end).filter(offer.date_from >= start).all()
        print(items_offer)
        return render_template("site/magazine.html", title="Magazine", items_offer = items_offer)
    else:
        return render_template("site/magazine.html", title="Magazine")

