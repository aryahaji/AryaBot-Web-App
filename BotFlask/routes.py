from flask import render_template, url_for, flash, redirect, request, abort
from BotFlask import app, db, bcrypt, mail
from BotFlask.forms import RegisterForm, LoginForm, CheckoutForm, ResetForm, ResetPassword
from BotFlask.models import User, Profile
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import requests
from bs4 import BeautifulSoup
import random
import tweepy
from tweepy import OAuthHandler
import json
from twilio.rest import Client

def getJoke():
    response = requests.get("https://official-joke-api.appspot.com/random_joke")
    jsonData = json.loads(response.text)
    setup = jsonData["setup"]
    punchline = jsonData["punchline"]
    space = " "
    joke = setup + space + punchline
    return joke

@app.route('/index/tweet')
def tweet():
    consumer_key = app.config['CONSUMER_KEY']
    consumer_secret = app.config['CONSUMER_SECRET']
    access_token = app.config['ACCESS_TOKEN']
    access_token_secret = app.config['ACCESS_TOKEN_SECRET']
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    api.update_status("I'm satisfied with AryaBot " + "Here is one of the jokes, " + getJoke())
    return redirect(url_for('index'))

#home page
@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html', joke=getJoke())

@app.route('/text', methods=['POST', 'GET'])
def text():
    account_sid = app.config["ACCOUNT_SID"]
    auth_token = app.config["AUTH_TOKEN"]
    client = Client(account_sid, auth_token)
    form = CheckoutForm()
    if form.phone.data != None:
        message = client.messages.create(
            body=getJoke(),
            from_=app.config['TWILIO_PHONE'],
            to=form.phone.data
        )
    return render_template('text.html', form=form)

#about page
@app.route('/about')
def about():
    return render_template('about.html', title="About")

#profiles page
@app.route('/account/profiles', methods=['GET', 'POST'])
def profiles():
    profiles = Profile.query.all()
    return render_template('account.html', title="Profiles", profiles=profiles)

#register for account
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') #make sure it is a string instead of bytes
        user = User(username=form.username.data.lower(), email=form.email.data.lower(), password=hashed_password) #create user with the hashed password to put in DB
        db.session.add(user) #add user to DB
        db.session.commit() #commit changes
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login')) #redirect to login upon account creation
    return render_template('register.html', title="Register", form=form)

#if user exists and passwords match log them in and redirect to home page, if not give login failed message
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            nextPage = request.args.get('next') #route user to protected page they were trying to access before being prompted to login
            return redirect(nextPage) if nextPage else redirect(url_for('profiles'))
        else:
            flash('Login Failed!', 'danger')
    return render_template('login.html', title="Login", form=form)

#logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

#account page
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    return render_template('account.html', title="Account")

#create new profile
@app.route('/newProfile', methods=['GET', 'POST'])
@login_required
def newProfile():  
    form = CheckoutForm()
    if form.validate_on_submit():
        profile = Profile(profileName = form.profileName.data, firstName = form.firstName.data, lastName = form.lastName.data, 
        email = form.email.data, phone = form.phone.data, address = form.address.data, address1 = form.address1.data, city = form.city.data,
        state = form.state.data, zipCode = form.zipCode.data, country = form.country.data, cc = form.cc.data, expMonth = form.expMonth.data,
        expYear = form.expYear.data, cvv = form.cvv.data, url = form.url.data, user = current_user) 
        db.session.add(profile)
        db.session.commit()
        flash(f"Profile Created!")
        return redirect(url_for('profiles'))
    return render_template('newProfile.html', title="New Profile", form=form)

#going to specific profile
@app.route('/account/profiles/<int:profile_id>')
@login_required
def selectedProfile(profile_id):
    profile = Profile.query.get_or_404(profile_id)
    return render_template('viewProfile.html', title=profile.id, profile=profile)

#deleting a profile
@app.route('/account/profiles/<int:profile_id>/delete', methods=['POST'])
@login_required
def deleteProfile(profile_id):
    profile = Profile.query.get_or_404(profile_id)
    if profile.user != current_user:
        abort(403)
    db.session.delete(profile)
    db.session.commit()
    flash('Your profile has been deleted!', 'success') 
    return redirect(url_for('account'))

#send resest email
def sendResetEmail(user):
    token = user.getResetToken()
    message = Message('Password Reset Request',
                  sender='reset@demo.com',
                  recipients=[user.email])
    message.body = f'''To reset your password, visit the following link:
{url_for('resetPassword', token=token, _external=True)}
If you did not make this request then simply ignore this email.
'''
    mail.send(message)

#request password reset 
@app.route('/resetPassword', methods=['GET', 'POST'])
def resetPasswordRequest():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        sendResetEmail(user)
        flash('Email has been sent with instructions to reset your password!', 'info')
        return redirect(url_for('login'))
    return render_template('resetRequest.html', title='Reset Password', form=form)

#reset password
@app.route('/resetPassword/<token>', methods=['GET', 'POST'])
def resetPassword(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verifyResetToken(token)
    if user is None:
        flash('That token has expired or is invalid', 'warning')
        return redirect(url_for('resetPasswordRequest'))
    form = ResetPassword()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit() 
        flash('Your password has been changed!', 'success')
        return redirect(url_for('login'))
    return render_template('reset.html', title='Reset Password', form=form)