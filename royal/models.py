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
    
class Magazine(db.Model):
    __tablename__ = 'magazine'
    id = db.Column(db.Integer, primary_key = True)
    code = db.Column(db.Integer, unique = True, nullable = False)
    magazine_name = db.Column(db.String(100), nullable = False)
    date_from = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    date_to = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    # offer = db.relationship('Offer', backref = 'offer', lazy = True)

    def __repr__(self):
        return f"Magazine ('{self.code}','{self.magazine_name }','{self.date_from }','{self.date_to }')"

class ItemSections(db.Model):
    __tablename__ = 'itemsections'
    id = db.Column(db.Integer, primary_key = True)
    code = db.Column(db.Integer, unique = True, nullable = False)
    section_name = db.Column(db.String(100), nullable = False)
    # items = db.relationship('Items', backref = 'item', lazy = True)

    def __repr__(self):
        return f"Item Section('{self.code}','{self.section_name}')"

class Magazinesections(db.Model):
    __tablename__ = 'magazine_sections'
    id = db.Column(db.Integer, primary_key = True)
    code = db.Column(db.Integer, unique = True, nullable = False)
    section_name = db.Column(db.String(100), nullable = False)
    # offer = db.relationship('Offer', backref = 'offer', lazy = True)
    
    def __repr__(self):
        return f"Magazine Section('{self.id}','{self.section_name}')"


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key = True)
    code = db.Column(db.Integer, nullable = False)
    item_name = db.Column(db.String(100), nullable = False)
    item_price = db.Column(db.Float(), nullable = False)
    item_sale_price = db.Column(db.Float(), nullable = False)
    description = db.Column(db.Text, nullable = False)
    item_image = db.Column(db.String(20), nullable = False, default = 'default.jpg')
    magazine_id = db.Column(db.Integer, db.ForeignKey('magazine.id'), nullable = False)
    magazinesections_id = db.Column(db.Integer, db.ForeignKey('magazine_sections.id'), nullable = False)
    
    def __repr__(self):
        return f"Offer('{self.code}','{self.item_name}','{self.item_price}','{self.item_sale_price}')"


class Items(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key = True)
    code = db.Column(db.Integer, unique = True, nullable = False)
    item_name = db.Column(db.String(100), nullable = False)
    item_price = db.Column(db.Float(), nullable = False)
    item_section = db.Column(db.Integer, db.ForeignKey('itemsections.id'), nullable = False)

    def __repr__(self):
        return f"Item('{self.code}','{self.item_name}','{self.item_price}')"
