from flask import render_template, url_for, flash, redirect, request 
from BotFlask import app, db, bcrypt
from BotFlask.forms import RegisterForm, LoginForm
from BotFlask.models import User
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html', title = "About")

@app.route('/contact')
def contact():
    return render_template('contact.html', title = "Contact")

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
    return render_template('register.html', title = "Register", form = form)

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
            return redirect(nextPage) if nextPage else redirect(url_for('index'))
        else:
            flash('Login Failed!', 'danger')
    return render_template('login.html', title = "Login", form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title="Profile")