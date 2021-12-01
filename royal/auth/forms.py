from flask_wtf import FlaskForm
#from flask_wtf.file import FileField, file_allowed
#from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField#, TextAreaField, DateField, DecimalField,IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError#, email_validator
from royal.models import User#, offer
#import email_validator


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_Password = PasswordField('confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This user is already taken, Please choose another one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already taken, Please choose another one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')
