import json

with open('config.json') as config_file:
    config = json.load(config_file)

class Config:
    SECRET_KEY = config.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = config.get('SQLALCHEMY_DATABASE_URI')
    UPLOAD_FOLDER = 'static/items_images'
    MAX_CONTENT_PATH = 210000 # maximum size of file uploaded – in bytes	
