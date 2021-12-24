from flask_wtf import FlaskForm
from flask_wtf.file import FileField, file_allowed
#from flask_login import current_user
from wtforms import StringField, SubmitField, TextAreaField, DateField, DecimalField,IntegerField#, PasswordField, BooleanField
from wtforms.validators import DataRequired#, Email, Length, EqualTo, ValidationError, email_validator
from royal.models import Magazine, Magazinesections#, Offer, Items, User, 
#from royal.models import User, offer
#import email_validator
from wtforms_sqlalchemy.fields import QuerySelectField

def magazine_sections():
    mag_sections = Magazinesections.query.all()
    return mag_sections

def magazine_selection():
    mag = Magazine.query.all()
    return mag

class MagazineSelection(FlaskForm):
    mag = QuerySelectField('Magazine',validators=[DataRequired()],query_factory=magazine_selection,allow_blank=True,blank_text='Select Magazine', get_label='magazine_name')
    submit = SubmitField('Get')

class MagazineSection(FlaskForm):
    code = IntegerField('Code', validators=[DataRequired()])
    magazine_section = StringField('Name', validators=[])
    submit = SubmitField('Save')

class OfferForm(FlaskForm):
    code = IntegerField('Code', validators=[DataRequired()])
    item_name  = StringField('Name', validators=[])
    item_price = DecimalField('Price', places=2, rounding=None)
    item_sale_price = DecimalField('Sale Price', places=2, rounding=None)
    mag = QuerySelectField('Magazine',validators=[DataRequired()],query_factory=magazine_selection,allow_blank=True,blank_text='Select Magazine', get_label='magazine_name')
    mag_sections = QuerySelectField('Magazine Section',validators=[DataRequired()],query_factory=magazine_sections,allow_blank=True,blank_text='Select Section', get_label='section_name')
    description = TextAreaField('Description', validators=[])
    item_image = FileField('Upload image', validators=[file_allowed(['jpg','png'])])
    submit = SubmitField('Save')

class MagazineForm(FlaskForm):
    code = IntegerField('Code', validators=[DataRequired()])
    magazine_name  = StringField('Name', validators=[])
    date_from = DateField('Start Date', format='%Y-%m-%d')
    date_to = DateField('End Date', format='%Y-%m-%d')
    submit = SubmitField('Save')