from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from BotFlask.models import User, Profile

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    passwordConfirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up!')

    #prevents crash by ensuring username isn't already in DB
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken already!')
    
    #prevents crash by ensuring email isn't already in DB
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That email is already being used!')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login!')

class CheckoutForm(FlaskForm):
    profileName = StringField('Profile Name', validators=[DataRequired()])
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    address1 = StringField('Address Line 2')
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zipCode = StringField('Zip', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    cc = StringField('Credit Card', validators=[DataRequired(), Length(16)])
    expMonth = StringField('Expiry Month', validators=[DataRequired(), Length(max=2)])
    expYear = StringField('Expiry Year', validators=[DataRequired(), Length(max=2)])
    cvv = StringField('CVV', validators=[DataRequired(), Length(min=3, max=4)])
    url = StringField('URL', validators=[DataRequired()])
    submit = SubmitField('Checkout')

#request to reset password
class ResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset') 

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if None:
            raise ValidationError('There is no account found with that email. You must register first!')

#reset password
class ResetPassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    passwordConfirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password!')