from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from royal.config import Config


db= SQLAlchemy()
crypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.debug = True

    db.init_app(app)
    crypt.init_app(app)
    login_manager.init_app(app)

    from royal.site.routes import site
    from royal.auth.routes import auth
    from royal.errors.handlers import errors
    app.register_blueprint(auth)
    app.register_blueprint(site)
    app.register_blueprint(errors)

    return app