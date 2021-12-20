#import os
#import secrets
#from datetime import date
#from PIL import Image
from datetime import datetime
from flask import render_template, url_for, flash, redirect, request,Blueprint, abort
#from sqlalchemy.orm import session
from royal import db#,app,  crypt
from royal.site.forms import OfferForm#,LoginForm, RegistrationForm, 
from royal.site.utils import save_image
from royal.models import offer, items#, User, 
from flask_login import login_required, utils#, login_user, current_user, logout_user,
from flask_weasyprint import HTML, render_pdf

site = Blueprint('site', __name__)

@site.route("/")
@site.route("/home")
def home():
    return render_template("site/dashboard.html")


@site.route("/item", methods=['GET','POST'])
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
            return redirect(url_for('site.create_offer_item'))
        else:
            flash("Data didn't saved successfully!", 'danger')
            return render_template("site/items.html", title="Make Offer", form = form)


@site.route("/magazine", methods=['GET'])
def magazine():
    if request.args:
        start = request.args.get('d_from') #'2021-11-31'
        end = request.args.get('d_to') #'2021-12-31'
        items_offer = offer.query.filter(offer.date_to <= end).filter(offer.date_from >= start).all()
        # print(items_offer)
        file_name = 'royal/static/pdf/magazine'+str(datetime.now().strftime("%Y%m%d%H%M%S"))+'.pdf'
        download_file_name = 'magazine'+str(datetime.now().strftime("%Y%m%d%H%M%S"))+'.pdf'
        html_file = render_template("site/magazine.html", title="Magazine", items_offer = items_offer,file_name=download_file_name)
        print(file_name)
        # render_pdf()
        HTML(string = html_file).write_pdf(file_name)
        return html_file
    else:
        return render_template("site/magazine.html", title="Magazine")

