import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = '62ab795ca335e00450ff3fc764f415cf' #make env variable
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587 #sending email
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "aryahaji.bot@gmail.com"
app.config['MAIL_PASSWORD'] = "datsyuk13"
mail = Mail(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
loginManager = LoginManager(app)
loginManager.login_view = 'login'
loginManager.login_message_category= 'info'

from BotFlask import routes
