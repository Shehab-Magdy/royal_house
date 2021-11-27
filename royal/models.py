from datetime import datetime
from royal import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(60), nullable = False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    
    
class offer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    code = db.Column(db.Integer, nullable = False)
    item_name = db.Column(db.String(100), nullable = False)
    item_price = db.Column(db.Float(), nullable = False)
    item_sale_price = db.Column(db.Float(), nullable = False)
    date_from = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    date_to = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    description = db.Column(db.Text, nullable = False)
    item_image = db.Column(db.String(20), nullable = False, default = 'default.jpg')


    def __repr__(self):
        return f"Offer('{self.code}','{self.item_name}','{self.item_price}','{self.item_sale_price}')"

class items(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    code = db.Column(db.Integer, unique = True, nullable = False)
    item_name = db.Column(db.String(100), nullable = False)
    item_price = db.Column(db.Float(), nullable = False)

    def __repr__(self):
        return f"Item('{self.code}','{self.item_name}','{self.item_price}')"