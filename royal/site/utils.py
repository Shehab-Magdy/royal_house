import os
import secrets
#from datetime import date
from PIL import Image
#from flask import render_template, url_for, flash, redirect, request, abort
#from sqlalchemy.orm import session
#from royal import app#, db, crypt
#from royal.forms import LoginForm, RegistrationForm, OfferForm
#from royal.models import User, offer, items
#from flask_login import login_user, current_user, logout_user, login_required
from flask import current_app


def save_image(form_picture):
    hex_name = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    image_name = hex_name + f_ext
    file_path = os.path.join(current_app.root_path, 'static/items_images', image_name)
    
    output_size = (230,190)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(file_path)
    
    return image_name

# @app.template_filter('datetimeformat')
# def datetimeformat(value, format='%Y-%m-%d'):
#     return value.strftime(format)
