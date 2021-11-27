from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'bdbfdc3388f5befed4b1a5dbb3c51b8a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['UPLOAD_FOLDER'] = 'static/items_images'
app.config['MAX_CONTENT_PATH']= 210000 # maximum size of file uploaded – in bytes	
app.debug = True
db= SQLAlchemy(app)
crypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from royal import routes