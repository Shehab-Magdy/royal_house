from flask_wtf import FlaskForm
from flask_wtf.file import FileField, file_allowed
#from flask_login import current_user
from wtforms import StringField, SubmitField, TextAreaField, DateField, DecimalField,IntegerField#, PasswordField, BooleanField
from wtforms.validators import DataRequired#, Email, Length, EqualTo, ValidationError, email_validator
#from royal.models import User, offer
#import email_validator


class OfferForm(FlaskForm):
    code = IntegerField('Code', validators=[DataRequired()])
    item_name  = StringField('Name', validators=[])
    item_price = DecimalField('Price', places=2, rounding=None)
    item_sale_price = DecimalField('Sale Price', places=2, rounding=None)
    date_from = DateField('Start Date', format='%Y-%m-%d')
    date_to = DateField('End Date', format='%Y-%m-%d')
    description = TextAreaField('Description', validators=[])
    item_image = FileField('Upload image', validators=[file_allowed(['jpg','png'])])
    submit = SubmitField('Save')
    