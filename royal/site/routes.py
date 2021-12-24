#import os
#import secrets
#from datetime import date
#from PIL import Image
from datetime import datetime
from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
#from sqlalchemy.orm import session
from royal import db  # ,app,  crypt
# ,LoginForm, RegistrationForm,
from royal.site.forms import OfferForm, MagazineForm, MagazineSelection, MagazineSection
from royal.site.utils import save_image
from royal.models import Offer, Items, Magazine,Magazinesections  # , User,
# , login_user, current_user, logout_user,
from flask_login import login_required, utils
from flask_weasyprint import HTML, render_pdf

site = Blueprint('site', __name__)


@site.route("/")
@site.route("/home")
def home():
    return render_template("site/dashboard.html")


@site.route("/item", methods=['GET', 'POST'])
@login_required
def create_offer_item():
    if request.method == 'GET':
        form = OfferForm()
        if request.args.get('q'):
            q = request.args.get('q')
            item1 = Items.query.filter_by(code=q).first()
            form.code.data = item1.code
            form.item_name.data = item1.item_name
            form.item_price.data = item1.item_price
        return render_template("site/items.html", title="Make Offer", form=form)
    elif request.method == 'POST':
        form = OfferForm()
        if form.validate_on_submit():
            new_offer = Offer(code=form.code.data, item_name=form.item_name.data, item_price=form.item_price.data, item_sale_price=form.item_sale_price.data, magazine_id=form.mag.data.id, magazinesections_id=form.mag_sections.data.id, description=form.description.data)
            if form.item_image.data:
                picture_file = save_image(form.item_image.data)
                new_offer.item_image = picture_file
            db.session.add(new_offer)
            db.session.commit()
            flash('Data saved successfully!', 'success')
            return redirect(url_for('site.create_offer_item'))
        else:
            flash("Data didn't saved successfully!", 'danger')
            return render_template("site/items.html", title="Make Offer", form=form)


@site.route("/magazine", methods=['GET', 'POST'])
def magazine():
    if request.method=='POST':
        mag_form = MagazineSelection()
        mag = mag_form.mag.data.id
        items_offer = Offer.query.filter(Offer.magazine_id == mag).all()
        file_name = 'royal/static/pdf/magazine' + str(datetime.now().strftime("%Y%m%d%H%M%S"))+'.pdf'
        download_file_name = 'magazine' + str(datetime.now().strftime("%Y%m%d%H%M%S"))+'.pdf'
        html_file = render_template("site/magazine.html", title="Magazine", items_offer=items_offer, file_name=download_file_name, form=mag_form)
        HTML(string=html_file).write_pdf(file_name)
        return html_file
    else:
        mag_form = MagazineSelection()
        return render_template("site/magazine.html", title="Magazine",form=mag_form)


@site.route("/add_magazine", methods=['GET', 'POST'])
def add_magazine():
    if request.method == 'GET':
        form = MagazineForm()
        return render_template("site/add_magazine.html", title="Add Magazine", form=form)
    elif request.method == 'POST':
        form = MagazineForm()
        if form.validate_on_submit():
            new_magazine = Magazine(code=form.code.data, magazine_name=form.magazine_name.data, date_from=form.date_from.data, date_to=form.date_to.data)
            db.session.add(new_magazine)
            db.session.commit()
            flash('Data saved successfully!', 'success')
            return redirect(url_for('site.add_magazine'))
        else:
            flash("Data didn't saved. Please review your inputs!", 'danger')
            return render_template("site/add_magazine.html", title="Add Magazine", form=form)

@site.route("/add_magazine_section", methods=['GET', 'POST'])
def add_magazine_section():
    if request.method == 'GET':
        form = MagazineSection()
        return render_template("site/add_magazine_sec.html", title="Add New Magazine Section", form=form)
    elif request.method == 'POST':
        form = MagazineSection()
        if form.validate_on_submit():
            new_mag_sec = Magazinesections(code=form.code.data, section_name=form.magazine_section.data)
            db.session.add(new_mag_sec)
            db.session.commit()
            flash('Data saved successfully!', 'success')
            return redirect(url_for('site.add_magazine_section'))
        else:
            flash("Data didn't saved. Please review your inputs!", 'danger')
            return render_template("site/add_magazine_sec.html", title="Add Magazine", form=form)
