class Config:
    SECRET_KEY = 'bdbfdc3388f5befed4b1a5dbb3c51b8a'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    UPLOAD_FOLDER = 'static/items_images'
    MAX_CONTENT_PATH = 210000 # maximum size of file uploaded – in bytes	
